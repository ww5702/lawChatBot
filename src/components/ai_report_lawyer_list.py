import streamlit as st
from src.data.select_lawyer import get_lawyers
from src.components.lawyer_card import display_lawyer_card, display_selected_lawyer

def set_page_to_lawyer_list():
    """변호사 목록 페이지로 이동합니다."""
    st.session_state.page = "lawyer_list"
    st.rerun()

def show_lawyer_list_page():
    """변호사 목록 페이지를 표시합니다."""
    st.markdown("<div class='main-title'>변호사 매칭 서비스</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-subtitle'>원하시는 변호사를 선택해 주세요!</div>", unsafe_allow_html=True)
    
    # 홈으로 돌아가기 버튼
    if st.button("← 처음으로 돌아가기", key="back_to_home"):
        st.session_state.page = "home"
        st.rerun()

    if st.session_state.selected_lawyer is None:
        lawyers = get_lawyers()
        cols = st.columns(3)
        
        for i, lawyer in enumerate(lawyers):
            with cols[i % 3]:
                display_lawyer_card(lawyer)
    else:
        display_selected_lawyer(st.session_state.selected_lawyer) 