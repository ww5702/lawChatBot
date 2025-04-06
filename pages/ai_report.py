import streamlit as st
from src.data.ai_report_data import PAGE_CONFIG, INITIAL_MESSAGE
from src.data.legal_categories import categories
from src.data.select_lawyer import get_lawyers
from src.components.ai_report.lawyer_card import display_lawyer_card, display_selected_lawyer
from src.components.ai_report.sidebar import display_sidebar_status
from src.components.ai_report.questionnaire import show_category_selection, show_question
from src.services.llm_service import create_llm, generate_legal_report, generate_chat_response
from css_report import load_css

# 페이지 설정
st.set_page_config(**PAGE_CONFIG)

# 현재 페이지 식별
current_page = "ai_report"

# 이전 페이지를 기억하는 상태가 없거나, 변경된 경우 초기화
if "last_page" not in st.session_state or st.session_state.last_page != current_page:
    st.session_state.clear()  # 기존 상태 초기화
    st.session_state.last_page = current_page  # 현재 페이지를 저장하여 비교

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

def initialize_session_state():
    """세션 상태를 초기화합니다."""
    # 메시지가 없을 때만 초기화 (페이지 전환 시 대화 내용 유지)
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": INITIAL_MESSAGE}]
    
    # 페이지 상태가 없을 때만 초기화
    if "page" not in st.session_state:
        st.session_state["page"] = "home"
    
    # 변호사 선택 상태가 없을 때만 초기화
    if "selected_lawyer" not in st.session_state:
        st.session_state["selected_lawyer"] = None

    if "button_disabled" not in st.session_state:
        st.session_state.button_disabled = False
    
    # 다른 상태 변수들을 초기화
    initial_states = {
        "current_step": "initial",
        "legal_specification": "",
        "additional_questions": "",
        "additional_responses": "",
        "extra_information": "",
        "final_report": "",
        "current_category": None,
        "category_selected": False,
        "current_question": 0,
        "user_answers": {},
        "show_questions": True,
        "questionnaire_completed": False
    }
    
    for key, value in initial_states.items():
        if key not in st.session_state:
            st.session_state[key] = value

def display_chat_history():
    """채팅 히스토리를 표시합니다."""
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

def handle_user_input(prompt):
    """사용자 입력을 처리합니다."""
    from components.ai_report.questionnaire import add_message
    
    # 사용자 메시지 표시
    add_message("user", prompt)
    
    # 현재 단계에 따른 처리
    if st.session_state.current_step == "answering_questions":
        handle_answering_questions_step(prompt)
    elif st.session_state.current_step == "extra_information":
        handle_extra_information_step(prompt)
    else:  # completed 또는 기타 상태
        handle_completed_step(prompt)

def handle_answering_questions_step(prompt):
    """추가 질문 답변 단계를 처리합니다."""
    from components.ai_report.questionnaire import add_message
    
    # 추가 질문에 대한 답변 처리
    st.session_state.additional_responses = prompt
    
    # 추가 정보 요청
    response_text = "추가 질문에 답변해주셔서 감사합니다. 추가로 알려주실 정보가 있으시면 입력해주세요. \n\n없으시면 '없음'이라고 입력해주세요."
    add_message("assistant", response_text)
    
    # 다음 단계로 이동
    st.session_state.current_step = "extra_information"

def handle_extra_information_step(prompt):
    """추가 정보 입력 단계를 처리합니다."""
    from components.ai_report.questionnaire import add_message
    
    # 추가 정보 처리
    st.session_state.extra_information = prompt if prompt.lower() != "없음" else ""
    
    # 최종 보고서 생성
    try:
        # 로딩 스피너 표시
        with st.spinner(' 법률 보고서를 생성 중입니다. 잠시만 기다려주세요...'):
            llm = create_llm()
            
            final_report = generate_legal_report(
                llm,
                st.session_state.legal_specification,
                st.session_state.additional_responses,
                st.session_state.extra_information
            )
            
            # 최종 보고서 저장
            st.session_state.final_report = final_report

        # 어시스턴트 응답 표시
        response_text = "법률 보고서가 생성되었습니다:\n\n" + final_report
        add_message("assistant", response_text)
        
        # 마무리 메시지
        completion_text = "보고서 생성이 완료되었습니다. 아래 '변호사 매칭하기' 버튼을 클릭하시면 변호사 매칭 페이지로 이동합니다. 추가 질문이 있으시면 말씀해주세요."
        add_message("assistant", completion_text)
        
        # 다음 단계로 이동
        st.session_state.current_step = "completed"

        # 다운로드 버튼
        st.download_button(
            label="📄 보고서 다운로드 (TXT)",
            data=st.session_state["final_report"],
            file_name="AI법률_자문_보고서.txt",
            mime="text/plain", 
            use_container_width=True
        )
        
    except Exception as e:
        error_message = f"보고서 생성 중 오류가 발생했습니다: {str(e)}"
        st.error(error_message)
        add_message("assistant", f"보고서 생성 중 오류가 발생했습니다. 다시 시도해주세요.")

def handle_completed_step(prompt):
    """완료 단계를 처리합니다."""
    from components.ai_report.questionnaire import add_message
    
    try:
        # 로딩 스피너 표시
        with st.spinner('답변을 생성 중입니다...'):
            msg = generate_chat_response(st.session_state.messages)
        
        add_message("assistant", msg)
    except Exception as e:
        error_message = f"답변 생성 중 오류가 발생했습니다: {str(e)}"
        st.error(error_message)
        add_message("assistant", "답변 생성 중 오류가 발생했습니다. 다시 시도해주세요.")

def main():
    """메인 애플리케이션을 실행합니다."""
    # 세션 상태 초기화
    initialize_session_state()

    # CSS 로드
    load_css()
    
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
            show_question(categories)
    else:
        # 사용자 입력 처리
        if prompt := st.chat_input("질문을 입력하세요..."):
            handle_user_input(prompt)
    
    # 사이드바에 현재 상태 표시
    display_sidebar_status(categories)
    
    # 보고서가 생성된 후에는 변호사 매칭 버튼 표시
    if st.session_state.current_step == "completed" and st.session_state.final_report:
        if st.button("👩‍⚖️ 변호사 매칭하기", key="start_matching_main", use_container_width=True, type="primary"):
            set_page_to_lawyer_list()

if __name__ == "__main__":
    main() 