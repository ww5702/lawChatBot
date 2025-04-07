import streamlit as st
from src.data.ai_report_data import STEPS
from src.services.report_service import get_progress_value, steps_completed

def display_sidebar_status(categories):
    """
    사이드바 상태를 표시합니다.
    
    Args:
        categories (dict): 법률 카테고리 데이터
    """
    with st.sidebar:
        st.subheader("진행 상태")
        
        current_step = st.session_state["current_step"]

        # 진행 상태 바
        progress_value = get_progress_value(
            current_step,
            st.session_state.current_category,
            st.session_state.current_question,
            categories
        )
        st.progress(progress_value)
        
        # 현재 선택된 카테고리 표시
        if st.session_state.current_category:
            st.info(f"선택한 법률 분야: {st.session_state.current_category}")

        # 상태에 따른 이모지 및 스타일 정의
        for step in STEPS:
            if steps_completed(
                current_step,
                step["key"],
                st.session_state.category_selected,
                st.session_state.questionnaire_completed
            ):
                # 완료된 단계 - 체크 표시와 함께 녹색으로 표시
                st.markdown(f"✅  **{step['name']}**")
            elif (current_step == "initial" and step["key"] == "category_selection" and st.session_state.category_selected) or \
                 (current_step == "initial" and step["key"] == "questionnaire" and not st.session_state.questionnaire_completed and st.session_state.category_selected) or \
                 (current_step == step["key"]):
                # 현재 진행 중인 단계 - 진행 중 표시와 함께 파란색으로 표시
                st.markdown(f"🔄  **{step['name']}**")
            else:
                # 아직 진행하지 않은 단계 - 회색으로 표시
                st.markdown(f"⬜  {step['name']}")

        # 보고서 다운로드 버튼 (보고서 생성이 완료된 경우에만)
        if current_step == "completed" and st.session_state["final_report"]:
            st.markdown("---")
            st.subheader("보고서 다운로드")
            st.download_button(
                label="📄 보고서 다운로드 (TXT)",
                data=st.session_state["final_report"],
                file_name="legal_report.txt",
                mime="text/plain"
            )
        
        # 처음부터 다시 시작하는 버튼
        if st.button("새 대화 시작"):
            reset_session_state()

        st.markdown("---")
        st.caption("고객센터: 02-1004-1004")
        st.caption("이메일: happy6team@skala.com")
        st.caption("운영시간: 연중무휴 24시간!")

def reset_session_state():
    """세션 상태를 초기화합니다."""
    from src.data.ai_report_data import INITIAL_MESSAGE
    
    # 초기화할 키 목록
    keys_to_reset = [
        "messages", "current_step", "legal_specification", 
        "additional_questions", "additional_responses", 
        "extra_information", "final_report",
        "current_category", "category_selected", "current_question",
        "user_answers", "show_questions", "questionnaire_completed"
    ]
    
    # 세션 상태 초기화
    for key in keys_to_reset:
        if key in st.session_state:
            if key == "messages":
                st.session_state[key] = [{"role": "assistant", "content": INITIAL_MESSAGE}]
            elif key == "current_step":
                st.session_state[key] = "initial"
            elif key == "current_category":
                st.session_state[key] = None
            elif key == "category_selected":
                st.session_state[key] = False
            elif key == "current_question":
                st.session_state[key] = 0
            elif key == "user_answers":
                st.session_state[key] = {}
            elif key == "show_questions":
                st.session_state[key] = True
            elif key == "questionnaire_completed":
                st.session_state[key] = False
            else:
                st.session_state[key] = ""
    st.rerun() 