import streamlit as st
import os
from typing import Dict, Any, Optional

def load_html(base_dir: str, file_name: str) -> str:
    """
    HTML 파일을 로드하여 문자열로 반환합니다.
    
    Args:
        base_dir (str): 기본 디렉토리 경로
        file_name (str): HTML 파일명
        
    Returns:
        str: HTML 내용
    """
    html_path = os.path.join(base_dir, "assets", "html", file_name)
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"HTML 파일을 찾을 수 없습니다: {html_path}")
        return ""

def render_html(base_dir: str, file_name: str, values: Optional[Dict[str, Any]] = None) -> None:
    """
    HTML 파일을 로드하고 Streamlit에 표시합니다.
    
    Args:
        base_dir (str): 기본 디렉토리 경로
        file_name (str): HTML 파일명
        values (Optional[Dict[str, Any]]): 대체할 키-값 쌍 (템플릿인 경우)
    """
    html = load_html(base_dir, file_name)
    if html:
        if values:
            # 모든 {key}를 해당 값으로 대체
            for key, value in values.items():
                html = html.replace(f"{{{key}}}", str(value))
        st.markdown(html, unsafe_allow_html=True)

def render_horizontal_line() -> None:
    """
    수평선을 표시합니다.
    """
    st.markdown("""
        <div class='horizon-line'></div>
        """, unsafe_allow_html=True)