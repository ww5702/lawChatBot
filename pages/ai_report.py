import streamlit as st
from src.data.ai_report_data import PAGE_CONFIG
from src.data.legal_categories import categories
from src.components.ai_report_setup import initialize_session_state, setup_page_state
from src.components.ai_report_lawyer_list import show_lawyer_list_page, set_page_to_lawyer_list
from src.components.ai_report_chat import display_chat_history, handle_user_input
from src.components.ai_report_sidebar import display_sidebar_status
from src.components.questionnaire import show_category_selection, show_question
from css_report import load_css

# 페이지 설정
st.set_page_config(**PAGE_CONFIG)

# 현재 페이지 식별
current_page = "ai_report"

# 페이지 상태 설정
setup_page_state(current_page)

def main():
    """메인 애플리케이션을 실행합니다."""
    # 세션 상태 초기화
    initialize_session_state()

    # CSS 로드
    load_css()

    print("testing", flush=True)
    
    # 페이지 라우팅 - 먼저 페이지 상태 확인
    if st.session_state.page == "lawyer_list":
        show_lawyer_list_page()
        return  # 중요: 여기서 함수 종료
    
    # AI 법률 자문 페이지 (홈)
    st.title("📝 AI 법률 자문 보고서 생성")
    st.caption("법률 보고서 생성 후 변호사 매칭이 이루어집니다 👩🏻‍💼")
    
    # 메시지 히스토리 표시
    display_chat_history()
    
    # 현재 단계에 따른 인터페이스 표시
    if st.session_state.show_questions:
        if not st.session_state.category_selected:
            show_category_selection()
        else:
            show_question()
    else:
        # 사용자 입력 처리
        if prompt := st.chat_input("질문을 입력하세요..."):
            handle_user_input(prompt)
    
    # 사이드바에 현재 상태 표시
    display_sidebar_status(categories)
    
    # 보고서가 생성된 후에는 변호사 매칭 버튼 표시
    if st.session_state.current_step == "completed" and st.session_state.final_report:
        # 버튼을 더 눈에 띄게 만들고 직접 페이지를 변경하는 함수 호출
        if st.button("👩‍⚖️ 변호사 매칭하기", key="start_matching_main", use_container_width=True, type="primary"):
            set_page_to_lawyer_list()

if __name__ == "__main__":
    main()
