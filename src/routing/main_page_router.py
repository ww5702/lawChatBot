import streamlit as st

def handle_redirects(baseSource):
    """리디렉션을 처리합니다."""
    if 'redirect_page' in st.session_state:
        redirect_page = st.session_state.redirect_page
        
        # 먼저 조회수 업데이트
        if redirect_page == "ai_consultation":
            baseSource.updateView("user_view")
        elif redirect_page == "law_report":
            baseSource.updateView("report_view")
        
        # 세션에서 제거
        del st.session_state.redirect_page
        
        # 페이지 이동 (마지막에 실행)
        if redirect_page == "ai_consultation":
            st.switch_page("pages/ai_chatbot.py")
        elif redirect_page == "law_report":
            st.switch_page("pages/ai_report.py")
        elif redirect_page == "guestbook":
            st.switch_page("pages/guestbook.py")

def update_current_page(show_services, show_team, show_home):
    """현재 페이지 상태를 업데이트합니다."""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "홈"
        
    # 버튼 클릭에 따라 페이지 상태 변경
    if show_home:
        st.session_state.current_page = "홈"
    if show_team:
        st.session_state.current_page = "우리 팀 소개"
    if show_services:
        st.session_state.current_page = "우리 서비스 소개"
    
    return st.session_state.current_page