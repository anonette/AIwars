import os
import logging
import re
from typing import List, Dict, Optional
from document_retrieval import DocumentStore, get_document_context_for_prompt
from debate_system import DebateAgent

class DocumentEnabledDebateAgent(DebateAgent):
    """Extension of DebateAgent with document retrieval capabilities"""
    
    def __init__(self, name: str, personality: str, agent_config_key: str, config: dict = None, 
                document_store: Optional[DocumentStore] = None):
        """
        Initialize a document-enabled debate agent
        
        Args:
            name: Agent name
            personality: Agent personality description
            agent_config_key: Key for the agent in the config
            config: Overall debate config
            document_store: DocumentStore instance for retrieving relevant documents
        """
        super().__init__(name, personality, agent_config_key, config)
        
        # Initialize document store if not provided
        if document_store is None:
            self.document_store = DocumentStore()
        else:
            self.document_store = document_store
        
        # Track document usage for transparency
        self.last_used_documents = []
            
        logging.info(f"Initialized document-enabled agent {name}")
    
    async def generate_response(self, context: str, last_message: str, debate_prompt: str = None) -> str:
        """
        Generate a response with document-augmented context
        
        Args:
            context: Conversation context
            last_message: Last message in the conversation
            debate_prompt: Optional debate prompt
            
        Returns:
            Generated response
        """
        try:
            # Reset document tracking
            self.last_used_documents = []
            
            # Extract topic from context
            topic = self._extract_topic(context)
            
            # Get relevant document context
            doc_context, used_documents = self._get_document_context_with_tracking(
                self.name,
                last_message,
                topic
            )
            
            # Store the documents used for this response
            self.last_used_documents = used_documents
            
            # Augment the agent's personality with relevant document context
            augmented_personality = self.personality
            if doc_context:
                augmented_personality = f"{self.personality}\n\n{doc_context}"
            
            # Temporarily set the augmented personality
            original_personality = self.personality
            self.personality = augmented_personality
            
            # Call the parent class's generate_response method
            response = await super().generate_response(context, last_message, debate_prompt)
            
            # Restore the original personality
            self.personality = original_personality
            
            # Add document citations if any documents were used
            if self.last_used_documents and not response.endswith("]"):
                citations = self._format_citations()
                response = f"{response}\n\n{citations}"
            
            return response
        except Exception as e:
            logging.error(f"Error generating document-augmented response: {str(e)}")
            return await super().generate_response(context, last_message, debate_prompt)
    
    def _get_document_context_with_tracking(self, agent_name: str, last_message: str, topic: str) -> tuple:
        """
        Get document context with tracking of which documents were used
        
        Args:
            agent_name: Agent name
            last_message: Last message
            topic: Debate topic
            
        Returns:
            Tuple of (document_context, used_documents)
        """
        used_documents = []
        
        # Combine topic and last message for better search context
        search_query = f"{topic} {last_message[:100]}"
        
        # Search for documents relevant to the combined query
        search_results = self.document_store.search_documents(
            query=search_query,
            agent_name=agent_name,
            max_results=3
        )
        
        if not search_results:
            return "", used_documents
        
        # Format the context string
        context_parts = [
            "Based on your policy documents, consider these relevant points when formulating your response:"
        ]
        
        for result in search_results:
            # Extract page numbers from snippets if available
            page_numbers = []
            for snippet in result['snippets']:
                page_match = re.search(r"--- Page (\d+) ---", snippet)
                if page_match:
                    page_numbers.append(page_match.group(1))
            
            # Get a representative quote from the first snippet
            representative_quote = ""
            if result['snippets']:
                # Clean up the snippet to get a good quote
                clean_snippet = result['snippets'][0].replace("\n", " ").strip()
                # Remove page markers
                clean_snippet = re.sub(r"--- Page \d+ ---", "", clean_snippet)
                # Get a short, representative quote
                if len(clean_snippet) > 50:
                    words = clean_snippet.split()
                    if len(words) > 10:
                        representative_quote = " ".join(words[:10]) + "..."
                    else:
                        representative_quote = clean_snippet
                else:
                    representative_quote = clean_snippet
            
            # Identify document section if possible
            section = "unspecified section"
            for snippet in result['snippets']:
                # Try to identify section headers
                section_match = re.search(r"([A-Z][A-Z\s]+:)|(\bI{1,3}\.|\bIV\.|\bV\.|\bVI\.|\bVII\.|\bVIII\.|\bIX\.|\bX\.)", snippet)
                if section_match:
                    potential_section = section_match.group(0)
                    if len(potential_section) > 3 and len(potential_section) < 50:
                        section = potential_section
                        break
            
            # Track which documents were used with more details
            used_documents.append({
                "title": result['title'],
                "type": result['type'],
                "score": result['score'],
                "pages": page_numbers,
                "section": section,
                "quote": representative_quote
            })
            
            for snippet in result['snippets'][:2]:  # Limit to 2 snippets per document
                # Clean and format the snippet
                clean_snippet = snippet.replace("\n", " ").strip()
                # Remove page markers for cleaner presentation
                clean_snippet = re.sub(r"--- Page \d+ ---", "", clean_snippet)
                if len(clean_snippet) > 300:
                    clean_snippet = clean_snippet[:300] + "..."
                
                context_parts.append(f"• {clean_snippet} (Source: {result['title']})")
        
        return "\n".join(context_parts), used_documents
    
    def _format_citations(self) -> str:
        """Format document citations for inclusion in response with concrete details"""
        if not self.last_used_documents:
            return ""
            
        citations = "_Sources referenced:_"
        for doc in self.last_used_documents:
            # Format page numbers if available
            page_str = ""
            if doc.get('pages') and len(doc.get('pages')) > 0:
                pages = doc.get('pages')
                if len(pages) == 1:
                    page_str = f", p. {pages[0]}"
                else:
                    page_str = f", pp. {'-'.join(pages[:2])}"
            
            # Add section information if available
            section_str = ""
            if doc.get('section') and doc.get('section') != "unspecified section":
                section_str = f", {doc.get('section')}"
            
            # Add the quote if available
            quote_str = ""
            if doc.get('quote'):
                quote_str = f": \"{doc.get('quote')}\""
            
            citations += f" '{doc['title']}' ({doc['type']}{page_str}{section_str}){quote_str},"
        
        # Remove trailing comma and add period
        citations = citations.rstrip(",") + "."
        return citations
    
    def _extract_topic(self, context: str) -> str:
        """
        Extract the debate topic from context
        
        Args:
            context: Conversation context
            
        Returns:
            Extracted topic or empty string if not found
        """
        try:
            # Try to extract from the first line that contains "Topic:"
            lines = context.split('\n')
            for line in lines:
                if "Topic:" in line:
                    return line.split("Topic:", 1)[1].strip()
            
            # If not found, return the first line as a fallback
            if lines:
                return lines[0].strip()
            
            return ""
        except Exception as e:
            logging.error(f"Error extracting topic: {str(e)}")
            return ""
    
    async def generate_conclusion(self, context: str) -> str:
        """
        Generate a document-augmented conclusion
        
        Args:
            context: Conversation context
            
        Returns:
            Generated conclusion
        """
        try:
            # Reset document tracking
            self.last_used_documents = []
            
            # Extract topic
            topic = self._extract_topic(context)
            
            # Get comprehensive document context for conclusion and track documents
            doc_context, used_documents = self._get_comprehensive_context_with_tracking(topic)
            
            # Store the documents used for this conclusion
            self.last_used_documents = used_documents
            
            # Format specific document citations for inclusion in the prompt
            citation_examples = self._format_citation_examples()
            
            # Augment the agent's personality with document context and citation examples
            augmented_personality = self.personality
            if doc_context:
                augmented_personality = f"{self.personality}\n\n{doc_context}\n\n{citation_examples}"
            
            # Temporarily set the augmented personality
            original_personality = self.personality
            self.personality = augmented_personality
            
            # Call the parent class's generate_conclusion method
            conclusion = await super().generate_conclusion(context)
            
            # Restore the original personality
            self.personality = original_personality
            
            # If citations aren't already included (rare case), add footnote citations
            if self.last_used_documents and "(" not in conclusion and not conclusion.endswith("]"):
                citations = self._format_conclusion_citations()
                conclusion = f"{conclusion}\n\n{citations}"
            
            return conclusion
        except Exception as e:
            logging.error(f"Error generating document-augmented conclusion: {str(e)}")
            return await super().generate_conclusion(context)
    
    def _get_comprehensive_context_with_tracking(self, topic: str) -> tuple:
        """
        Get comprehensive document context with tracking of which documents were used
        
        Args:
            topic: Debate topic
            
        Returns:
            Tuple of (document_context, used_documents)
        """
        used_documents = []
        
        try:
            # Get all relevant documents for the agent
            docs = self.document_store.get_document_list(self.name)
            if not docs:
                return "", used_documents
            
            # Search for relevant documents based on topic
            search_results = self.document_store.search_documents(
                query=topic,
                agent_name=self.name,
                max_results=5
            )
            
            if not search_results:
                return "", used_documents
            
            # Track which documents were used with enhanced details
            for result in search_results:
                # Extract page numbers from snippets if available
                page_numbers = []
                for snippet in result['snippets']:
                    page_match = re.search(r"--- Page (\d+) ---", snippet)
                    if page_match:
                        page_numbers.append(page_match.group(1))
                
                # Get multiple representative quotes (up to 3)
                representative_quotes = []
                for snippet in result['snippets'][:3]:
                    # Clean up the snippet to get a good quote
                    clean_snippet = snippet.replace("\n", " ").strip()
                    # Remove page markers
                    clean_snippet = re.sub(r"--- Page \d+ ---", "", clean_snippet)
                    # Get a short, representative quote
                    if len(clean_snippet) > 50:
                        # Find a complete sentence if possible
                        sentences = re.split(r'(?<=[.!?])\s+', clean_snippet)
                        if sentences and len(sentences[0]) >= 20:
                            representative_quotes.append(sentences[0])
                        else:
                            words = clean_snippet.split()
                            if len(words) > 10:
                                representative_quotes.append(" ".join(words[:10]) + "...")
                            else:
                                representative_quotes.append(clean_snippet)
                    else:
                        representative_quotes.append(clean_snippet)
                
                # Identify document section if possible
                section = "unspecified section"
                for snippet in result['snippets']:
                    # Try to identify section headers
                    section_match = re.search(r"([A-Z][A-Z\s]+:)|(\bI{1,3}\.|\bIV\.|\bV\.|\bVI\.|\bVII\.|\bVIII\.|\bIX\.|\bX\.)", snippet)
                    if section_match:
                        potential_section = section_match.group(0)
                        if len(potential_section) > 3 and len(potential_section) < 50:
                            section = potential_section
                            break
                
                used_documents.append({
                    "title": result['title'],
                    "type": result['type'],
                    "score": result['score'],
                    "pages": page_numbers,
                    "section": section,
                    "quote": representative_quotes[0] if representative_quotes else "",
                    "quotes": representative_quotes
                })
            
            # Format comprehensive context
            context_parts = [
                "Based on your official policy documents, consider these key points for your final position:"
            ]
            
            for result in search_results:
                # Add document title, type, and page information
                page_info = ""
                for snippet in result['snippets']:
                    page_match = re.search(r"--- Page (\d+) ---", snippet)
                    if page_match:
                        page_info = f" (p. {page_match.group(1)})"
                        break
                
                context_parts.append(f"\nFrom {result['title']} ({result['type']}){page_info}:")
                
                # Add snippets
                for snippet in result['snippets'][:3]:  # Up to 3 snippets per document
                    # Clean and format snippet
                    clean_snippet = snippet.replace("\n", " ").strip()
                    # Remove page markers
                    clean_snippet = re.sub(r"--- Page \d+ ---", "", clean_snippet)
                    if len(clean_snippet) > 400:
                        clean_snippet = clean_snippet[:400] + "..."
                    
                    context_parts.append(f"• {clean_snippet}")
            
            return "\n".join(context_parts), used_documents
        except Exception as e:
            logging.error(f"Error getting comprehensive context: {str(e)}")
            return "", used_documents
    
    def _format_conclusion_citations(self) -> str:
        """Format document citations for conclusion with concrete details"""
        if not self.last_used_documents:
            return ""
            
        citations = "**References:**"
        for i, doc in enumerate(self.last_used_documents):
            # Format page numbers if available
            page_str = ""
            if doc.get('pages') and len(doc.get('pages')) > 0:
                pages = doc.get('pages')
                if len(pages) == 1:
                    page_str = f", page {pages[0]}"
                else:
                    page_str = f", pages {'-'.join(pages[:2])}"
            
            # Add section information if available
            section_str = ""
            if doc.get('section') and doc.get('section') != "unspecified section":
                section_str = f", {doc.get('section')}"
            
            # Add representative quote if available
            quote_str = ""
            if doc.get('quote'):
                quote_str = f"\n   \"{doc.get('quote')}\""
            
            citations += f"\n{i+1}. {doc['title']} ({doc['type']}{page_str}{section_str}){quote_str}"
        
        return citations
    
    def _format_citation_examples(self) -> str:
        """Create example citations from actual documents for the LLM to follow"""
        if not self.last_used_documents:
            return ""
        
        citation_examples = "Here are specific references from your policy documents that you should cite in your position paper:\n\n"
        
        for i, doc in enumerate(self.last_used_documents):
            if i >= 3:  # Limit to 3 examples
                break
            
            title = doc.get('title', 'Policy Document')
            doc_type = doc.get('type', 'document')
            page = doc.get('pages', ['1'])[0] if doc.get('pages') and len(doc.get('pages')) > 0 else '1'
            quote = doc.get('quote', 'AI governance must balance innovation with security.')
            
            citation_examples += f"{i+1}. From '{title}' ({doc_type}, page {page}): \"{quote}\"\n"
        
        citation_examples += "\nIncorporate these references and others from your policy documents directly into your position paper using the format: \"[quote]\" (Document Title, page X)."
        
        return citation_examples
    
    def get_last_used_documents(self) -> List[Dict]:
        """Get the list of documents used in the last response"""
        return self.last_used_documents

def create_document_enabled_agents(config: dict, document_store: Optional[DocumentStore] = None) -> List[DocumentEnabledDebateAgent]:
    """
    Create document-enabled debate agents from config
    
    Args:
        config: Debate config dictionary
        document_store: Optional document store to use for all agents
        
    Returns:
        List of DocumentEnabledDebateAgent instances
    """
    if document_store is None:
        document_store = DocumentStore()
    
    agents = []
    agent_configs = config.get('agents', {})
    
    for agent_key, agent_config in agent_configs.items():
        try:
            agent = DocumentEnabledDebateAgent(
                name=agent_config['name'],
                personality=agent_config['personality'],
                agent_config_key=agent_key,
                config=config,
                document_store=document_store
            )
            agents.append(agent)
            logging.info(f"Created document-enabled agent: {agent.name}")
        except Exception as e:
            logging.error(f"Error creating document-enabled agent {agent_key}: {str(e)}")
    
    return agents

# Example of how to use this in the main application
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    from yaml import safe_load
    
    # Load config
    try:
        with open('config.yaml', 'r') as f:
            config = safe_load(f)
    except Exception as e:
        logging.error(f"Error loading config: {str(e)}")
        config = {}
    
    # Create document store
    document_store = DocumentStore()
    
    # Create document-enabled agents
    agents = create_document_enabled_agents(config, document_store)
    
    # Print agents
    for agent in agents:
        print(f"Created agent: {agent.name}")
        
    print("\nTo use these agents with documents, integrate this module with your debate application.")
    print("Example:")
    print("1. Import DocumentEnabledDebateAgent and create_document_enabled_agents")
    print("2. Replace DebateAgent instances with DocumentEnabledDebateAgent")
    print("3. Upload documents using the document_retrieval.py command-line interface")
    print("\nRun 'python document_retrieval.py upload --help' for more information on uploading documents.") 