# key 값
from config import initialize_environment
openai_api_key, tavily_api_key = initialize_environment()

# 초기 메시지
INITIAL_MESSAGE = "법률 사건의 정확한 이해를 돕기 위해 상담을 진행합니다."

# 모델 설정
OPENAI_API_KEY=openai_api_key
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.2

# 페이지 설정
PAGE_CONFIG = {
    "page_title": "AI 법률 자문 보고서 생성",
    "page_icon": "📝",
    "layout": "centered",  # "wide"에서 "centered"로 변경
    "initial_sidebar_state": "expanded"
}

# 법률 카테고리 옵션
CATEGORIES_OPTIONS = [
    {"name": "교통사고", "col": 0},
    {"name": "폭행/상해", "col": 0},
    {"name": "사기", "col": 1},
    {"name": "이혼", "col": 1}
]

# 단계 정의
STEPS = [
    {"key": "category_selection", "name": "법률 카테고리 선택"},
    {"key": "questionnaire", "name": "사건 명세서 작성"},
    {"key": "answering_questions", "name": "추가 질문 답변"},
    {"key": "extra_information", "name": "추가 정보 입력"},
    {"key": "completed", "name": "법률 자문 보고서 생성"}
]

# 진행률 설정
PROGRESS_VALUES = {
    "initial": 0.0,
    "category_selection": 0.1,
    "questionnaire": 0.4,
    "answering_questions": 0.6,
    "extra_information": 0.8,
    "completed": 1.0
} 