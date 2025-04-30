import streamlit as st
from src.utils.service_css_loader import load_service_css
from src.components.service_sections_renderer import render_service_sections

def show_service_page():
    """
    서비스 소개 페이지를 렌더링합니다.
    """
    # CSS 로드
    load_service_css()
    
    # 페이지 제목
    st.markdown("""
        <div class="title-container">
            <h1>🚀 사고닷 🚀</h1>
            <p>복잡한 법률 문제를 쉽고 빠르게 해결해드립니다</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 페이지 섹션 렌더링
    render_service_sections()