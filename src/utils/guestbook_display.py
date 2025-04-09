import streamlit as st
import src.components.guestbook_inputs as gi
import src.components.guestbook_handles as gh
from src.components.load import load_css, load_html, load_review
from src.components.guestbook_db import GuestbookDB

# 데이터베이스 객체 초기화
db = GuestbookDB()

def display_reviews(path, file_name : str):
    """저장된 후기 목록을 출력"""
    load_css(path, file_name)
    
    # 세션 상태 초기화
    if 'active_form' not in st.session_state:
        st.session_state.active_form = None
    
    st.write("### 방명록")
    
    # 모든 리뷰 불러오기
    all_reviews = db.get_all_reviews()

    # 각 리뷰 표시
    for idx, row in enumerate(all_reviews):
        review_id, name, password, review, likes = row[:5]

        # 리뷰 박스 생성
        load_review(path, name, review, likes)
        
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
            display_edit(path, review, review_id, password)

        # 삭제 버튼 처리
        if delete_button:
            gh.handle_delete(all_reviews, review_id)

        # 삭제 폼 표시
        if st.session_state.get(f"show_delete_form_{review_id}", False):
            display_cancel(path, review_id, name, password)
        
        # 리뷰 사이에 구분선 추가
        st.markdown("<hr style='margin: 20px 0; opacity: 0.3;'>", unsafe_allow_html=True)

def display_cancel(path, review_id, name, password):
    with st.container():
        # 삭제 폼
        load_html(path, "guestbook_cancel_form.html")
                
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

def display_edit(path, review, review_id, password):
    with st.container():
        # 수정 폼
        load_html(path, "guestbook_edit_form.html")
                
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