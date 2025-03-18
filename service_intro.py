import streamlit as st
import os


def show_service_page():
    # 페이지 기본 설정

    # CSS 스타일 적용
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
            * {
                font-family: 'Noto Sans KR', sans-serif;
            }
            .main {
                background-color: #F8F9FA;
                color: #333;
            }
            .title-container {
                background: linear-gradient(135deg, #3D6AFF, #3D6AFF );
                padding: 3rem 1rem;
                border-radius: 20px;
                color: white;
                text-align: center;
                margin-bottom: 2.5rem;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            }
            .title-container h1 {
                font-size: 3rem;
                font-weight: 700;
                margin-bottom: 1rem;
                letter-spacing: -0.5px;
            }
            .title-container p {
                font-size: 1.3rem;
                opacity: 0.9;
                max-width: 700px;
                margin: 0 auto;
            }
            .section-title {
                color: #0062CC;
                font-size: 2.2rem;
                margin: 2.5rem 0 1.5rem 0;
                text-align: center;
                font-weight: 700;
                letter-spacing: -0.5px;
                position: relative;
                padding-bottom: 10px;
            }
            .section-title:after {
                content: "";
                position: absolute;
                bottom: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 80px;
                height: 4px;
                background: linear-gradient(90deg, #0062CC, #104E8B);
                border-radius: 2px;
            }
            .problem-list {
                list-style-type: none;
                padding-left: 0;
                text-align: center;
                max-width: 800px;
                margin: 0 auto;
            }
            .problem-list li {
                font-size: 1.2rem;
                margin-bottom: 15px;
                line-height: 1.6;
                color: #333;
            }
            .feature-card {
                background-color: #fff;
                padding: 2rem;
                margin-bottom: 1.5rem;
                border-radius: 16px;
                text-align: center;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.05);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                border-top: 5px solid #0062CC;
            }
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
            }
            .feature-title {
                font-size: 1.7rem;
                color: #0062CC;
                margin-bottom: 1rem;
                font-weight: 700;
            }
            .feature-card p {
                font-size: 1.1rem;
                line-height: 1.7;
                color: #555;
            }
            .contributor-section {
                background-color: #E6F2FF;
                padding: 2rem;
                border-radius: 16px;
                margin-top: 2rem;
                margin-bottom: 2rem;
            }
            .contributor-card {
                background-color: #fff;
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
                height: 100%;
                transition: transform 0.3s ease;
            }
            .contributor-card:hover {
                transform: translateY(-3px);
            }
            .contributor-title {
                color: #0062CC;
                font-size: 1.3rem;
                font-weight: 600;
                margin-bottom: 0.8rem;
                text-align: center;
            }
            .contributor-names {
                text-align: center;
                font-size: 1.1rem;
                color: #555;
            }
            .footer {
                text-align: center;
                padding: 3rem 0 1rem 0;
                color: #666;
                font-size: 1rem;
                margin-top: 2rem;
                border-top: 1px solid #eee;
            }
            .vision-box {
                background: linear-gradient(135deg, #E6F2FF, #CCE5FF);
                padding: 2rem;
                border-radius: 16px;
                margin: 2rem auto;
                max-width: 900px;
                text-align: center;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.05);
                position: relative;
                overflow: hidden;
            }
            .vision-box:before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 5px;
                background: linear-gradient(90deg, #0062CC, #104E8B);
            }
            .vision-box h3 {
                color: #0062CC;
                font-size: 1.8rem;
                margin-bottom: 1rem;
                font-weight: 700;
            }
            .vision-box p {
                font-size: 1.2rem;
                line-height: 1.7;
                color: #444;
            }
            /* 스트림릿 요소 스타일 재정의 */
            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 1200px;
                margin: 0 auto;
            }
            /* 버튼 스타일 */
            .stButton>button {
                background-color: white;
                border-radius: 10px;
                border: none;
                font-weight: 500;
                border-radius: 5px;
                width: 100%;
                margin-bottom: 3px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s;
                cursor: pointer;
                padding: 0.8em;
            }
            
            .stButton>button:hover {
                background-color: #3d6aff;
                color: white;
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
            }
            /* 컨테이너 패딩 */
            .main .block-container {
                padding-left: 2rem;
                padding-right: 2rem;
            }
            /* 아이콘 스타일 */
            .icon {
                font-size: 2.5rem;
                color: #0062CC;
                margin-bottom: 1rem;
            }
            /* ✅ 다크모드 스타일 */
            @media (prefers-color-scheme: dark) {
            /* 페이지 전체 배경 및 텍스트 색상 조정 */
            .main {
                background-color: #121212 !important;
                color: #EAEAEA !important;
            }
        
            /* 문제 리스트 (problem-list) - 배경 투명, 글씨 흰색 */
            .problem-list {
                color: #FFF !important;
            }
        
            /* 문제 리스트의 개별 항목 (li) - 글씨 흰색 */
            .problem-list li {
                color: #FFF !important;
            }
        
            /* 서비스 카드 (feature-card) - 검정 배경, 흰 글씨 */
            .feature-card {
                background-color: #000 !important;
                color: #FFF !important;
                border-top: 5px solid #3D6AFF !important;
                box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1) !important;
            }
        
            /* 서비스 카드 안의 텍스트 (p 태그) - 글씨 흰색 */
            .feature-card p {
                color: #FFF !important;
            }
        
            /* 기여자 카드 (contributor-card) - 검정 배경 */
            .contributor-card {
                background-color: #000 !important;
                color: #FFF !important;
                box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1) !important;
            }
        
            /* 기여자 이름 (contributor-names) - 흰 글씨 */
            .contributor-names {
                color: #FFF !important;
            }
            .vision-box {
                background-color: #000 !important;
                color: #FFF !important;
                box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1) !important;
            }
        
            /* 기여자 이름 (contributor-names) - 흰 글씨 */
            .vision-box p {
                color: #FFF !important;
            }
        }

            
        </style>
        """, unsafe_allow_html=True)
        # 페이지 제목
    st.markdown("""
        <div class="title-container">
            <h1>🚀 사고닷 🚀</h1>
            <p>복잡한 법률 문제를 쉽고 빠르게 해결해드립니다</p>
        </div>
        """, unsafe_allow_html=True)
        # 서비스 소개
    st.markdown("<div class='section-title'>우리 서비스</div>", unsafe_allow_html=True)
    st.markdown("""
            <ul class='problem-list'>
                <li>법률 정보, 누구나 필요하지만 너무 어렵고 복잡해서 쉽게 접근하기 힘들죠?</li>
                <li>그래서 우리 팀은 AI 기반 법률 상담 서비스를 만들었어요!</li>
                <li>기술과 법률을 연결해서, 법에 대해 잘 모르는 사람도 쉽게 필요한 정보를 얻고,</li>
                    <li>적절한 법적 조치를 취할 수 있도록 도와주는 게 우리의 목표입니다.</li>
            </ul>
        """, unsafe_allow_html=True)
        # 해결하고자 한 문제
    st.markdown("<div class='section-title'>우리가 해결하고자 한 문제</div>", unsafe_allow_html=True)
    st.markdown("""
        <ul class='problem-list'>
            <li>법률 상담은 너무 비싸고, 어디서부터 시작해야 할지 막막해요.</li>
            <li>인터넷에서 찾아도 이 정보가 맞는지, 신뢰할 수 있는지 알기 어렵고요.</li>
            <li>변호사를 찾아서 상담받는 것도 너무 번거로워요.</li>
        </ul>
        """, unsafe_allow_html=True)
        # 서비스 특징
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
        # 비전
    st.markdown("""
        <div class="vision-box">
            <h3>우리의 비전</h3>
            <p>우리는 이 서비스를 통해, 누구나 편리하게 사용할 수 있는 도구가 되길 바랍니다.</p>
        </div>
        """, unsafe_allow_html=True)
        # 개발 기여자들
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
    st.markdown('</div>', unsafe_allow_html=True)
