import streamlit as st
import src.components.guestbook_inputs as gi
from src.components.load import load_css

def render_review_form(path, file_name: str):
    load_css(path, file_name)
    
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

