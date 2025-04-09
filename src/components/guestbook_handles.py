# import streamlit as st
# from databases import baseSource
# import sqlite3
# import time as now

# conn = baseSource.init()
# conn = baseSource.connect()
# cursor = conn.cursor()

# def handle_edit_cancel(review_id):
#     del st.session_state[f"show_edit_form_{review_id}"]
#     st.session_state.active_form = None
#     st.rerun()

# def handle_delete_cancel(review_id):
#     del st.session_state[f"show_delete_form_{review_id}"]
#     st.session_state.active_form = None
#     st.rerun()

# def handle_like(review_id):
#     try:
#         cursor.execute("UPDATE boards SET likes = likes + 1 WHERE board_id = ?", (review_id,))   
#         conn.commit()
#         st.success("좋아요를 눌렀습니다!")
#     except sqlite3.Error as e:
#         st.error(f"데이터베이스 오류: {e}")
#         conn.rollback()
#     # 1초 대기 후 페이지 새로고침
#     now.sleep(1)
#     st.rerun()

# def handle_delete(all_reviews, review_id):
#     # 다른 모든 폼 닫기
#     for r_id in [r[0] for r in all_reviews]:
#         # 다른 리뷰의 삭제 폼 닫기
#         st.session_state[f"show_delete_form_{r_id}"] = False
        
#         # 자신을 제외한 다른 리뷰의 편집 폼 닫기
#         if r_id != review_id:
#             st.session_state[f"show_edit_form_{r_id}"] = False
        
#         # 모든 편집 확인 상태 초기화
#         st.session_state[f"edit_verified_{r_id}"] = False
    
#     # 현재 리뷰의 편집 폼 닫기
#     st.session_state[f"show_edit_form_{review_id}"] = False
    
#     # 현재 폼 활성화
#     st.session_state.active_form = f"delete_{review_id}"
#     st.session_state[f"show_delete_form_{review_id}"] = True

# def handle_edit(all_reviews, review_id):
#     # 모든 다른 폼 닫기
#     for r_id in [r[0] for r in all_reviews]:
#         # 다른 리뷰의 삭제 폼 닫기
#         st.session_state[f"show_delete_form_{r_id}"] = False
        
#         # 자신을 제외한 다른 리뷰의 편집 폼 닫기
#         if r_id != review_id:
#             st.session_state[f"show_edit_form_{r_id}"] = False
        
#         # 모든 편집 확인 상태 초기화
#         st.session_state[f"edit_verified_{r_id}"] = False
    
#     # 현재 리뷰의 삭제 폼 닫기
#     st.session_state[f"show_delete_form_{review_id}"] = False
    
#     # 현재 폼 활성화
#     st.session_state.active_form = f"edit_{review_id}"
#     st.session_state[f"show_edit_form_{review_id}"] = True
    
# def handle_review_submission(user_name, user_password, user_review):
#     """후기 제출 시 DB 저장"""
#     if user_name and user_password and user_review:
#         cursor.execute("INSERT INTO boards (board_name, password, comment) VALUES (?, ?, ?)", (user_name, user_password, user_review))
#         conn.commit()
        
#         st.success("소중한 후기 감사합니다 😊")

#         # 세션 상태 초기화
#         for key in ["user_name", "user_password", "user_review"]:
#             if key in st.session_state:
#                 del st.session_state[key]

#         now.sleep(1)
#         st.rerun()
#     else:
#         st.error("이름과 비밀번호, 후기를 모두 작성해 주세요.")

# def delete_with_password(review_id, name, stored_password, input_password):
#     """비밀번호 확인 후 댓글 삭제"""
#     if input_password == stored_password:
#         # 비밀번호가 일치하면 삭제
#         cursor.execute("DELETE FROM boards WHERE board_id = ?", (review_id,))
#         conn.commit()
        
#         # 삭제 폼 상태 초기화
#         if f"show_delete_form_{review_id}" in st.session_state:
#             del st.session_state[f"show_delete_form_{review_id}"]
            
#         st.success(f"{name}님의 리뷰가 삭제되었습니다.")
#         now.sleep(1)
#         st.rerun()
#     else:
#         st.error("비밀번호가 일치하지 않습니다.")


# def handle_edit_pw(password_input, password, review_id):
#     if password_input == password:
#         st.session_state[f"edit_verified_{review_id}"] = True
#         st.success("비밀번호가 확인되었습니다. 내용을 수정해주세요.")
#         st.rerun()
#     else:
#         st.error("비밀번호가 일치하지 않습니다.")
        
# def handle_edit_save(new_review, review_id):
#     cursor.execute(
#         "UPDATE boards SET comment = ?, updated_at = CURRENT_TIMESTAMP WHERE board_id = ?", 
#         (new_review, review_id)
#     )
#     conn.commit()
                        
#     # 상태 초기화
#     del st.session_state[f"show_edit_form_{review_id}"]
#     del st.session_state[f"edit_verified_{review_id}"]
#     st.session_state.active_form = None
#     st.success("리뷰가 수정되었습니다.")
#     now.sleep(1)
#     st.rerun()

# def handle_edit_save_cancel(review_id):
#     del st.session_state[f"show_edit_form_{review_id}"]
#     del st.session_state[f"edit_verified_{review_id}"]
#     st.session_state.active_form = None
#     st.rerun()

import streamlit as st
import time as now
from .guestbook_db import GuestbookDB

# 데이터베이스 객체 초기화
db = GuestbookDB()

# 세션 상태 초기화
if 'active_form' not in st.session_state:
    st.session_state.active_form = None

def handle_edit_cancel(review_id):
    """편집 취소 처리"""
    del st.session_state[f"show_edit_form_{review_id}"]
    st.session_state.active_form = None
    st.rerun()

def handle_delete_cancel(review_id):
    """삭제 취소 처리"""
    del st.session_state[f"show_delete_form_{review_id}"]
    st.session_state.active_form = None
    st.rerun()

def handle_like(review_id):
    """좋아요 처리"""
    result = db.update_likes(review_id)
    if isinstance(result, tuple):
        st.error(result[1])
    else:
        st.success("좋아요를 눌렀습니다!")
    # 1초 대기 후 페이지 새로고침
    now.sleep(1)
    st.rerun()

def handle_delete(all_reviews, review_id):
    """삭제 폼 처리"""
    # 다른 모든 폼 닫기
    for r_id in [r[0] for r in all_reviews]:
        # 다른 리뷰의 삭제 폼 닫기
        st.session_state[f"show_delete_form_{r_id}"] = False
        
        # 자신을 제외한 다른 리뷰의 편집 폼 닫기
        if r_id != review_id:
            st.session_state[f"show_edit_form_{r_id}"] = False
        
        # 모든 편집 확인 상태 초기화
        st.session_state[f"edit_verified_{r_id}"] = False
    
    # 현재 리뷰의 편집 폼 닫기
    st.session_state[f"show_edit_form_{review_id}"] = False
    
    # 현재 폼 활성화
    st.session_state.active_form = f"delete_{review_id}"
    st.session_state[f"show_delete_form_{review_id}"] = True

def handle_edit(all_reviews, review_id):
    """편집 폼 처리"""
    # 모든 다른 폼 닫기
    for r_id in [r[0] for r in all_reviews]:
        # 다른 리뷰의 삭제 폼 닫기
        st.session_state[f"show_delete_form_{r_id}"] = False
        
        # 자신을 제외한 다른 리뷰의 편집 폼 닫기
        if r_id != review_id:
            st.session_state[f"show_edit_form_{r_id}"] = False
        
        # 모든 편집 확인 상태 초기화
        st.session_state[f"edit_verified_{r_id}"] = False
    
    # 현재 리뷰의 삭제 폼 닫기
    st.session_state[f"show_delete_form_{review_id}"] = False
    
    # 현재 폼 활성화
    st.session_state.active_form = f"edit_{review_id}"
    st.session_state[f"show_edit_form_{review_id}"] = True
    
def handle_review_submission(user_name, user_password, user_review):
    """후기 제출 처리"""
    if user_name and user_password and user_review:
        result = db.add_review(user_name, user_password, user_review)
        
        if isinstance(result, tuple):
            st.error(result[1])
        else:
            st.success("소중한 후기 감사합니다 😊")

            # 세션 상태 초기화
            for key in ["user_name", "user_password", "user_review"]:
                if key in st.session_state:
                    del st.session_state[key]

            now.sleep(1)
            st.rerun()
    else:
        st.error("이름과 비밀번호, 후기를 모두 작성해 주세요.")

def delete_with_password(review_id, name, stored_password, input_password):
    """비밀번호 확인 후 댓글 삭제"""
    if input_password == stored_password:
        # 비밀번호가 일치하면 삭제
        result = db.delete_review(review_id)
        
        if isinstance(result, tuple):
            st.error(result[1])
        else:
            # 삭제 폼 상태 초기화
            if f"show_delete_form_{review_id}" in st.session_state:
                del st.session_state[f"show_delete_form_{review_id}"]
                
            st.success(f"{name}님의 리뷰가 삭제되었습니다.")
            now.sleep(1)
            st.rerun()
    else:
        st.error("비밀번호가 일치하지 않습니다.")

def handle_edit_pw(password_input, password, review_id):
    """편집을 위한 비밀번호 확인"""
    if password_input == password:
        st.session_state[f"edit_verified_{review_id}"] = True
        st.success("비밀번호가 확인되었습니다. 내용을 수정해주세요.")
        st.rerun()
    else:
        st.error("비밀번호가 일치하지 않습니다.")
        
def handle_edit_save(new_review, review_id):
    """수정된 리뷰 저장"""
    result = db.update_review(review_id, new_review)
    
    if isinstance(result, tuple):
        st.error(result[1])
    else:
        # 상태 초기화
        del st.session_state[f"show_edit_form_{review_id}"]
        del st.session_state[f"edit_verified_{review_id}"]
        st.session_state.active_form = None
        st.success("리뷰가 수정되었습니다.")
        now.sleep(1)
        st.rerun()

def handle_edit_save_cancel(review_id):
    """편집 저장 취소"""
    del st.session_state[f"show_edit_form_{review_id}"]
    del st.session_state[f"edit_verified_{review_id}"]
    st.session_state.active_form = None
    st.rerun()

# 애플리케이션 종료 시 연결 닫기
def close_connection():
    db.close_connection()

# 앱 종료 시 연결 닫기 등록
import atexit
atexit.register(close_connection)