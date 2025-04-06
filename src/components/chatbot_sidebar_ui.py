import streamlit as st
from .chatbot_interface import reset_chat

def create_sidebar(llm):
    """Create and manage sidebar functionality"""
    with st.sidebar:
        # Search tools section
        st.subheader("🔍 검색 도구")
        st.caption("💬 버튼을 누르면 법률 검색이 진행됩니다. ")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 관련사례", use_container_width=True):
                st.session_state["loading"] = "case"
        
        with col2:
            if st.button("📜 법률정보", use_container_width=True):
                st.session_state["loading"] = "law"
        
        # Divider
        st.markdown("---")
        
        # Feature introduction
        st.subheader("📋 기능 소개")
        st.markdown("""
        💬 **법률 상담**: AI 변호사와 법률 상담하기 \n
        🔎 **관련사례 검색**: 유사 사례 및 예상 결과 확인 \n 
        📚 **법률정보 검색**: 관련 법률 조항 및 정보 제공
        """)
        
        st.markdown("---")
        
        # Chat reset button
        st.subheader("💬 채팅 관리")
        if st.button("🔄 채팅 새로하기", use_container_width=True):
            reset_chat()
        
        # Footer information
        st.markdown("---")
        st.caption("고객센터: 02-1004-1004")
        st.caption("이메일: happy6team@skala.com")
        st.caption("운영시간: 연중무휴 24시간!")