import streamlit as st
import os

# CSS 파일 불러와 적용
def load_css(base_dir, file_name: str):
    css_path = os.path.join(base_dir, "assets", "css", file_name)
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# html 파일 불러와 적용
def load_html(base_dir, file_name: str):
    html_path = os.path.join(base_dir, "assets", "html", file_name)
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
        st.markdown(f"{html}", unsafe_allow_html=True)
        
def load_review(base_dir, name : str, review : str, likes : str):
    html_path = os.path.join(base_dir, "assets", "html", "guestbook_review_box.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
            
            # 자리 표시자에 Python 변수 값 삽입
            html = html.replace("{name}", name).replace("{review}", review).replace("{likes}", str(likes))
            
            # 수정된 HTML을 Streamlit에서 렌더링
            st.markdown(html, unsafe_allow_html=True)
    else:
        st.error(f"지정된 HTML 파일을 찾을 수 없습니다.")