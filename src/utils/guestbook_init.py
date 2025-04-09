import streamlit as st

def initialize_session():
    """세션 상태 초기화"""
    # 초기 세션 상태 설정
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "user_password" not in st.session_state:
        st.session_state.user_password = ""
    if "user_review" not in st.session_state:
        st.session_state.user_review = ""
    # 비밀번호 입력 상태 추가
    if "delete_password" not in st.session_state:
        st.session_state.delete_password = {}
    # 활성 폼 상태 추가
    if "active_form" not in st.session_state:
        st.session_state.active_form = None