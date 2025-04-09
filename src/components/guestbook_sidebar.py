import streamlit as st

def display_sidebar(cursor):
     """사이드바를 표시하는 함수"""
     with st.sidebar:
         # 로고 및 타이틀
         st.markdown("<h1 style='font-size:120px;'>⚖️</h1>", unsafe_allow_html=True)
         st.title("사고닷 방명록")
         st.markdown('사고닷 서비스를 이용해 주셔서 감사합니다. 여러분의 소중한 의견을 남겨주세요.', unsafe_allow_html=True)         
        
         st.divider()
        
         # 카운터 표시 (총 후기 갯수와 총 좋아요 갯수)
         st.subheader("📊 한눈에 보기")
        
         # 총 후기 갯수 
         cursor.execute("SELECT COUNT(*) FROM boards")
         total_reviews = cursor.fetchone()[0]
         st.metric(label="총 후기 개수", value=f"{total_reviews}개")
        
         # 총 좋아요 갯수
         cursor.execute("SELECT SUM(likes) FROM boards")
         total_likes = cursor.fetchone()[0] or 0  # 이 함수는 별도로 구현해야 함
         st.metric(label="총 좋아요 개수", value=f"{total_likes}개")
        
         st.divider()
        
         # 연락처 정보
         st.caption("고객센터: 02-1004-1004")
         st.caption("이메일: happy6team@skala.com")
         st.caption("운영시간: 연중무휴 24시간!")