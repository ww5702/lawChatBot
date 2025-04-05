import streamlit as st
import os
from typing import List

# 단일 CSS 파일 불러와 적용
def load_css(base_dir: str, file_name: str) -> None:
    """
    단일 CSS 파일을 불러와 Streamlit에 적용합니다.

    Args:
        base_dir (str): 기본 디렉토리 경로
        file_name (str): CSS 파일명
    """
    css_path = os.path.join(base_dir, "assets", "css", file_name)
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS 파일을 찾을 수 없습니다: {css_path}")

# 여러 CSS 파일을 한 번에 불러와 적용
def load_multiple_css(base_dir: str, file_names: List[str]) -> None:
    """
    여러 CSS 파일을 순서대로 불러와 하나의 스타일 태그로 Streamlit에 적용합니다.

    Args:
        base_dir (str): 기본 디렉토리 경로
        file_names (List[str]): CSS 파일명 리스트
    """
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

