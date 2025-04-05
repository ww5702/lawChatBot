import os
import streamlit as st
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

# key 값
from config import initialize_environment
openai_api_key, tavily_api_key = initialize_environment()

@st.cache_resource
def load_chroma_db():
    """Load and cache ChromaDB for better performance"""
    # Create Chroma client instance
    chroma_client = chromadb.Client()
    
    return Chroma(
        client=chroma_client,
        collection_name="law_data",
        embedding_function=OpenAIEmbeddings(
            model="text-embedding-3-small", 
            # openai_api_key=st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY"))
            openai_api_key = openai_api_key
        ),
    )

def format_docs(docs):
    """Format documents for display, including metadata"""
    if isinstance(docs, list) and all(hasattr(doc, 'page_content') for doc in docs):
        # For PDF documents
        return "\n\n---\n\n".join([doc.page_content + f"\n출처: {doc.metadata['source']}" for doc in docs])
    else:
        # For web search results
        formatted_docs = []
        for d in docs:
            text = f"Content: {d.page_content}"
            if hasattr(d, 'metadata') and 'source' in d.metadata:
                text += f"\nURL: {d.metadata['source']}"
            formatted_docs.append(text)
        return "\n\n---\n\n".join(formatted_docs)