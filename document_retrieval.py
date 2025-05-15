import os
import re
import logging
from typing import Dict, List, Optional, Tuple
import PyPDF2
import json
from pathlib import Path
import numpy as np
import tempfile
from datetime import datetime

# Configuration for semantic search
ENABLE_SEMANTIC_SEARCH = True  # Set to False to disable semantic search
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Model for creating embeddings
SEMANTIC_CHUNK_SIZE = 300  # Characters per chunk for semantic indexing
SIMILARITY_THRESHOLD = 0.5  # Minimum similarity score for semantic matches

# Optional: if available in the environment - for vector embeddings
try:
    import torch
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True and ENABLE_SEMANTIC_SEARCH
except ImportError:
    EMBEDDINGS_AVAILABLE = False

class DocumentStore:
    """Manages document storage and retrieval for debate agents"""
    
    def __init__(self, documents_dir: str = "agent_documents", enable_semantic_search: bool = ENABLE_SEMANTIC_SEARCH):
        """
        Initialize the document store
        
        Args:
            documents_dir: Directory to store uploaded documents and metadata
            enable_semantic_search: Whether to enable semantic search capabilities
        """
        self.documents_dir = documents_dir
        self.index_file = os.path.join(documents_dir, "document_index.json")
        self.document_data = {}
        self.vector_db = {}
        self.model = None
        self.enable_semantic_search = enable_semantic_search
        
        # Initialize embedding model if available and enabled
        if EMBEDDINGS_AVAILABLE and self.enable_semantic_search:
            try:
                self.model = SentenceTransformer(EMBEDDING_MODEL)
                logging.info(f"Initialized sentence embeddings model '{EMBEDDING_MODEL}' for semantic search")
            except Exception as e:
                logging.error(f"Failed to load embedding model: {str(e)}")
                self.model = None
        
        # Create documents directory if it doesn't exist
        os.makedirs(documents_dir, exist_ok=True)
        
        # Create agent-specific subdirectories
        for agent in ["United_States", "European_Union", "Peoples_Republic_of_China"]:
            os.makedirs(os.path.join(documents_dir, agent), exist_ok=True)
        
        # Load existing document index if it exists
        self._load_index()
    
    def _load_index(self):
        """Load document index from disk"""
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    self.document_data = json.load(f)
                logging.info(f"Loaded {len(self.document_data)} documents from index")
            except Exception as e:
                logging.error(f"Failed to load document index: {str(e)}")
                self.document_data = {}
    
    def _save_index(self):
        """Save document index to disk"""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.document_data, f, indent=2)
            logging.info(f"Saved {len(self.document_data)} documents to index")
        except Exception as e:
            logging.error(f"Failed to save document index: {str(e)}")
    
    def upload_document(self, 
                       file_path: str, 
                       agent_name: str, 
                       document_type: str, 
                       title: Optional[str] = None,
                       description: Optional[str] = None) -> str:
        """
        Upload and process a PDF document
        
        Args:
            file_path: Path to the PDF file
            agent_name: Name of the agent this document belongs to (United_States, European_Union, etc.)
            document_type: Type of document (regulation, strategy, policy, etc.)
            title: Document title (if None, use filename)
            description: Document description
            
        Returns:
            Document ID if successful, empty string if failed
        """
        try:
            # Validate file exists and is PDF
            if not os.path.exists(file_path):
                logging.error(f"File not found: {file_path}")
                return ""
            
            if not file_path.lower().endswith('.pdf'):
                logging.error(f"File is not a PDF: {file_path}")
                return ""
            
            # Format agent name for directory
            agent_dir = agent_name.replace(" ", "_")
            
            # Create document ID and target paths
            document_id = f"{agent_dir}_{os.path.basename(file_path).replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            target_path = os.path.join(self.documents_dir, agent_dir, os.path.basename(file_path))
            text_path = os.path.join(self.documents_dir, agent_dir, f"{document_id}.txt")
            
            # Extract text from PDF
            extracted_text, num_pages = self._extract_text_from_pdf(file_path)
            
            if not extracted_text:
                logging.error(f"Failed to extract text from {file_path}")
                return ""
            
            # Save extracted text
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(extracted_text)
            
            # Create document metadata
            self.document_data[document_id] = {
                "id": document_id,
                "title": title or os.path.basename(file_path),
                "agent": agent_name,
                "type": document_type,
                "description": description or "",
                "original_file": target_path,
                "text_file": text_path,
                "pages": num_pages,
                "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "char_count": len(extracted_text)
            }
            
            # Save index
            self._save_index()
            
            # Create embeddings if model is available
            if self.model:
                self._create_embeddings(document_id, extracted_text)
            
            logging.info(f"Successfully uploaded document: {document_id}")
            return document_id
            
        except Exception as e:
            logging.error(f"Error uploading document: {str(e)}")
            return ""
    
    def _extract_text_from_pdf(self, file_path: str) -> Tuple[str, int]:
        """
        Extract text from a PDF file
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Tuple of (extracted_text, number_of_pages)
        """
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                
                text = []
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    text.append(f"--- Page {page_num + 1} ---\n{page.extract_text()}\n")
                
                return "\n".join(text), num_pages
        except Exception as e:
            logging.error(f"Error extracting text from PDF: {str(e)}")
            return "", 0
    
    def _create_embeddings(self, document_id: str, text: str):
        """
        Create embeddings for document chunks for semantic search
        
        Args:
            document_id: Document ID
            text: Extracted text from the document
        """
        try:
            # Split into chunks - more sophisticated than simple paragraph splitting
            chunks = self._split_text_into_chunks(text)
            
            if not chunks:
                logging.warning(f"No valid chunks found in document {document_id}")
                return
            
            logging.info(f"Splitting document {document_id} into {len(chunks)} semantic chunks")
            
            # Generate embeddings with batching for efficiency
            embeddings = self.model.encode(chunks, batch_size=8, show_progress_bar=True)
            
            # Store in vector database with page information
            self.vector_db[document_id] = {
                "chunks": chunks,
                "embeddings": embeddings,
                "chunk_metadata": self._extract_chunk_metadata(chunks, text)
            }
            
            logging.info(f"Created embeddings for {len(chunks)} chunks in document {document_id}")
        except Exception as e:
            logging.error(f"Error creating embeddings: {str(e)}")
    
    def _split_text_into_chunks(self, text: str) -> List[str]:
        """
        Split text into semantic chunks for better embeddings
        
        Args:
            text: Document text
        
        Returns:
            List of text chunks
        """
        # First split by pages
        pages = re.split(r'--- Page \d+ ---', text)
        
        chunks = []
        for page in pages:
            if not page.strip():
                continue
            
            # Get page number if available
            page_num = None
            page_match = re.search(r'--- Page (\d+) ---', page)
            if page_match:
                page_num = page_match.group(1)
            
            # Split page into paragraphs
            paragraphs = [p for p in re.split(r'\n\s*\n', page) if p.strip()]
            
            # Process each paragraph
            for para in paragraphs:
                # If paragraph is short, add it as is
                if len(para) <= SEMANTIC_CHUNK_SIZE:
                    chunks.append(para.strip())
                else:
                    # Split large paragraphs into sentences
                    sentences = re.split(r'(?<=[.!?])\s+', para)
                    current_chunk = ""
                    
                    for sentence in sentences:
                        if len(current_chunk) + len(sentence) <= SEMANTIC_CHUNK_SIZE:
                            current_chunk += " " + sentence if current_chunk else sentence
                        else:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                            current_chunk = sentence
                    
                    if current_chunk:
                        chunks.append(current_chunk.strip())
        
        # Remove any empty chunks or chunks that are too short
        return [chunk for chunk in chunks if len(chunk) > 20]
    
    def _extract_chunk_metadata(self, chunks: List[str], full_text: str) -> List[Dict]:
        """
        Extract metadata for each chunk (page numbers, section info)
        
        Args:
            chunks: List of text chunks
            full_text: Full document text
        
        Returns:
            List of metadata dictionaries for each chunk
        """
        metadata = []
        
        for chunk in chunks:
            # Initialize metadata for this chunk
            chunk_meta = {"page": None, "section": None}
            
            # Find the chunk in the original text to get context
            chunk_pos = full_text.find(chunk)
            if chunk_pos >= 0:
                # Look for page number before this chunk
                text_before = full_text[:chunk_pos]
                page_matches = list(re.finditer(r'--- Page (\d+) ---', text_before))
                if page_matches:
                    chunk_meta["page"] = page_matches[-1].group(1)
                
                # Look for potential section headers
                section_context = full_text[max(0, chunk_pos - 200):chunk_pos]
                section_match = re.search(r'([A-Z][A-Z\s]+:)|(\bI{1,3}\.|\bIV\.|\bV\.|\bVI\.|\bVII\.|\bVIII\.|\bIX\.|\bX\.)', section_context)
                if section_match:
                    chunk_meta["section"] = section_match.group(0).strip()
            
            metadata.append(chunk_meta)
        
        return metadata
    
    def get_document_list(self, agent_name: Optional[str] = None) -> List[Dict]:
        """
        Get list of documents, optionally filtered by agent
        
        Args:
            agent_name: Optional filter by agent name
            
        Returns:
            List of document metadata dictionaries
        """
        if agent_name:
            return [doc for doc in self.document_data.values() 
                   if doc["agent"].lower() == agent_name.lower()]
        return list(self.document_data.values())
    
    def get_document_text(self, document_id: str) -> str:
        """
        Get full text of a document
        
        Args:
            document_id: Document ID
            
        Returns:
            Full document text
        """
        if document_id not in self.document_data:
            logging.error(f"Document not found: {document_id}")
            return ""
        
        text_path = self.document_data[document_id]["text_file"]
        try:
            with open(text_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logging.error(f"Error reading document text: {str(e)}")
            return ""
    
    def search_documents(self, 
                        query: str, 
                        agent_name: Optional[str] = None,
                        document_type: Optional[str] = None,
                        max_results: int = 10) -> List[Dict]:
        """
        Search for documents by keyword or semantic similarity
        
        Args:
            query: Search query
            agent_name: Optional filter by agent name
            document_type: Optional filter by document type
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with document snippets
        """
        results = []
        
        # Filter documents by agent and type
        filtered_docs = list(self.document_data.values())
        if agent_name:
            filtered_docs = [doc for doc in filtered_docs 
                           if doc["agent"].lower() == agent_name.lower()]
        if document_type:
            filtered_docs = [doc for doc in filtered_docs 
                           if doc["type"].lower() == document_type.lower()]
        
        # Try semantic search first if available
        if self.model and query and self.enable_semantic_search:
            semantic_results = self._semantic_search(query, filtered_docs, max_results)
            if semantic_results:
                # Add a marker that these are semantic search results
                for result in semantic_results:
                    result["search_method"] = "semantic"
                return semantic_results
        
        # Fall back to keyword search
        logging.info(f"Falling back to keyword search for: '{query}'")
        for doc in filtered_docs:
            doc_id = doc["id"]
            doc_text = self.get_document_text(doc_id)
            
            # Simple keyword search
            if query.lower() in doc_text.lower():
                # Find relevant snippets
                snippets = self._find_snippets(doc_text, query)
                
                results.append({
                    "document_id": doc_id,
                    "title": doc["title"],
                    "agent": doc["agent"],
                    "type": doc["type"],
                    "snippets": snippets[:3],  # Top 3 snippets
                    "score": len(snippets),  # Score by number of matches
                    "search_method": "keyword"
                })
        
        # Sort by score and limit results
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:max_results]
    
    def _semantic_search(self, query: str, documents: List[Dict], max_results: int) -> List[Dict]:
        """
        Perform semantic search using embeddings
        
        Args:
            query: Search query
            documents: List of document metadata
            max_results: Maximum number of results
            
        Returns:
            List of search results with document snippets
        """
        try:
            if not self.enable_semantic_search or not self.model:
                return []
            
            logging.info(f"Performing semantic search for: '{query}'")
            
            # Encode the query
            query_embedding = self.model.encode(query)
            results = []
            
            for doc in documents:
                doc_id = doc["id"]
                
                # Skip if document doesn't have embeddings
                if doc_id not in self.vector_db:
                    continue
                
                chunks = self.vector_db[doc_id]["chunks"]
                embeddings = self.vector_db[doc_id]["embeddings"]
                chunk_metadata = self.vector_db[doc_id].get("chunk_metadata", [{}] * len(chunks))
                
                if len(chunks) == 0:
                    continue
                    
                # Calculate cosine similarity
                similarities = np.dot(embeddings, query_embedding) / (
                    np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
                )
                
                # Get top chunks
                top_indices = np.argsort(similarities)[-5:][::-1]  # Get 5 instead of 3 for more context
                top_scores = similarities[top_indices]
                
                # Only include if there's a reasonable match
                if len(top_indices) > 0 and top_scores[0] > SIMILARITY_THRESHOLD:
                    # Get the top chunks and their metadata
                    top_chunks = [chunks[i] for i in top_indices if similarities[i] > SIMILARITY_THRESHOLD]
                    top_metadata = [chunk_metadata[i] if i < len(chunk_metadata) else {} for i in top_indices if similarities[i] > SIMILARITY_THRESHOLD]
                    
                    # Format snippets with page and section info when available
                    snippets = []
                    for i, chunk in enumerate(top_chunks):
                        if i >= 3:  # Limit to 3 snippets
                            break
                            
                        meta = top_metadata[i] if i < len(top_metadata) else {}
                        page_info = f" (Page {meta.get('page')})" if meta.get('page') else ""
                        section_info = f" - {meta.get('section')}" if meta.get('section') else ""
                        
                        # Add context marker
                        if page_info or section_info:
                            snippet = f"{page_info}{section_info}: {chunk}"
                        else:
                            snippet = chunk
                            
                        snippets.append(snippet)
                    
                    # Create result entry
                    results.append({
                        "document_id": doc_id,
                        "title": doc["title"],
                        "agent": doc["agent"],
                        "type": doc["type"],
                        "snippets": snippets,
                        "score": float(top_scores[0])  # Convert to float for JSON serialization
                    })
            
            # Sort by score and limit results
            results.sort(key=lambda x: x["score"], reverse=True)
            
            logging.info(f"Semantic search found {len(results)} results for '{query}'")
            return results[:max_results]
            
        except Exception as e:
            logging.error(f"Error in semantic search: {str(e)}")
            return []
    
    def _find_snippets(self, text: str, query: str, context_size: int = 150) -> List[str]:
        """
        Find relevant text snippets containing the query
        
        Args:
            text: Document text
            query: Search query
            context_size: Number of characters to include before and after the match
            
        Returns:
            List of relevant snippets
        """
        snippets = []
        query_lower = query.lower()
        text_lower = text.lower()
        
        start = 0
        while start < len(text_lower):
            pos = text_lower.find(query_lower, start)
            if pos == -1:
                break
                
            # Get context around the match
            snippet_start = max(0, pos - context_size)
            snippet_end = min(len(text), pos + len(query) + context_size)
            
            # Extract the snippet
            snippet = text[snippet_start:snippet_end]
            
            # Add ellipsis if clipped
            if snippet_start > 0:
                snippet = "..." + snippet
            if snippet_end < len(text):
                snippet = snippet + "..."
                
            snippets.append(snippet)
            start = pos + len(query)
            
        return snippets
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document from the store
        
        Args:
            document_id: Document ID
            
        Returns:
            True if successful, False otherwise
        """
        if document_id not in self.document_data:
            logging.error(f"Document not found: {document_id}")
            return False
            
        try:
            # Get file paths
            doc = self.document_data[document_id]
            text_path = doc["text_file"]
            
            # Delete files
            if os.path.exists(text_path):
                os.remove(text_path)
                
            # Remove from vector DB if it exists
            if document_id in self.vector_db:
                del self.vector_db[document_id]
                
            # Remove from index
            del self.document_data[document_id]
            
            # Save index
            self._save_index()
            
            logging.info(f"Successfully deleted document: {document_id}")
            return True
        except Exception as e:
            logging.error(f"Error deleting document: {str(e)}")
            return False
    
    def get_embedding_stats(self) -> Dict:
        """
        Get statistics about the vector database
        
        Returns:
            Dictionary with statistics
        """
        if not self.enable_semantic_search:
            return {"enabled": False}
        
        stats = {
            "enabled": True,
            "model": EMBEDDING_MODEL,
            "documents_with_embeddings": len(self.vector_db),
            "total_chunks": sum(len(data["chunks"]) for data in self.vector_db.values()) if self.vector_db else 0,
            "documents": {}
        }
        
        # Get per-document stats
        for doc_id, data in self.vector_db.items():
            if doc_id in self.document_data:
                doc_title = self.document_data[doc_id]["title"]
                stats["documents"][doc_title] = {
                    "chunks": len(data["chunks"]),
                    "embedding_size": data["embeddings"].shape[1] if len(data["embeddings"]) > 0 else 0
                }
        
        return stats

def get_document_context_for_agent(document_store: DocumentStore, agent_name: str, topic: str) -> str:
    """
    Generate a context string from documents relevant to the agent and topic
    
    Args:
        document_store: DocumentStore instance
        agent_name: Agent name to filter documents
        topic: Debate topic to search for relevant context
        
    Returns:
        Formatted context string with relevant document snippets
    """
    # Search for documents relevant to the topic
    search_results = document_store.search_documents(
        query=topic,
        agent_name=agent_name,
        max_results=5
    )
    
    if not search_results:
        return f"No relevant documents found for {agent_name} on topic: {topic}"
    
    # Format the context string
    context_parts = [f"Relevant document snippets for {agent_name} on topic: {topic}\n"]
    
    for result in search_results:
        context_parts.append(f"Document: {result['title']} ({result['type']})")
        for i, snippet in enumerate(result['snippets']):
            # Truncate long snippets
            if len(snippet) > 500:
                snippet = snippet[:500] + "..."
            context_parts.append(f"Snippet {i+1}: {snippet}\n")
    
    return "\n".join(context_parts)

def get_document_context_for_prompt(document_store: DocumentStore, 
                                  agent_name: str, 
                                  last_message: str,
                                  topic: str) -> str:
    """
    Generate a context string for an agent's prompt based on relevant documents
    
    Args:
        document_store: DocumentStore instance
        agent_name: Agent name to filter documents
        last_message: Last message from another agent to provide context
        topic: Debate topic
        
    Returns:
        Formatted context string with relevant document snippets
    """
    # Combine topic and last message for better search context
    search_query = f"{topic} {last_message[:100]}"
    
    # Search for documents relevant to the combined query
    search_results = document_store.search_documents(
        query=search_query,
        agent_name=agent_name,
        max_results=3
    )
    
    if not search_results:
        return ""
    
    # Format the context string
    context_parts = [
        "Based on your policy documents, consider these relevant points when formulating your response:"
    ]
    
    for result in search_results:
        for snippet in result['snippets'][:2]:  # Limit to 2 snippets per document
            # Clean and format the snippet
            clean_snippet = re.sub(r'\s+', ' ', snippet).strip()
            if len(clean_snippet) > 300:
                clean_snippet = clean_snippet[:300] + "..."
            
            context_parts.append(f"• {clean_snippet} (Source: {result['title']})")
    
    return "\n".join(context_parts)


# Example usage in a standalone script
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test the document store
    store = DocumentStore()
    
    # Command-line interface for testing
    import argparse
    
    parser = argparse.ArgumentParser(description='Document Retrieval System for AI Debate')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Upload command
    upload_parser = subparsers.add_parser('upload', help='Upload a document')
    upload_parser.add_argument('--file', required=True, help='Path to PDF file')
    upload_parser.add_argument('--agent', required=True, 
                             choices=['United_States', 'European_Union', 'Peoples_Republic_of_China'],
                             help='Agent this document belongs to')
    upload_parser.add_argument('--type', required=True, help='Document type (e.g., regulation, strategy)')
    upload_parser.add_argument('--title', help='Document title')
    upload_parser.add_argument('--desc', help='Document description')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List documents')
    list_parser.add_argument('--agent', help='Filter by agent')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search documents')
    search_parser.add_argument('--query', required=True, help='Search query')
    search_parser.add_argument('--agent', help='Filter by agent')
    search_parser.add_argument('--type', help='Filter by document type')
    search_parser.add_argument('--max', type=int, default=5, help='Maximum results')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a document')
    delete_parser.add_argument('--id', required=True, help='Document ID')
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Get document text')
    get_parser.add_argument('--id', required=True, help='Document ID')
    
    # Add status command to show semantic search info
    status_parser = subparsers.add_parser('status', help='Show semantic search status')
    
    # Parse arguments
    args = parser.parse_args()
    
    if args.command == 'upload':
        doc_id = store.upload_document(
            file_path=args.file,
            agent_name=args.agent,
            document_type=args.type,
            title=args.title,
            description=args.desc
        )
        if doc_id:
            print(f"Document uploaded successfully. ID: {doc_id}")
        else:
            print("Failed to upload document")
    
    elif args.command == 'list':
        docs = store.get_document_list(args.agent)
        print(f"Found {len(docs)} documents:")
        for doc in docs:
            print(f"{doc['id']} - {doc['title']} ({doc['agent']}, {doc['type']})")
    
    elif args.command == 'search':
        results = store.search_documents(
            query=args.query,
            agent_name=args.agent,
            document_type=args.type,
            max_results=args.max
        )
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results):
            print(f"{i+1}. {result['title']} ({result['agent']}, {result['type']}, score: {result['score']:.2f})")
            for j, snippet in enumerate(result['snippets']):
                print(f"   Snippet {j+1}: {snippet[:100]}...")
            print()
    
    elif args.command == 'delete':
        if store.delete_document(args.id):
            print(f"Document {args.id} deleted successfully")
        else:
            print(f"Failed to delete document {args.id}")
    
    elif args.command == 'get':
        text = store.get_document_text(args.id)
        if text:
            print(f"Document text ({len(text)} characters):")
            print(text[:500] + "..." if len(text) > 500 else text)
        else:
            print(f"Failed to get document {args.id}")
    
    elif args.command == 'status':
        stats = store.get_embedding_stats()
        if stats["enabled"]:
            print(f"Semantic search is ENABLED")
            print(f"Using model: {stats['model']}")
            print(f"Documents with embeddings: {stats['documents_with_embeddings']}")
            print(f"Total text chunks indexed: {stats['total_chunks']}")
            
            if stats["documents"]:
                print("\nDocument details:")
                for title, doc_stats in stats["documents"].items():
                    print(f"  {title}: {doc_stats['chunks']} chunks, {doc_stats['embedding_size']} dimensions")
        else:
            print("Semantic search is DISABLED")
            print("Enable it by setting ENABLE_SEMANTIC_SEARCH = True at the top of document_retrieval.py")
    
    else:
        parser.print_help() 