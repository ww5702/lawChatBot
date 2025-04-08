import streamlit as st
from src.utils.main_html_loader import render_html, render_horizontal_line
from src.components.main_service_renderer import render_service_cards
from src.components.main_profile_renderer import render_lawyer_profiles
from src.data.main_lawyers_data import get_lawyers_data
from src.data.main_statistics import render_statistics
from src.utils.image_utils import get_image_as_base64

def render_home_page(base_dir, conn, cursor):
    """홈 페이지를 렌더링합니다."""
    # 헤더 표시
    render_html(base_dir, "main_header.html")
    
    # 서비스 소개 제목
    render_html(base_dir, "main_services_title.html")
    
    # 서비스 카드 렌더링
    render_service_cards(base_dir)
    
    # 구분선
    render_horizontal_line()
    
    # 변호사 소개 제목
    render_html(base_dir, "main_lawyers_title.html")
    
    # 변호사 프로필 렌더링
    lawyers_data = get_lawyers_data()
    render_lawyer_profiles(base_dir, lawyers_data, get_image_as_base64)
    
    # 구분선
    render_horizontal_line()
    
    # 통계 섹션
    render_html(base_dir, "main_statistics_title.html")
    
    # 통계 렌더링
    render_statistics(conn, cursor)