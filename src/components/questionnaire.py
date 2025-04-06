import streamlit as st
from data.ai_report_data import CATEGORIES_OPTIONS
from src.data.legal_categories import categories
from src.services.report_service import generate_legal_specification
from src.services.llm_service import create_llm, generate_questions, improve_questions

def show_category_selection():
    """법률 카테고리 선택 화면을 표시합니다."""
    st.write("상담 카테고리를 선택해 주세요.")
    cols = st.columns(2)
    
    for category in CATEGORIES_OPTIONS:
        with cols[category["col"]]:
            if st.button(category["name"], use_container_width=True):
                st.session_state.current_category = category["name"]
                st.session_state.category_selected = True
                st.session_state.current_question = 0
                st.session_state.user_answers = {}
                st.rerun()

def disable_button():
    """마지막 질문에서만 버튼을 비활성화합니다."""
    if st.session_state.current_question + 1 >= len(categories[st.session_state.current_category]):
        st.session_state.button_disabled = True

def show_question(categories):
    """
    현재 질문을 표시하고 응답을 수집합니다.
    
    Args:
        categories (dict): 법률 카테고리 데이터
    """
    if st.session_state.current_category and st.session_state.current_question < len(categories[st.session_state.current_category]):
        current_q = categories[st.session_state.current_category][st.session_state.current_question]
        total_questions = len(categories[st.session_state.current_category])

        # 질문 내용 표시
        st.write(f"{current_q['question']} ({st.session_state.current_question + 1}/{total_questions})")

        # 현재 질문이 마지막 질문인지 확인
        is_last_question = st.session_state.current_question + 1 >= total_questions

        # 라디오 버튼 (단일 선택)
        if current_q['type'] == 'radio':
            selected_option = st.radio("선택하세요:", current_q['options'], key=f"radio_{st.session_state.current_question}")

            if st.button("다음", key=f"next_{st.session_state.current_question}", disabled=st.session_state.button_disabled, on_click=disable_button if is_last_question else None):
                handle_question_response(current_q, selected_option, categories)

        # 체크박스 (다중 선택)
        elif current_q['type'] == 'checkbox':
            selected_options = []
            for option in current_q['options']:
                if st.checkbox(option, key=f"checkbox_{st.session_state.current_question}_{option}"):
                    selected_options.append(option)
            
            if st.button("다음", key=f"next_{st.session_state.current_question}", disabled=st.session_state.button_disabled, on_click=disable_button if is_last_question else None):
                if selected_options:
                    handle_question_response(current_q, selected_options, categories)
                else:
                    st.warning("최소 하나 이상의 옵션을 선택해주세요.")

def handle_question_response(current_q, selected_option, categories):
    """
    질문 응답을 처리합니다.
    
    Args:
        current_q (dict): 현재 질문 정보
        selected_option: 선택된 응답
        categories (dict): 법률 카테고리 데이터
    """
    # 응답 저장
    st.session_state.user_answers[current_q['question']] = selected_option
    
    # 다음 질문으로 이동
    st.session_state.current_question += 1
    
    # 모든 질문이 끝났을 때 다음 단계로 진행
    if st.session_state.current_question >= len(categories[st.session_state.current_category]):
        handle_questionnaire_completion()
    
    st.rerun()

def handle_questionnaire_completion():
    """설문지 완료 후 처리를 수행합니다."""
    try:
        # 먼저 사용자에게 법률 명세서 요약 표시
        legal_spec = generate_legal_specification(st.session_state.user_answers, st.session_state.current_category)
        summary_message = f"작성하신 {st.session_state.current_category} 사건 명세서의 내용은 다음과 같습니다:\n\n"
        
        # 응답을 정리해서 표시
        for question, answers in st.session_state.user_answers.items():
            if isinstance(answers, list):
                summary_message += f"• {question}: {', '.join(answers)}\n\n"
            else:
                summary_message += f"• {question}: {answers}\n\n"
        
        # 사용자에게 법률 명세서 요약 표시
        add_message("user", summary_message)

        # 로딩 스피너 표시
        with st.spinner('법률 명세서를 분석하고 추가 질문을 생성 중입니다...'):
            # LLM 인스턴스 생성
            llm = create_llm()
            
            # 추가 질문 생성
            generated_questions = generate_questions(llm, legal_spec)
            
            # 생성된 질문 개선
            improved_questions = improve_questions(llm, generated_questions)
            
            # 개선된 질문 저장 (문자열 형태)
            st.session_state.additional_questions = improved_questions
        
        # 어시스턴트 응답 표시
        response_text = f"입력하신 내용을 바탕으로 분석했습니다. 추가 정보를 위해 다음 질문에 답변해 주세요:\n\n{improved_questions}\n\n답변 가능한 선에서 최대한 구체적으로 작성해주세요."
        
        add_message("assistant", response_text)
        
        # 다음 단계로 이동
        st.session_state.current_step = "answering_questions"
        st.session_state.show_questions = False
        
    except Exception as e:
        st.error(f"법률 명세서 분석 중 오류가 발생했습니다: {str(e)}")
        add_message("assistant", f"오류가 발생했습니다. 다시 시도해주세요.")

def add_message(role, content):
    """메시지를 추가합니다."""
    st.session_state.messages.append({"role": role, "content": content})
    st.chat_message(role).write(content) 