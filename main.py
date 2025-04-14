import streamlit as st
import os
import team_intro 
import service_intro
from src.utils.main_css_loader import load_main_css
from src.utils.main_html_loader import render_html
from src.components.main_sidebar import render_sidebar
from src.components.main_home_page import render_home_page
from src.routing.main_page_router import handle_redirects, update_current_page
from databases import baseSource


# 페이지 설정
st.set_page_config(
    page_title="AI 법률 서비스 사고닷",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 로드 
base_dir = os.path.dirname(os.path.abspath(__file__))
load_main_css(base_dir)

# DB 구성
conn = baseSource.init()
conn = baseSource.connect()
cursor = conn.cursor()

# 리디렉션 처리
handle_redirects(baseSource)

# 사이드바 렌더링
show_services, show_team, show_home = render_sidebar()

# 현재 페이지 상태 업데이트
current_page = update_current_page(show_services, show_team, show_home)

# 페이지 렌더링
if current_page == "홈":
    render_home_page(base_dir, conn, cursor)
elif current_page == "우리 팀 소개":
    team_intro.show_team_page()
elif current_page == "우리 서비스 소개":
    service_intro.show_service_page()

# 모든 페이지에 공통으로 표시되는 푸터
render_html(base_dir, "main_footer.html")
