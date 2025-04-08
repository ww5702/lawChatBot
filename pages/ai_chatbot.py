# 아래 코드 Warning 제거
import os
import sys
import streamlit as st

# Import components
from src.components.chatbot_setup import initialize_llm
from src.components.chatbot_db_manager import load_chroma_db
from src.components.chatbot_interface import setup_session_state, display_messages, handle_user_input, display_search_results
from src.components.chatbot_sidebar_ui import create_sidebar
from src.components.chatbot_search_engine import process_searches

# key 값
from config import initialize_environment



################ 1. openai-api key #################

# OpenAI 클라이언트 연결
openai_api_key, tavily_api_key = initialize_environment()
# openai_api_key = st.secrets["OPENAI_API_KEY"]
# tavily_api_key = st.secrets["TAVILY_API_KEY"]


# client = OpenAI(api_key=openai_api_key)
os.environ["TAVILY_API_KEY"] = tavily_api_key
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ['USER_AGENT']='MyCustomAgent'


def main():
    """Main function to run the Streamlit app"""
    # Set page configuration
    st.set_page_config(
        page_title="실시간 AI 법률 상담",
        page_icon="💬",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # Current page identifier
    current_page = "ai_chatbot"
    
    # Initialize environment variables and API keys
    # openai_api_key, tavily_api_key = initialize_environment()
    
    # Initialize LLM
    llm = initialize_llm(openai_api_key)
    
    # Load ChromaDB
    db = load_chroma_db()
    
    # Setup BASE_DIR for path references
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(BASE_DIR)
    
    # Set up title and caption
    st.title("💬 실시간 AI 법률 상담")
    st.caption("💬 법률 관련 질문을 입력하고 AI 변호사와 상담해 보세요.")
    
    # Initialize or update session state
    setup_session_state(current_page)
    
    # Display previous messages
    display_messages()
    
    # Create sidebar with search functionality
    create_sidebar(llm)
    
    # Process any pending searches
    process_searches(llm)
    
    # Handle user input
    handle_user_input(openai_api_key)
    
    # Display search results if available
    display_search_results()

if __name__ == "__main__":
    main()
