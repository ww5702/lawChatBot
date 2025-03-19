import streamlit as st
import pandas as pd
def display_sidebar():
    """사이드바를 표시하는 함수"""
    with st.sidebar:
        # 로고 및 타이틀
        st.markdown("<h1 style='font-size:120px;'>⚖️</h1>", unsafe_allow_html=True)
        st.title("사고닷 방명록")
        st.markdown('사고닷 서비스를 이용해 주셔서 감사합니다. 여러분의 소중한 의견을 남겨주세요.', unsafe_allow_html=True)
        st.divider()
        # 카운터 표시 (총 후기 갯수와 총 좋아요 갯수)
        st.subheader(":막대_차트: 한눈에 보기")
        # # 총 후기 갯수
        # cursor.execute("SELECT COUNT(*) FROM boards")
        # total_reviews = cursor.fetchone()[0]
        # st.metric(label="총 후기 개수", value=f"{total_reviews}개")
        # # 총 좋아요 갯수
        # cursor.execute("SELECT SUM(likes) FROM boards")
        # total_likes = cursor.fetchone()[0] or 0  # 이 함수는 별도로 구현해야 함
        # st.metric(label="총 좋아요 개수", value=f"{total_likes}개")
        # st.divider()
        # 연락처 정보
        st.caption("고객센터: 02-1004-1004")
        st.caption("이메일: happy6team@skala.com")
        st.caption("운영시간: 연중무휴 24시간!")
def main():
    # 페이지 기본 설정
    st.set_page_config(
        page_title="오류 안내",
        page_icon=":경고:",
        layout="centered"
    )
    # CSS 스타일 적용
    st.markdown("""
    <style>
    .error-container {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
    }
    .error-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
    }
    .error-title {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #FF4B4B;
    }
    .error-message {
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .contact-info {
        font-size: 1rem;
        color: #555;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    # 오류 내용 표시
    st.markdown("""
    <div class="error-container">
        <div class="error-icon">:경고:</div>
        <div class="error-title">서비스 이용에 불편을 드려 죄송합니다</div>
        <div class="error-message">
            많은 사용량으로 인해 해당 서비스를 중단하게 되었습니다.<br>
            75분간 이용해 주셔서 감사합니다.
    </div>
    """, unsafe_allow_html=True)
    # 돌아가기 버튼
    if st.button("메인 페이지로 돌아가기"):
        st.success("메인 페이지로 이동합니다...")
        # 실제 구현 시에는 여기에 메인 페이지로 리디렉션하는 코드 추가
    # 오류 세부 정보 (접어두기 기능)
    with st.expander("오류 세부 정보"):
        st.code("""
Error: 500 Internal Server Error
Time: 2025-03-19 14:30:45
Path: /dashboard/analytics
Request ID: 7a8b9c0d1e2f
        """)
         # 사이드바 추가
    display_sidebar()
if __name__ == "__main__":
    main()
