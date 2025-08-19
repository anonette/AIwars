#!/usr/bin/env python3
"""
Batch upload script for adding all TEXTS/pdfs documents to the RAG system
Organizes documents by country/agent for better search and retrieval
"""

import os
import sys
from document_retrieval import DocumentStore

# Document mapping: filename -> (agent, document_type, title, description)
DOCUMENT_MAPPINGS = {
    # China documents
    "China2017red.pdf": ("Peoples_Republic_of_China", "policy", "China AI Strategy 2017", "China's early AI development strategy document"),
    "China2022.pdf": ("Peoples_Republic_of_China", "policy", "China AI Strategy 2022", "Updated Chinese AI governance and development framework"),
    "China2023.pdf": ("Peoples_Republic_of_China", "policy", "China AI Strategy 2023", "Latest Chinese AI policy developments"),
    "China2025.pdf": ("Peoples_Republic_of_China", "strategy", "China AI Vision 2025", "China's long-term AI development roadmap"),
    "ChinaAll.pdf": ("Peoples_Republic_of_China", "comprehensive", "China AI Comprehensive Framework", "Complete overview of Chinese AI policies and strategies"),
    "ChinagenAI.pdf": ("Peoples_Republic_of_China", "regulation", "China Generative AI Regulations", "Chinese regulatory framework for generative AI systems"),
    "ChinaReg.pdf": ("Peoples_Republic_of_China", "regulation", "China AI Regulations", "Chinese AI regulatory framework and compliance requirements"),
    "ChinaSummary.pdf": ("Peoples_Republic_of_China", "summary", "China AI Policy Summary", "Executive summary of Chinese AI governance approach"),
    
    # EU documents
    "EUAIAct2025.pdf": ("European_Union", "legislation", "EU AI Act 2025", "European Union's comprehensive AI regulation framework"),
    "EUAICloud.pdf": ("European_Union", "infrastructure", "EU AI Cloud Initiative", "European cloud computing infrastructure for AI development"),
    "EUAIcontAnnex.pdf": ("European_Union", "regulation", "EU AI Act Annexes", "Technical annexes and implementation details for EU AI Act"),
    "EUAIcontinent.pdf": ("European_Union", "strategy", "EU AI Continent Strategy", "Europe's vision for AI leadership and technological sovereignty"),
    "EUAIScience.pdf": ("European_Union", "research", "EU AI Science Framework", "European approach to AI research and development"),
    "EUCOE.pdf": ("European_Union", "ethics", "EU AI Ethics Guidelines", "European guidelines for ethical AI development and deployment"),
    "EUdoc.pdf": ("European_Union", "policy", "EU AI Policy Document", "General EU policy framework for artificial intelligence"),
    "EUReg2023.pdf": ("European_Union", "regulation", "EU AI Regulation 2023", "European regulatory updates for AI governance"),
    
    # US documents
    "USANIST.pdf": ("United_States", "standards", "NIST AI Standards", "US National Institute of Standards and Technology AI framework"),
    "USChipAct.pdf": ("United_States", "legislation", "US CHIPS and Science Act", "American semiconductor and AI infrastructure investment"),
    "UScopyright.pdf": ("United_States", "regulation", "US AI Copyright Framework", "US approach to intellectual property in AI systems"),
    "USframework.pdf": ("United_States", "framework", "US AI Governance Framework", "Comprehensive US approach to AI regulation and development"),
    
    # Global/Reference documents - assign to all agents
    "GlobalAI.pdf": ("United_States", "analysis", "Global AI Governance Analysis", "International perspective on AI governance challenges"),
    "key_terms_for_ai_governance.pdf": ("European_Union", "reference", "Key Terms for AI Governance", "Glossary and definitions for AI policy terms"),
    "The Language of Trustworthy AI_ An In-Depth Glossary of Terms (updated August 4, 2024).pdf": ("European_Union", "reference", "Trustworthy AI Glossary 2024", "Updated terminology and definitions for trustworthy AI systems")
}

def upload_documents():
    """Upload all documents from TEXTS/pdfs to the document store"""
    
    # Initialize document store
    print("Initializing document store...")
    doc_store = DocumentStore()
    
    # Base directory
    pdfs_dir = "TEXTS/pdfs"
    
    if not os.path.exists(pdfs_dir):
        print(f"Error: Directory {pdfs_dir} not found!")
        return False
    
    successful_uploads = 0
    failed_uploads = []
    
    print(f"Found {len(DOCUMENT_MAPPINGS)} documents to upload...")
    print("=" * 60)
    
    for filename, (agent, doc_type, title, description) in DOCUMENT_MAPPINGS.items():
        file_path = os.path.join(pdfs_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"⚠️  File not found: {filename}")
            failed_uploads.append(f"{filename} - File not found")
            continue
        
        print(f"📄 Uploading: {filename}")
        print(f"   Agent: {agent}")
        print(f"   Type: {doc_type}")
        print(f"   Title: {title}")
        
        try:
            doc_id = doc_store.upload_document(
                file_path=file_path,
                agent_name=agent,
                document_type=doc_type,
                title=title,
                description=description
            )
            
            if doc_id:
                print(f"✅ Successfully uploaded: {doc_id}")
                successful_uploads += 1
            else:
                print(f"❌ Failed to upload: {filename}")
                failed_uploads.append(f"{filename} - Upload failed")
                
        except Exception as e:
            print(f"❌ Error uploading {filename}: {str(e)}")
            failed_uploads.append(f"{filename} - Error: {str(e)}")
        
        print("-" * 40)
    
    # Summary
    print("=" * 60)
    print("UPLOAD SUMMARY")
    print("=" * 60)
    print(f"✅ Successful uploads: {successful_uploads}")
    print(f"❌ Failed uploads: {len(failed_uploads)}")
    
    if failed_uploads:
        print("\nFailed uploads:")
        for failure in failed_uploads:
            print(f"  - {failure}")
    
    print(f"\nTotal documents in store: {len(doc_store.document_data)}")
    
    # Show document count by agent
    agent_counts = {}
    for doc in doc_store.document_data.values():
        agent = doc['agent']
        agent_counts[agent] = agent_counts.get(agent, 0) + 1
    
    print("\nDocuments by agent:")
    for agent, count in sorted(agent_counts.items()):
        print(f"  - {agent}: {count} documents")
    
    return successful_uploads > 0

if __name__ == "__main__":
    print("🚀 Starting batch document upload...")
    print("This will add all PDF documents from TEXTS/pdfs to the RAG system")
    print()
    
    success = upload_documents()
    
    if success:
        print("\n🎉 Batch upload completed!")
        print("You can now run the Streamlit app with enhanced RAG capabilities.")
    else:
        print("\n💥 Batch upload failed!")
        sys.exit(1)
