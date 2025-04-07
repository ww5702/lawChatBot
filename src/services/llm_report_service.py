from langchain_community.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from src.data.ai_report_data import API_KEY, MODEL, TEMPERATURE
from prompts.ai_report_prompts import question_generation_prompt, re_write_prompt, report_prompt

def create_llm():
    """LLM 인스턴스를 생성합니다."""
    return ChatOpenAI(
        openai_api_key=API_KEY,
        model=MODEL,
        temperature=TEMPERATURE
    )

def generate_questions(llm, specification):
    """추가 질문을 생성합니다."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", question_generation_prompt),
        ("user", "{specification}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"specification": specification})

def improve_questions(llm, questions_text):
    """생성된 질문을 개선합니다."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", re_write_prompt),
        ("user", "{questions}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"questions": questions_text})

def generate_legal_report(llm, legal_specification, additional_responses, extra_information):
    """법률 보고서를 생성합니다."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", report_prompt),
        ("user", "법률 분야: {category}\n사례 개요: {specification}\n추가 질문에 대한 답변:\n{additional_responses}\n추가 정보:\n{extra_information}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        "category": st.session_state.current_category,
        "specification": legal_specification,
        "additional_responses": additional_responses,
        "extra_information": extra_information
    })

def generate_chat_response(messages):
    """채팅 응답을 생성합니다."""
    from openai import OpenAI
    client = OpenAI(api_key=API_KEY)
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "당신은 법률 자문을 제공하는 AI 어시스턴트입니다. 사용자의 질문에 전문적이고 명확하게 답변해주세요."},
            *messages
        ],
        temperature=TEMPERATURE
    )
    
    return response.choices[0].message.content 