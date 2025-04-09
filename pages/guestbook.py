import streamlit as st
import sqlite3
import time as now
import os
import sys

from src.components.load import load_css, load_html, load_review
import src.components.guestbook_sidebar as bar
import src.components.guestbook_render as gr
import src.components.guestbook_handles as gh
from databases import baseSource
import src.utils.guestbook_init as init
import src.utils.guestbook_display as gd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # Python import 경로에 추가

st.set_page_config(
    page_title="방명록",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="expanded"
)

def main():
    """메인 실행 함수"""
    # 세션 초기화
    init.initialize_session()
    
    # 데이터베이스 연결
    conn = baseSource.init()
    conn = baseSource.connect()
    cursor = conn.cursor()
    
    load_css(BASE_DIR, "guestbook_background.css") # background css
    load_html(BASE_DIR, "guestbook_info.html") # info html

    # 후기 작성 폼 실행
    user_name, user_password, user_review, submit_button = gr.render_review_form(BASE_DIR, "guestbook_review.css")
    
    # 제출 버튼 클릭 시 처리
    if submit_button:
        gh.handle_review_submission(user_name, user_password, user_review)

    # 저장된 리뷰 목록 표시
    gd.display_reviews(BASE_DIR, "guestbook_reviews.css")

    # 사이드바 추가
    bar.display_sidebar(cursor)

if __name__ == "__main__":
    main()