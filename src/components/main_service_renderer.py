import streamlit as st
from src.utils.main_html_loader import render_html

def render_service_cards(base_dir):
    """서비스 카드를 렌더링합니다."""
    col1, col2, col3 = st.columns(3)
    
    # AI 법률 상담 폼
    with col1:
        render_service_form(
            base_dir,
            "ai_consultation_form",
            "💬",
            "실시간 AI 법률 상담",
            "AI 법률 비서가 실시간으로 법률 상담을 제공합니다.<br>간단한 법률 질문부터 검색까지 신속하게 답변해 드립니다.",
            "ai_consultation"
        )
    
    # 법률 자문 보고서 폼
    with col2:
        render_service_form(
            base_dir,
            "law_report_form",
            "📝",
            "AI 법률 보고서 + 변호사 매칭",
            "케이스에 맞는 맞춤형 법률 자문 보고서를 생성합니다.<br>이를 바탕으로 국내 최고의 변호사들과 바로 연결됩니다.",
            "law_report"
        )
    
    # 방명록 폼
    with col3:
        render_service_form(
            base_dir,
            "guestbook_form",
            "📋",
            "방명록",
            "서비스에 대해 자유롭게 의견을 남길 수 있는 공간입니다.<br>방명록을 작성하거나 '좋아요'를 눌러보세요!",
            "guestbook"
        )

def render_service_form(base_dir, form_key, icon, title, description, redirect_page):
    """서비스 폼을 렌더링합니다."""
    with st.form(key=form_key):
        service_values = {
            "icon": icon,
            "title": title,
            "description": description
        }
        render_html(base_dir, "main_service_card.html", service_values)
        submit_button = st.form_submit_button("바로가기", use_container_width=True)
        
        if submit_button:
            st.session_state.redirect_page = redirect_page
            st.rerun()