import os
import sys
import streamlit as st
# from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI  # ✅ 최신 경고 해결


# Import base directory for consistent imports
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# key 값
from config import initialize_environment
openai_api_key, tavily_api_key = initialize_environment()

def initialize_llm(openai_api_key=None):
    """Initialize the Language Model"""
    if not openai_api_key:
        openai_api_key = st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY"))
        # openai_api_key = openai_api_key
        
    return ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.1,
        openai_api_key=openai_api_key,
        max_tokens=256
    )

def load_prompt(filename: str) -> str:
    # 현재 파일 기준으로 상위 폴더 ../prompts/filename 위치로 경로 설정
    base_dir = os.path.dirname(__file__)  # = src/components
    # prompt_path = os.path.join(base_dir, "..", "..", "prompts", filename)
    # src/prompts로 변경할 시 가져올 코드 
    prompt_path = os.path.join(base_dir, "..", "prompts", filename) 
    prompt_path = os.path.abspath(prompt_path)  # 절대 경로로 변환

    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()
