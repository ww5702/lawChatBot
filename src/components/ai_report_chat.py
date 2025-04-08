from src.components.ai_report_handlers import handle_answering_questions_step, handle_completed_step, handle_extra_information_step
import streamlit as st
from src.components.questionnaire import add_message

def display_chat_history():
    """채팅 히스토리를 표시합니다."""
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

def handle_user_input(prompt):
    """사용자 입력을 처리합니다."""
    # 사용자 메시지 표시
    add_message("user", prompt)
    
    # 현재 단계에 따른 처리
    if st.session_state.current_step == "answering_questions":
        handle_answering_questions_step(prompt)
    elif st.session_state.current_step == "extra_information":
        handle_extra_information_step(prompt)
    else:  # completed 또는 기타 상태
        handle_completed_step(prompt) 