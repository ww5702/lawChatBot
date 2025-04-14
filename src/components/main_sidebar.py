import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.image("assets/images/저울.webp", width=100)
        st.title("AI 법률 서비스 사고닷")
        st.markdown('<p>AI와 법률 전문가가 함께하는 스마트 법률 서비스.<br>승리를 만드는 길, 사고닷과 함께 준비하세요.</p>', unsafe_allow_html=True)
        
        st.divider()
        
        # 메뉴란 대신 버튼으로 대체
        st.subheader("소개합니다")
        show_services = st.button("👩🏻‍⚖️ 우리 서비스 소개")
        show_team = st.button("☀️ 우리 팀 소개")
        show_home = st.button("🏠 홈 돌아가기")
        
        st.divider()
        
        # 연락처 정보
        st.caption("고객센터: 02-1004-1004")
        st.caption("이메일: happy6team@skala.com")
        st.caption("운영시간: 연중무휴 24시간!")
        
    return show_services, show_team, show_home