def generate_legal_specification(user_answers, current_category):
    """
    사용자 응답을 바탕으로 법률 명세서를 생성합니다.
    
    Args:
        user_answers (dict): 사용자의 응답
        current_category (str): 현재 선택된 법률 카테고리
        
    Returns:
        str: 생성된 법률 명세서
    """
    specification = f"법률 카테고리: {current_category}\n\n"
    
    for question, answers in user_answers.items():
        if isinstance(answers, list):
            specification += f"- {question}: {', '.join(answers)}\n"
        else:
            specification += f"- {question}: {answers}\n"
    
    return specification

def get_progress_value(current_step, current_category, current_question, categories):
    """
    현재 진행 상태의 진행률을 계산합니다.
    
    Args:
        current_step (str): 현재 단계
        current_category (str): 현재 선택된 카테고리
        current_question (int): 현재 질문 번호
        categories (dict): 카테고리 데이터
        
    Returns:
        float: 0.0 ~ 1.0 사이의 진행률
    """
    from src.config.config import PROGRESS_VALUES
    
    # 현재 상태를 평가하기 위한 현재 단계 결정
    if current_step == "initial" and current_category:
        current_status = "category_selection"
    else:
        current_status = current_step
    
    # 설문지 진행 중인 경우 진행률 계산
    if current_status == "category_selection" and current_category:
        total_questions = len(categories.get(current_category, []))
        if total_questions > 0:
            questionnaire_progress = current_question / total_questions
            return PROGRESS_VALUES["category_selection"] + questionnaire_progress * (PROGRESS_VALUES["questionnaire"] - PROGRESS_VALUES["category_selection"])
    
    return PROGRESS_VALUES.get(current_status, 0.0)

def steps_completed(current_step, step_key, category_selected, questionnaire_completed):
    """
    특정 단계가 완료되었는지 확인합니다.
    
    Args:
        current_step (str): 현재 단계
        step_key (str): 확인할 단계 키
        category_selected (bool): 카테고리가 선택되었는지 여부
        questionnaire_completed (bool): 설문지가 완료되었는지 여부
        
    Returns:
        bool: 단계 완료 여부
    """
    step_order = {
        "initial": 0,
        "category_selection": 1,
        "questionnaire": 2,
        "answering_questions": 3,
        "extra_information": 4,
        "completed": 5
    }
    
    # 카테고리가 선택되었으면 category_selection 단계는 완료된 것으로 간주
    if step_key == "category_selection" and category_selected:
        return True
    
    # 설문지가 완료되었으면 questionnaire 단계는 완료된 것으로 간주
    if step_key == "questionnaire" and questionnaire_completed:
        return True
    
    # 현재 단계가 해당 단계보다 뒤에 있으면 완료된 것으로 간주
    return step_order.get(current_step, 0) > step_order.get(step_key, 0) 