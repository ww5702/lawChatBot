import streamlit as st

def input_username():
    return st.text_input(
        "이름", 
        value=st.session_state.user_name if "user_name" in st.session_state else "", 
        key="user_name",
        placeholder="이름을 입력해주세요"
    )

def input_userpw():
    return st.text_input(
        "비밀번호", 
        type="password", 
        value=st.session_state.user_password if "user_password" in st.session_state else "", 
        key="user_password",
        placeholder="비밀번호를 입력해주세요"
    )

def input_review():
    return st.text_area(
        "후기 작성", 
        value=st.session_state.user_review if "user_review" in st.session_state else "", 
        key="user_review",
        placeholder="여기에 후기를 작성해주세요...",
        height=120
    )

def input_new_review(review, review_id):
    return st.text_area(
        "수정할 내용", 
        value=review, 
        key=f"edit_content_{review_id}"
    )

def input_delete_cancel(review_id):
    return st.text_input(
        "비밀번호를 입력하세요", 
        type="password", 
        key=f"del_pwd_{review_id}"
    )

def input_edit_cancel(review_id):
    return st.text_input(
        "비밀번호를 입력하세요", 
        type="password", 
        key=f"edit_pwd_{review_id}"
    )