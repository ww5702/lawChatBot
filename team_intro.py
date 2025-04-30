import streamlit as st
from src.utils.team_css_loader import load_team_css
from src.components.team_profile_renderer import render_team_profiles
from src.data.team_members_data import get_team_members_data

def show_team_page():
    """
    팀 소개 페이지를 렌더링합니다.
    """
    # CSS 로드
    load_team_css()
    
    # 헤더 섹션
    st.markdown("""
    <div class="title-container">
        <h1>행복한 6조 <span style="font-size: 1.5rem">(feat. 왕자님과 아이들)</span></h1>
        <p>저희 조는 웃음이 끊기지 않는 행복한 6조랍니다 🌸</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 팀원 데이터 로드
    team_members = get_team_members_data()
    
    # 팀원 프로필 렌더링
    render_team_profiles(team_members)