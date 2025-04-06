import os
import streamlit as st

def initialize_environment():
    """Initialize environment variables and API keys"""
    # # Try to get keys from secrets
    try:
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        tavily_api_key = st.secrets["TAVILY_API_KEY"]
    except Exception:
        # If secrets not available, try to import from config
        try:
            from config import load_keys
            openai_api_key, tavily_api_key = load_keys()
        except ImportError:
            st.error("API keys not found. Please check your configuration.")
            st.stop()
    """API 키 로드"""
    #openai_api_key = "YOUR_KEY"
    #tavily_api_key = "YOUR_KEY"
    # Set environment variables
    os.environ["TAVILY_API_KEY"] = tavily_api_key
    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ['USER_AGENT'] = 'MyCustomAgent'
    
    return openai_api_key, tavily_api_key
