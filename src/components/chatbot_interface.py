import os
import time
import streamlit as st
from openai import OpenAI

from .chatbot_setup import load_prompt
from models.agent import Agent

# key 값
from config import initialize_environment
openai_api_key, tavily_api_key = initialize_environment()

def setup_session_state(current_page):
    """Initialize or update session state variables"""
    # Check if page has changed and reset if needed
    if "last_page" not in st.session_state or st.session_state.last_page != current_page:
        st.session_state.clear()
        st.session_state.last_page = current_page
    
    # Load system prompt
    system_prompt = load_prompt("chatbot_prompt.txt")
    
    # Initialize chatbot if not already present
    if "chatbot" not in st.session_state:
        st.session_state["chatbot"] = Agent(
            system_prompt=system_prompt, 
            # api_key=st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY"))
            api_key= openai_api_key
        )
    
    # Initialize message history
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 법률 상담이 필요하시면 질문해 주세요."}]
    
    # Initialize search results storage
    if "case_result" not in st.session_state:
        st.session_state["case_result"] = None
    if "law_result" not in st.session_state:
        st.session_state["law_result"] = None
    if "loading" not in st.session_state:
        st.session_state["loading"] = False

def display_messages():
    """Display all messages in the chat history"""
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

def handle_user_input(openai_api_key):
    """Process user input and generate response"""
    user_input = st.chat_input("질문을 입력하세요...")
    
    if user_input:
        # Check if API key is available
        if not openai_api_key:
            st.info("🔑 OpenAI API Key를 입력해주세요.")
            st.stop()
        
        # Short delay
        time.sleep(1)
        
        # Initialize OpenAI client
        client = OpenAI(api_key=openai_api_key)
        
        # Save user input to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        # Short delay before generating response
        time.sleep(1)
        
        # Generate chatbot response
        chatbot_response = st.session_state["chatbot"](user_input)
        st.session_state.messages.append({"role": "assistant", "content": chatbot_response})
        st.chat_message("assistant").write(chatbot_response)

def display_search_results():
    """Display search results if available"""
    # Display case search results
    if st.session_state["case_result"]:
        st.subheader("🔍 검색된 관련사례 및 예상결과")
        st.write(st.session_state["case_result"].content)
    
    # Display law search results
    if st.session_state["law_result"]:
        st.subheader("📚 검색된 법률정보")
        st.write(st.session_state["law_result"])

def reset_chat():
    """Reset chat to initial state"""
    # Load system prompt
    system_prompt = load_prompt("chatbot_prompt.txt")
    
    # Create new chatbot instance
    st.session_state["chatbot"] = Agent(
        system_prompt=system_prompt, 
        # api_key=st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY"))
        api_key=openai_api_key
    )
    
    # Reset messages
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 법률 상담이 필요하시면 질문해주세요."}]
    
    # Reset search results
    st.session_state["case_result"] = None
    st.session_state["law_result"] = None
    
    # Refresh page
    st.rerun()