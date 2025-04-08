import streamlit as st
from src.components.questionnaire import add_message
from src.services.llm_report_service import create_llm, generate_legal_report, generate_chat_response

def handle_answering_questions_step(prompt):
    """추가 질문 답변 단계를 처리합니다."""
    # 추가 질문에 대한 답변 처리
    st.session_state.additional_responses = prompt
    
    # 추가 정보 요청
    response_text = "추가 질문에 답변해주셔서 감사합니다. 추가로 알려주실 정보가 있으시면 입력해주세요. \n\n없으시면 '없음'이라고 입력해주세요."
    add_message("assistant", response_text)
    
    # 다음 단계로 이동
    st.session_state.current_step = "extra_information"

def handle_extra_information_step(prompt):
    """추가 정보 입력 단계를 처리합니다."""
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
    try:
        # 로딩 스피너 표시
        with st.spinner('답변을 생성 중입니다...'):
            msg = generate_chat_response(st.session_state.messages)
        
        add_message("assistant", msg)
    except Exception as e:
        error_message = f"답변 생성 중 오류가 발생했습니다: {str(e)}"
        st.error(error_message)
        add_message("assistant", "답변 생성 중 오류가 발생했습니다. 다시 시도해주세요.") 