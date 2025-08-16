#!/usr/bin/env python3
"""
Script to load documents from TEXTS directory into the agent document store.
This enables the RAG system to access these documents during debates.
"""

import os
import sys
import logging
from pathlib import Path
from document_retrieval import DocumentStore
import shutil
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Document mappings - which documents are relevant for which agent
AGENT_DOCUMENT_MAPPINGS = {
    "United_States": [
        "CHIPS Act",
        "Framework for AI Diffusion", 
        "EAR Control",
        "Foreign Direct Product Rule",
        "CSET-Decoding-Intentions",
        "ai-cold-war-analysis-usa-prc.pdf",
        "The AI Cold War With China That Threatens Us All",
        "updated-ai-programs-json.json",
        "ai-containment-json.json",
        "ChipWars.pdf",
        "Comprehensive AI Containment Program Funding Analysis.pdf"
    ],
    "Peoples_Republic_of_China": [
        "China",
        "Algorithm Regulations",
        "ai-cold-war-analysis-usa-prc.pdf",
        "The AI Cold War With China That Threatens Us All",
        "CSET-Decoding-Intentions",
        "ChipWars.pdf"
    ],
    "European_Union": [
        "European",
        "EU",
        "Copyright__Third_Draft",
        "Safety_and_Security__Third_Draft",
        "Transparency__Third_Draft",
        "Democracy, Theatre and Performance",
        "Ekiert"
    ]
}

def find_matching_files(texts_dir: str, patterns: list) -> list:
    """Find files in TEXTS directory that match the given patterns."""
    matching_files = []
    texts_path = Path(texts_dir)
    
    if not texts_path.exists():
        logging.error(f"TEXTS directory not found: {texts_dir}")
        return matching_files
    
    # Get all files in TEXTS directory
    all_files = []
    for root, dirs, files in os.walk(texts_path):
        # Skip the pdfs subdirectory as it contains duplicates
        if 'pdfs' in root:
            continue
        for file in files:
            if file.endswith(('.pdf', '.txt', '.md', '.json', '.docx')):
                all_files.append(os.path.join(root, file))
    
    # Match files based on patterns
    for file_path in all_files:
        filename = os.path.basename(file_path)
        for pattern in patterns:
            if pattern.lower() in filename.lower():
                matching_files.append(file_path)
                break
    
    return matching_files

def determine_document_type(filename: str) -> str:
    """Determine the document type based on filename."""
    filename_lower = filename.lower()
    
    if 'act' in filename_lower or 'legislation' in filename_lower:
        return 'legislation'
    elif 'framework' in filename_lower or 'strategy' in filename_lower:
        return 'strategy'
    elif 'regulation' in filename_lower or 'rule' in filename_lower:
        return 'regulation'
    elif 'analysis' in filename_lower or 'report' in filename_lower:
        return 'analysis'
    elif 'research' in filename_lower or 'paper' in filename_lower:
        return 'research'
    elif 'policy' in filename_lower:
        return 'policy'
    else:
        return 'document'

def load_documents_for_agents(texts_dir: str = "TEXTS", agent_docs_dir: str = "agent_documents"):
    """Load documents from TEXTS directory into agent document store."""
    
    # Initialize document store
    document_store = DocumentStore(documents_dir=agent_docs_dir)
    
    # Track statistics
    stats = {
        "total_processed": 0,
        "successful": 0,
        "failed": 0,
        "by_agent": {}
    }
    
    # Process documents for each agent
    for agent_name, patterns in AGENT_DOCUMENT_MAPPINGS.items():
        logging.info(f"\nProcessing documents for {agent_name}...")
        stats["by_agent"][agent_name] = {"processed": 0, "successful": 0}
        
        # Find matching files
        matching_files = find_matching_files(texts_dir, patterns)
        logging.info(f"Found {len(matching_files)} matching files for {agent_name}")
        
        # Process each file
        for file_path in matching_files:
            filename = os.path.basename(file_path)
            stats["total_processed"] += 1
            stats["by_agent"][agent_name]["processed"] += 1
            
            # Skip non-PDF files for now (can be extended later)
            if not file_path.lower().endswith('.pdf'):
                logging.warning(f"Skipping non-PDF file: {filename}")
                continue
            
            # Determine document type
            doc_type = determine_document_type(filename)
            
            # Create a clean title
            title = filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
            title = ' '.join(word.capitalize() for word in title.split())
            
            try:
                # Upload document
                logging.info(f"Uploading: {filename} as {doc_type} for {agent_name}")
                doc_id = document_store.upload_document(
                    file_path=file_path,
                    agent_name=agent_name,
                    document_type=doc_type,
                    title=title,
                    description=f"Document from TEXTS directory: {filename}"
                )
                
                if doc_id:
                    stats["successful"] += 1
                    stats["by_agent"][agent_name]["successful"] += 1
                    logging.info(f"✓ Successfully uploaded: {doc_id}")
                else:
                    stats["failed"] += 1
                    logging.error(f"✗ Failed to upload: {filename}")
                    
            except Exception as e:
                stats["failed"] += 1
                logging.error(f"✗ Error uploading {filename}: {str(e)}")
    
    # Print summary
    print("\n" + "="*60)
    print("DOCUMENT LOADING SUMMARY")
    print("="*60)
    print(f"Total files processed: {stats['total_processed']}")
    print(f"Successfully uploaded: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    print("\nBy Agent:")
    for agent, agent_stats in stats["by_agent"].items():
        print(f"  {agent}:")
        print(f"    - Processed: {agent_stats['processed']}")
        print(f"    - Successful: {agent_stats['successful']}")
    print("="*60)
    
    # Check current document index
    if os.path.exists(os.path.join(agent_docs_dir, "document_index.json")):
        with open(os.path.join(agent_docs_dir, "document_index.json"), 'r') as f:
            index = json.load(f)
            print(f"\nTotal documents in index: {len(index)}")
    
    return stats

def main():
    """Main function to run the document loader."""
    print("AI Debate Document Loader")
    print("=" * 60)
    print("This script will load documents from the TEXTS directory")
    print("into the agent document store for RAG-based debates.")
    print("=" * 60)
    
    # Check if TEXTS directory exists
    if not os.path.exists("TEXTS"):
        print("\nERROR: TEXTS directory not found!")
        print("Please ensure you're running this script from the project root directory.")
        sys.exit(1)
    
    # Check if agent_documents directory exists
    if not os.path.exists("agent_documents"):
        print("\nCreating agent_documents directory...")
        os.makedirs("agent_documents")
    
    # Ask for confirmation
    response = input("\nDo you want to proceed with loading documents? (y/n): ")
    if response.lower() != 'y':
        print("Operation cancelled.")
        sys.exit(0)
    
    # Load documents
    print("\nLoading documents...")
    stats = load_documents_for_agents()
    
    if stats["successful"] > 0:
        print("\n✓ Document loading completed successfully!")
        print("The agents can now access these documents during debates.")
    else:
        print("\n✗ No documents were successfully loaded.")
        print("Please check the error messages above.")

if __name__ == "__main__":
    main()