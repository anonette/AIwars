import streamlit as st
import os
import pandas as pd
from document_retrieval import DocumentStore
import tempfile
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize document store
document_store = DocumentStore()

# Set page title and icon
st.set_page_config(
    page_title="AI Debate Document Manager",
    page_icon="📚",
    layout="wide"
)

# CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .upload-section {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 2rem;
    }
    .document-card {
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #e6e6e6;
        margin-bottom: 1rem;
    }
    .success-message {
        color: #0c5460;
        background-color: #d1ecf1;
        border-color: #bee5eb;
        padding: 0.75rem 1.25rem;
        border-radius: 0.25rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("📚 AI Debate Document Manager")
st.markdown("Upload and manage policy documents for debate agents.")

# Sidebar with actions
with st.sidebar:
    st.header("Document Management")
    action = st.radio(
        "Choose an action:",
        ["Upload Documents", "View Documents", "Search Documents", "Delete Documents"]
    )
    
    st.header("About")
    st.info(
        "This tool allows you to manage policy documents for AI debate agents. "
        "Documents are stored permanently and will be accessible to agents during debates."
    )
    
    st.header("Agent Colors")
    st.markdown("🇺🇸 United States - Blue")
    st.markdown("🇪🇺 European Union - Gold")
    st.markdown("🇨🇳 People's Republic of China - Red")

# Upload Documents Interface
if action == "Upload Documents":
    st.header("Upload Policy Documents")
    
    upload_col1, upload_col2 = st.columns([2, 1])
    
    with upload_col1:
        uploaded_files = st.file_uploader(
            "Choose PDF files to upload",
            type="pdf",
            accept_multiple_files=True
        )
    
    with upload_col2:
        agent_name = st.selectbox(
            "Select agent",
            ["United_States", "European_Union", "Peoples_Republic_of_China"],
            format_func=lambda x: x.replace("_", " ")
        )
        
        document_type = st.selectbox(
            "Document type",
            ["policy", "regulation", "strategy", "framework", "whitepaper", "legislation", 
             "report", "standards", "guidance", "research"]
        )
    
    if uploaded_files:
        st.subheader("Files to Upload")
        file_info = []
        
        for i, uploaded_file in enumerate(uploaded_files):
            col1, col2 = st.columns([3, 1])
            with col1:
                title = st.text_input(f"Title for {uploaded_file.name}", 
                                     value=uploaded_file.name.replace(".pdf", ""),
                                     key=f"title_{i}")
                description = st.text_area(f"Description (optional) for {uploaded_file.name}", 
                                          height=100,
                                          key=f"desc_{i}")
            with col2:
                st.write("File info:")
                st.write(f"Size: {uploaded_file.size / 1024:.1f} KB")
                
            file_info.append({
                "file": uploaded_file,
                "title": title,
                "description": description
            })
            
            st.markdown("---")
        
        if st.button("Upload All Documents", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, file_data in enumerate(file_info):
                status_text.text(f"Processing {file_data['file'].name}...")
                
                # Write the uploaded file to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(file_data['file'].getvalue())
                    tmp_file_path = tmp_file.name
                
                try:
                    # Upload the document using DocumentStore
                    doc_id = document_store.upload_document(
                        file_path=tmp_file_path,
                        agent_name=agent_name,
                        document_type=document_type,
                        title=file_data['title'],
                        description=file_data['description']
                    )
                    
                    if doc_id:
                        status_text.success(f"✅ Successfully uploaded: {file_data['title']}")
                    else:
                        status_text.error(f"❌ Failed to upload: {file_data['title']}")
                        
                finally:
                    # Clean up the temporary file
                    os.unlink(tmp_file_path)
                
                # Update progress
                progress_bar.progress((i + 1) / len(file_info))
            
            status_text.text("All documents processed!")
            st.success(f"Successfully uploaded {len(file_info)} documents for {agent_name.replace('_', ' ')}")
            st.balloons()

# View Documents Interface
elif action == "View Documents":
    st.header("View Uploaded Documents")
    
    agent_filter = st.selectbox(
        "Filter by agent",
        ["All", "United_States", "European_Union", "Peoples_Republic_of_China"],
        format_func=lambda x: "All Agents" if x == "All" else x.replace("_", " ")
    )
    
    type_filter = st.selectbox(
        "Filter by document type",
        ["All", "policy", "regulation", "strategy", "framework", "whitepaper", 
         "legislation", "report", "standards", "guidance", "research"]
    )
    
    if agent_filter == "All":
        documents = document_store.get_document_list()
    else:
        documents = document_store.get_document_list(agent_filter)
    
    # Apply type filter
    if type_filter != "All":
        documents = [doc for doc in documents if doc.get('type', '').lower() == type_filter.lower()]
    
    if not documents:
        st.info("No documents found with the selected filters.")
    else:
        # Convert to DataFrame for better display
        df = pd.DataFrame([
            {
                "ID": doc.get("id", ""),
                "Title": doc.get("title", ""),
                "Agent": doc.get("agent", ""),
                "Type": doc.get("type", ""),
                "Pages": doc.get("pages", 0),
                "Upload Date": doc.get("upload_date", ""),
                "Size (chars)": doc.get("char_count", 0)
            }
            for doc in documents
        ])
        
        # Add color-coding by agent
        def color_by_agent(val):
            if "United_States" in val:
                return 'background-color: #d1e6ff'
            elif "European_Union" in val:
                return 'background-color: #fff8d1'
            elif "Peoples_Republic_of_China" in val:
                return 'background-color: #ffd1d1'
            return ''
        
        # Display DataFrame with styling
        st.dataframe(
            df.style.applymap(color_by_agent, subset=['Agent']),
            use_container_width=True
        )
        
        # Display document count
        st.caption(f"Showing {len(documents)} documents")
        
        # Document preview feature
        selected_doc_id = st.selectbox("Select a document to preview:", 
                                     options=[doc.get("id", "") for doc in documents],
                                     format_func=lambda x: next((doc.get("title", "") for doc in documents if doc.get("id", "") == x), x))
        
        if selected_doc_id:
            selected_doc = next((doc for doc in documents if doc.get("id", "") == selected_doc_id), None)
            if selected_doc:
                st.subheader(f"Preview: {selected_doc.get('title', '')}")
                
                doc_text = document_store.get_document_text(selected_doc_id)
                if doc_text:
                    with st.expander("Document Content", expanded=True):
                        st.text_area("Document text (first 5000 characters):", 
                                    value=doc_text[:5000] + ("..." if len(doc_text) > 5000 else ""),
                                    height=400)
                else:
                    st.error("Failed to load document text.")

# Search Documents Interface
elif action == "Search Documents":
    st.header("Search Documents")
    
    search_col1, search_col2 = st.columns([3, 1])
    
    with search_col1:
        search_query = st.text_input("Enter search query")
    
    with search_col2:
        agent_filter = st.selectbox(
            "Filter by agent",
            ["All", "United_States", "European_Union", "Peoples_Republic_of_China"],
            format_func=lambda x: "All Agents" if x == "All" else x.replace("_", " ")
        )
        
        max_results = st.slider("Maximum results", min_value=1, max_value=20, value=5)
    
    if search_query:
        with st.spinner("Searching documents..."):
            results = document_store.search_documents(
                query=search_query,
                agent_name=None if agent_filter == "All" else agent_filter,
                max_results=max_results
            )
        
        if not results:
            st.info(f"No results found for '{search_query}'")
        else:
            st.success(f"Found {len(results)} results for '{search_query}'")
            
            for i, result in enumerate(results):
                with st.container():
                    st.markdown(f"### {i+1}. {result['title']} ({result['agent'].replace('_', ' ')})")
                    st.markdown(f"**Document type:** {result['type']} | **Relevance score:** {result['score']:.2f}")
                    
                    for j, snippet in enumerate(result['snippets']):
                        st.markdown(f"**Snippet {j+1}:**")
                        st.markdown(f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>{snippet}</div>", unsafe_allow_html=True)
                    
                    st.markdown("---")

# Delete Documents Interface
elif action == "Delete Documents":
    st.header("Delete Documents")
    st.warning("⚠️ Deleting documents is permanent and cannot be undone.")
    
    agent_filter = st.selectbox(
        "Filter by agent",
        ["All", "United_States", "European_Union", "Peoples_Republic_of_China"],
        format_func=lambda x: "All Agents" if x == "All" else x.replace("_", " ")
    )
    
    if agent_filter == "All":
        documents = document_store.get_document_list()
    else:
        documents = document_store.get_document_list(agent_filter)
    
    if not documents:
        st.info("No documents found with the selected filter.")
    else:
        # Display documents in a more concise format for deletion
        for doc in documents:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{doc.get('title', '')}**")
                st.caption(f"{doc.get('agent', '').replace('_', ' ')} | {doc.get('type', '')} | {doc.get('upload_date', '')}")
            
            with col2:
                if st.button("Delete", key=f"delete_{doc.get('id', '')}", type="primary"):
                    if document_store.delete_document(doc.get('id', '')):
                        st.success(f"Document '{doc.get('title', '')}' deleted successfully.")
                        # Rerun the app to refresh the list
                        st.rerun()
                    else:
                        st.error(f"Failed to delete document '{doc.get('title', '')}'.")

if __name__ == "__main__":
    # This will run the Streamlit app when executed directly
    pass 