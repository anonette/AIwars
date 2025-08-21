#!/usr/bin/env python3
"""
Upload theoretical texts from TEXTS/ directory to the document store
This ensures theoretical works like Ezrahi's are available for retrieval
"""

import os
import sys
from document_retrieval import DocumentStore
from pathlib import Path

# Theoretical text mappings
THEORETICAL_MAPPINGS = {
    # Core theoretical works - assign to all agents for theoretical analysis
    "Yaron Ezrahi - Imagined Democracies _ Necessary Political Fictions-Cambridge University Press (2012).pdf": {
        "agents": ["United_States", "European_Union", "Peoples_Republic_of_China"],
        "type": "theoretical_framework",
        "title": "Imagined Democracies: Necessary Political Fictions",
        "description": "Ezrahi's framework on political imaginaries and necessary fictions in democratic governance"
    },
    "Michel Foucault - Society Must Be Defended_ Lectures at the College de France, 1975-76-Picador (2003).pdf": {
        "agents": ["United_States", "European_Union", "Peoples_Republic_of_China"],
        "type": "theoretical_framework",
        "title": "Society Must Be Defended",
        "description": "Foucault's analysis of power, sovereignty, and biopolitics"
    },
    "Mark Coeckelbergh - The Political Philosophy of AI_ An Introduction-Polity (2022).pdf": {
        "agents": ["United_States", "European_Union", "Peoples_Republic_of_China"],
        "type": "theoretical_framework",
        "title": "The Political Philosophy of AI",
        "description": "Coeckelbergh's framework for understanding AI governance and politics"
    },
    "Mathias Risse - Political Theory of the Digital Age_ Where Artificial Intelligence Might Take Us-Cambridge University Press (2023).pdf": {
        "agents": ["United_States", "European_Union", "Peoples_Republic_of_China"],
        "type": "theoretical_framework",
        "title": "Political Theory of the Digital Age",
        "description": "Risse's analysis of digital governance and algorithmic authority"
    },
    "Homi K. Bhabha - The Location of Culture (1994).djvu": {
        "agents": ["United_States", "European_Union", "Peoples_Republic_of_China"],
        "type": "theoretical_framework",
        "title": "The Location of Culture",
        "description": "Bhabha's postcolonial theory on cultural positioning and hybridity"
    },
    "Roland Barthes, Richard Howard - The Rustle of Language-University of California Press (1989).pdf": {
        "agents": ["United_States", "European_Union", "Peoples_Republic_of_China"],
        "type": "theoretical_framework",
        "title": "The Rustle of Language",
        "description": "Barthes' semiotics and analysis of political discourse"
    }
}

def upload_theoretical_texts():
    """Upload theoretical texts to the document store"""
    
    # Initialize document store
    print("Initializing document store...")
    doc_store = DocumentStore()
    
    # Path to TEXTS directory
    texts_path = Path("TEXTS")
    if not texts_path.exists():
        print(f"Error: TEXTS directory not found at {texts_path}")
        return
    
    # Track uploads
    successful_uploads = 0
    failed_uploads = 0
    
    # Process each theoretical text
    for filename, metadata in THEORETICAL_MAPPINGS.items():
        file_path = texts_path / filename
        
        if not file_path.exists():
            print(f"Warning: File not found: {filename}")
            # Try without .djvu extension (in case it was converted to PDF)
            if filename.endswith('.djvu'):
                pdf_filename = filename.replace('.djvu', '.pdf')
                file_path = texts_path / pdf_filename
                if not file_path.exists():
                    failed_uploads += 1
                    continue
        
        print(f"\nUploading: {metadata['title']}")
        
        # Upload for each agent
        for agent in metadata["agents"]:
            try:
                doc_id = doc_store.upload_document(
                    file_path=str(file_path),
                    agent_name=agent,
                    document_type=metadata["type"],
                    title=metadata["title"],
                    description=metadata["description"]
                )
                
                if doc_id:
                    print(f"  ✓ Uploaded for {agent} (ID: {doc_id})")
                    successful_uploads += 1
                else:
                    print(f"  ✗ Failed to upload for {agent}")
                    failed_uploads += 1
                    
            except Exception as e:
                print(f"  ✗ Error uploading for {agent}: {str(e)}")
                failed_uploads += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Upload Summary:")
    print(f"  Successful uploads: {successful_uploads}")
    print(f"  Failed uploads: {failed_uploads}")
    print(f"  Total theoretical texts: {len(THEORETICAL_MAPPINGS)}")
    print(f"{'='*60}")

if __name__ == "__main__":
    upload_theoretical_texts()