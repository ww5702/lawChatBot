import streamlit as st
from src.data.ai_report_data import INITIAL_MESSAGE

def initialize_session_state():
    """세션 상태를 초기화합니다."""
    # 메시지가 없을 때만 초기화 (페이지 전환 시 대화 내용 유지)
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": INITIAL_MESSAGE}]
    
    # 페이지 상태가 없을 때만 초기화
    if "page" not in st.session_state:
        st.session_state["page"] = "home"
    
    # 변호사 선택 상태가 없을 때만 초기화
    if "selected_lawyer" not in st.session_state:
        st.session_state["selected_lawyer"] = None

    if "button_disabled" not in st.session_state:
        st.session_state.button_disabled = False
    
    # 다른 상태 변수들을 초기화
    initial_states = {
        "current_step": "initial",
        "legal_specification": "",
        "additional_questions": "",
        "additional_responses": "",
        "extra_information": "",
        "final_report": "",
        "current_category": None,
        "category_selected": False,
        "current_question": 0,
        "user_answers": {},
        "show_questions": True,
        "questionnaire_completed": False
    }
    
    for key, value in initial_states.items():
        if key not in st.session_state:
            st.session_state[key] = value

def setup_page_state(current_page):
    """페이지 상태를 설정합니다."""
    # 이전 페이지를 기억하는 상태가 없거나, 변경된 경우 초기화
    if "last_page" not in st.session_state or st.session_state.last_page != current_page:
        st.session_state.clear()  # 기존 상태 초기화
        st.session_state.last_page = current_page  # 현재 페이지를 저장하여 비교 