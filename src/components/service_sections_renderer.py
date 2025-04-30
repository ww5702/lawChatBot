import streamlit as st

def render_service_sections():
    """
    서비스 소개 페이지의 각 섹션을 렌더링합니다.
    """
    render_service_intro()
    render_problem_section()
    render_feature_section()
    render_vision_section()
    render_contributor_section()

def render_service_intro():
    """서비스 소개 섹션을 렌더링합니다."""
    st.markdown("<div class='section-title'>우리 서비스</div>", unsafe_allow_html=True)
    st.markdown("""
        <ul class='problem-list'>
            <li>법률 정보, 누구나 필요하지만 너무 어렵고 복잡해서 쉽게 접근하기 힘들죠?</li>
            <li>그래서 우리 팀은 AI 기반 법률 상담 서비스를 만들었어요!</li>
            <li>기술과 법률을 연결해서, 법에 대해 잘 모르는 사람도 쉽게 필요한 정보를 얻고,</li>
            <li>적절한 법적 조치를 취할 수 있도록 도와주는 게 우리의 목표입니다.</li>
        </ul>
    """, unsafe_allow_html=True)

def render_problem_section():
    """해결하고자 한 문제 섹션을 렌더링합니다."""
    st.markdown("<div class='section-title'>우리가 해결하고자 한 문제</div>", unsafe_allow_html=True)
    st.markdown("""
        <ul class='problem-list'>
            <li>법률 상담은 너무 비싸고, 어디서부터 시작해야 할지 막막해요.</li>
            <li>인터넷에서 찾아도 이 정보가 맞는지, 신뢰할 수 있는지 알기 어렵고요.</li>
            <li>변호사를 찾아서 상담받는 것도 너무 번거로워요.</li>
        </ul>
    """, unsafe_allow_html=True)

def render_feature_section():
    """서비스 특징 섹션을 렌더링합니다."""
    st.markdown("<div class='section-title'>서비스 특징</div>", unsafe_allow_html=True)
    
    # 각 서비스 카드
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🤖</div>
            <div class="feature-title">실시간 AI 법률 상담</div>
            <p>법에 대해 잘 몰라도, 누구나 쉽게 상담할 수 있어요! 복잡한 법률 용어는 잊고 일상적인 언어로 질문하세요. <br>
                    AI 기술과 법전을 담은 데이터 베이스를 활용하여 믿을 수 있는 정보와 관련 사례를 제공합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">📋</div>
            <div class="feature-title">AI 법률 보고서 </br> 변호사 매칭</div>
            <p>AI 기술을 활용한 사건 보고서 생성과 변호사 매칭 기능까지 지원해 실질적인 법적 조치를 취할 수 있어요!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">📝</div>
            <div class="feature-title">방명록</div>
            <p>사고닷을 사용한 후 의견이나 궁금한 점, 방문 후기를 자유롭게 남겨주세요! 여러분의 피드백이 서비스를 개선하는 데 큰 도움이 됩니다.</p>
        </div>
        """, unsafe_allow_html=True)

def render_vision_section():
    """비전 섹션을 렌더링합니다."""
    st.markdown("""
        <div class="vision-box">
            <h3>우리의 비전</h3>
            <p>우리는 이 서비스를 통해, 누구나 편리하게 사용할 수 있는 도구가 되길 바랍니다.</p>
        </div>
    """, unsafe_allow_html=True)

def render_contributor_section():
    """개발 기여자 섹션을 렌더링합니다."""
    st.markdown("<div class='section-title'>개발 기여자들</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="contributor-card">
            <div class="contributor-title">실시간 AI 법률 상담</div>
            <div class="contributor-names">재웅, 실</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="contributor-card">
            <div class="contributor-title">AI 법률 보고서 + 변호사 매칭</div>
            <div class="contributor-names">지영, 민주</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="contributor-card">
            <div class="contributor-title">방명록</div>
            <div class="contributor-names">다은, 효정</div>
        </div>
        """, unsafe_allow_html=True)