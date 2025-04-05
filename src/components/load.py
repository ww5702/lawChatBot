from typing import List
import streamlit as st
import os

# 단일 CSS 파일 불러와 적용
def load_css(base_dir, file_name: str):
    css_path = os.path.join(base_dir, "assets", "css", file_name)
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# 여러 CSS 파일을 한 번에 불러와 적용
def load_multiple_css(base_dir: str, file_names: List[str]) -> None:
    css_content = ""
    for file_name in file_names:
        css_path = os.path.join(base_dir, "assets", "css", file_name)
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                css_content += f.read() + "\n"
        except FileNotFoundError:
            st.error(f"CSS 파일을 찾을 수 없습니다: {css_path}")
            
    if css_content:
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)



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


#  모든 main 관련 CSS 파일을 일관된 순서로 로드하는 함수
def load_main_css(base_dir: str) -> None:
    """메인 페이지의 CSS 파일들을 로드합니다."""
    css_files = [
        "main_base.css",
        "main_layout.css",
        "main_components.css", 
        "main_profile.css",
        "main_darkmode.css"
    ]
    load_multiple_css(base_dir, css_files)