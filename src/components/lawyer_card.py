import streamlit as st
from src.utils.image_utils import get_image_as_base64

def display_lawyer_card(lawyer):
    """
    변호사 카드를 표시합니다. (원형 이미지 스타일 적용)
    
    Args:
        lawyer (dict): 변호사 정보
        show_selection_button (bool): 선택 버튼 표시 여부
    """
    st.markdown(f"""
    <div class="lawyer-info">
        <div style="text-align: center;">
            <div style="width: 150px; height: 150px; border-radius: 50%; overflow: hidden; margin: 0 auto;">
                <img src="data:image/jpeg;base64,{get_image_as_base64(lawyer["image_url"])}" style="width:100%; height:100%; object-fit:cover;">
            </div>
            <div style="font-size: 20px; font-weight: bold; margin-top: 10px;">{lawyer['name']} 변호사</div>
            <div style="font-style: italic; margin: 10px 0;">{lawyer['personality']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"{lawyer['name']} 변호사 선택하기", key=f"select_{lawyer['id']}", use_container_width=True):
        show_lawyer_selection_dialog(lawyer)

def display_selected_lawyer(lawyer):
    """
    선택된 변호사 정보를 표시합니다.
    
    Args:
        lawyer (dict): 선택된 변호사 정보
    """
    st.balloons()
    
    st.markdown(f"""
    <div class="selected-lawyer">
        <div style="display: flex; align-items: center;">
            <div style="margin-right: 20px;">
                <div style="width: 80px; height: 80px; border-radius: 50%; overflow: hidden;">
                    <img src="data:image/jpeg;base64,{get_image_as_base64(lawyer['image_url'])}" style="width:100%; height:100%; object-fit:cover;">
                </div>
            </div>
            <div>
                <div style="font-size: 24px; font-weight: bold;">{lawyer['name']} 변호사가 매칭되었습니다!</div>
                <div style="font-size: 18px; color: #3d6aff; margin-top: 5px;">{lawyer['specialty']}</div>
                <div style="font-size: 16px; color: #4B5563; margin-top: 5px;">{lawyer['personality2']}</div>
            </div>
        </div>
        <hr>
        <p style="white-space: pre-line;">{lawyer['description']}</p>
        <div style="margin-top: 20px;">
            <p>변호사가 곧 연락드릴 예정입니다. 감사합니다!<br><br>* 사실 연결은 안됩니다. 죄송합니다😘</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("다른 변호사 선택하기"):
        st.session_state.selected_lawyer = None
        st.rerun()
    
    st.balloons()

@st.dialog("국내 Top 변호사를 소개합니다")
def show_lawyer_selection_dialog(lawyer):
    """
    변호사 선택 다이얼로그를 표시합니다.
    
    Args:
        lawyer (dict): 변호사 정보
    """
    # 원형 이미지 컨테이너 스타일 적용
    st.markdown(f'''
    <div style="text-align: center; margin-bottom: 20px;">
        <div style="width: 150px; height: 150px; border-radius: 50%; overflow: hidden; margin: 0 auto;">
            <img src="data:image/jpeg;base64,{get_image_as_base64(lawyer["image_url"])}" style="width:100%; height:100%; object-fit:cover;">
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'<div class="lawyer-name">{lawyer["name"]} 변호사</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="lawyer-specialty">{lawyer["specialty"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="lawyer-personality">{lawyer["personality2"]}</div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f'<div class="lawyer-description">{lawyer["description"]}</div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("이 변호사를 선택하시겠습니까?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("취소", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("선택하기", type="primary", use_container_width=True):
            st.session_state.selected_lawyer = lawyer
            st.rerun() 