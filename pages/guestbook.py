import streamlit as st
import sqlite3
import time as now
import os
import sys

from src.components.load import load_css, load_html, load_review
import src.components.guestbook_inputs as gi
import src.components.guestbook_handles as gh

st.set_page_config(
    page_title="방명록",
    page_icon="📋",
    layout="centered",  # "wide"에서 "centered"로 변경
    initial_sidebar_state="expanded"
)

# utils 폴더를 sys.path에 추가
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # Python import 경로에 추가

from databases import baseSource

conn = baseSource.init()
conn = baseSource.connect()
cursor = conn.cursor()

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

def render_review_form(file_name: str):
    load_css(BASE_DIR, file_name)
    
    st.write("### 사용자 후기")
    with st.form(key='review_form'):
        col1, col2 = st.columns(2)
        with col1:
            user_name = gi.input_username()
        with col2:
            user_password = gi.input_userpw()
        user_review = gi.input_review()
        submit_button = st.form_submit_button("후기 제출")
    st.markdown('</div>', unsafe_allow_html=True)
    
    return user_name, user_password, user_review, submit_button

def display_reviews(file_name : str):
    """저장된 후기 목록을 출력"""
    load_css(BASE_DIR, file_name)
    
    # 세션 상태 초기화
    if 'active_form' not in st.session_state:
        st.session_state.active_form = None
    
    st.write("### 방명록")
    
    # 모든 리뷰 불러오기
    cursor.execute("SELECT * FROM boards ORDER BY board_id DESC")
    all_reviews = cursor.fetchall()

    # 각 리뷰 표시
    for idx, row in enumerate(all_reviews):
        review_id, name, password, review, likes = row[:5]

        # 리뷰 박스 생성
        load_review(BASE_DIR, name, review, likes)
        
        # 버튼 생성
        col1, col2, col3 = st.columns(3)
        
        # 좋아요 버튼
        like_button = col1.button("👍 좋아요", key=f"like_{review_id}_{idx}")
        
        # 수정 버튼
        edit_button = col2.button("✏️ 수정", key=f"edit_{idx}")
        
        # 삭제 버튼
        delete_button = col3.button("🗑️ 삭제", key=f"delete_{idx}")

        # 좋아요 버튼 처리
        if like_button:
            gh.handle_like(review_id)

        # 수정 버튼 처리
        if edit_button:
            gh.handle_edit(all_reviews, review_id)
            
        # 수정 폼 표시
        if st.session_state.get(f"show_edit_form_{review_id}", False):
            display_edit(review, review_id, password)

        # 삭제 버튼 처리
        if delete_button:
            gh.handle_delete(all_reviews, review_id)

        # 삭제 폼 표시
        if st.session_state.get(f"show_delete_form_{review_id}", False):
            display_cancel(review_id, name, password)
        
        # 리뷰 사이에 구분선 추가
        st.markdown("<hr style='margin: 20px 0; opacity: 0.3;'>", unsafe_allow_html=True)

def display_cancel(review_id, name, password):
    with st.container():
        # 삭제 폼
        load_html(BASE_DIR, "guestbook_cancel_form.html")
                
        # 비밀번호 입력 필드
        password_input = gi.input_delete_cancel(review_id)
                
        # 확인 및 취소 버튼
        del_col1, del_col2 = st.columns(2)
        confirm_button = del_col1.button("✓ 확인", key=f"confirm_del_{review_id}")
        cancel_button = del_col2.button("❌ 취소", key=f"cancel_del_{review_id}")
                
        # 확인 버튼 처리
        if confirm_button:
            gh.delete_with_password(review_id, name, password, password_input)
            st.session_state.active_form = None
                
        # 취소 버튼 처리
        if cancel_button:
            gh.handle_delete_cancel(review_id)

def display_edit(review, review_id, password):
    with st.container():
        # 수정 폼
        load_html(BASE_DIR, "guestbook_edit_form.html")
                
        # 비밀번호 입력 필드
        password_input = gi.input_edit_cancel(review_id)
                
        # 비밀번호 인증 완료 시 수정 폼
        if st.session_state.get(f"edit_verified_{review_id}", False):
            new_review = gi.input_new_review(review, review_id)
                    
            # 저장 및 취소 버튼
            col1, col2 = st.columns(2)
            save_button = col1.button("💾 저장", key=f"save_{review_id}")
            cancel_button = col2.button("❌ 취소", key=f"cancel_{review_id}")
                    
            # 저장 버튼 처리
            if save_button:
                gh.handle_edit_save(new_review, review_id)
                    
            # 취소 버튼 처리
            if cancel_button:
                gh.handle_edit_save_cancel(review_id)
        else:
            # 비밀번호 확인 및 취소 버튼
            verify_col1, verify_col2 = st.columns(2)
            verify_button = verify_col1.button("🔑 비밀번호 확인", key=f"verify_edit_{review_id}")
            cancel_edit_button = verify_col2.button("❌ 취소", key=f"cancel_edit_init_{review_id}")
                    
            # 비밀번호 확인 처리
            if verify_button:
                gh.handle_edit_pw(password_input, password, review_id)
                    
            # 취소 버튼 처리
            if cancel_edit_button:
                gh.handle_edit_cancel(review_id)

def display_sidebar():
    """사이드바를 표시하는 함수"""
    with st.sidebar:
        # 로고 및 타이틀
        st.markdown("<h1 style='font-size:120px;'>⚖️</h1>", unsafe_allow_html=True)
        st.title("사고닷 방명록")
        st.markdown('사고닷 서비스를 이용해주셔서 감사합니다. 여러분의 소중한 의견을 남겨주세요.', unsafe_allow_html=True)         
        
        st.divider()
        
        # 카운터 표시 (총 후기 갯수와 총 좋아요 갯수)
        st.subheader("📊 한눈에 보기")
        
        # 총 후기 갯수 
        cursor.execute("SELECT COUNT(*) FROM boards")
        total_reviews = cursor.fetchone()[0]
        st.metric(label="총 후기 갯수", value=f"{total_reviews}개")
        
        # 총 좋아요 갯수
        cursor.execute("SELECT SUM(likes) FROM boards")
        total_likes = cursor.fetchone()[0] or 0  # 이 함수는 별도로 구현해야 함
        st.metric(label="총 좋아요 갯수", value=f"{total_likes}개")
        
        st.divider()
        
        # 연락처 정보
        st.caption("고객센터: 02-1004-1004")
        st.caption("이메일: sagodot@example.com")
        st.caption("© 2025 사고닷. All rights reserved.")

def main():
    """메인 실행 함수"""
    load_css(BASE_DIR, "guestbook_background.css") # background css
    load_html(BASE_DIR, "guestbook_info.html") # info html

    # 후기 작성 폼 실행
    user_name, user_password, user_review, submit_button = render_review_form("guestbook_review.css")
    # 제출 버튼 클릭 시 처리
    if submit_button:
        gh.handle_review_submission(user_name, user_password, user_review)

    # 저장된 리뷰 목록 표시
    display_reviews("guestbook_reviews.css")

    # 사이드바 추가
    display_sidebar()

if __name__ == "__main__":
    main()