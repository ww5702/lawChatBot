import streamlit as st
from src.utils.image_utils import get_image_as_base64

def render_team_profiles(team_members):
    """
    팀원 프로필 카드를 렌더링합니다.
    
    Args:
        team_members (list): 팀원 정보가 담긴 사전 객체 리스트
    """
    # 3개의 컬럼 생성
    cols = st.columns(3)
    
    # 팀원 데이터를 순회하며 각 컬럼에 프로필 카드 추가
    for i, member in enumerate(team_members):
        col_index = i % 3
        
        with cols[col_index]:
            render_single_profile(member)

def render_single_profile(member):
    """
    개별 팀원 프로필을 렌더링합니다.
    
    Args:
        member (dict): 팀원 정보가 담긴 사전 객체
    """
    try:
        # 이미지 로드 및 렌더링
        img_base64 = get_image_as_base64(member['image'])
        if img_base64:
            st.markdown(f"""
                <div class="member-card">
                    <img src="data:image/jpeg;base64,{img_base64}">
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:red;">⚠️ 이미지 로드 실패</p>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"이미지 로드 중 오류 발생: {e}")

    # 팀원 정보 렌더링
    st.markdown(f"""
        <div class="member-info">
            <h2 class="member-name">{member['name']}</h2>
            <span class="member-nickname">{member['nickname']}</span>
            <p>🔷 {member['intro']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 팀원 상세 정보 렌더링
    st.markdown(f"""
        <div class="member-details">
            <p><strong>특징:</strong> {member['feature']}</p>
            <p><strong>MBTI:</strong> {member['mbti']}</p>
            <p><strong>담당 역할:</strong> {member['role']}</p>
        </div>
        """, unsafe_allow_html=True)