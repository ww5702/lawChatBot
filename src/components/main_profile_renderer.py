import streamlit as st
from src.utils.main_html_loader import render_html

def render_lawyer_profiles(base_dir, lawyers_data, get_image_as_base64):
    """변호사 프로필 카드를 렌더링합니다."""
    # 첫 번째 행 (변호사 0, 1, 2)
    row1_cols = st.columns(3)
    
    for i in range(3):
        render_profile(base_dir, lawyers_data[i], row1_cols[i], get_image_as_base64)
    
    # 첫 번째 행과 두 번째 행 사이의 간격 추가
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # 두 번째 행 (변호사 3, 4, 5)
    row2_cols = st.columns(3)
    
    for i in range(3, 6):
        render_profile(base_dir, lawyers_data[i], row2_cols[i-3], get_image_as_base64)

def render_profile(base_dir, lawyer, column, get_image_as_base64):
    """개별 변호사 프로필을 렌더링합니다."""
    img_path = lawyer["image"]
    img_base64 = get_image_as_base64(img_path)
    
    if img_base64:
        img_html = f'<img src="data:image/jpeg;base64,{img_base64}" style="width:100%; height:100%; object-fit:cover;">'
    else:
        # 이미지가 없을 경우 기본 아이콘 사용
        gender_icon = "👩‍⚖️" if lawyer["name"] not in ["이재웅"] else "👨‍⚖️"
        img_html = f'<span style="font-size: 30px;">{gender_icon}</span>'
    
    profile_values = {
        "image": img_html,
        "name": lawyer["name"],
        "specialty": lawyer["specialty"]
    }
    
    with column:
        render_html(base_dir, "main_profile_card.html", profile_values)