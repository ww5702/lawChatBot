from langchain_community.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from src.data.ai_report_data import OPENAI_API_KEY, MODEL, TEMPERATURE
from src.components.chatbot_setup import load_prompt

def create_llm():
    """LLM 인스턴스를 생성합니다."""
    return ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model=MODEL,
        temperature=TEMPERATURE
    )

def generate_questions(llm, specification):
    """추가 질문을 생성합니다."""
    question_generation_prompt = ChatPromptTemplate.from_messages([
    ("system", load_prompt("question_generation_prompt.txt")),
    ("human", "다음 법률 명세서를 바탕으로 추가 질문 3가지를 생성해주세요: {specification}")
    ])
    print("question prompt 생성 완료")
    
    chain = question_generation_prompt | llm | StrOutputParser()
    print("chain 생성 완료")
    return chain.invoke({"specification": specification})

def improve_questions(llm, questions_text):
    re_write_prompt = ChatPromptTemplate.from_messages([
    ("system", load_prompt("re_write_prompt.txt")),
    ("user", "원본 질문: {question} \n 새로운 질문:")
    ])
    
    question_rewriter = re_write_prompt | llm | StrOutputParser()
    return question_rewriter.invoke({"question": questions_text})

def generate_legal_report(llm, legal_specification, additional_responses, extra_information):
    """법률 보고서를 생성합니다."""
    report_prompt =ChatPromptTemplate.from_messages([
    ("system", load_prompt("system_report_prompt.txt")),
    ("human", load_prompt("human_report_prompt.txt"))
    ])
    
    chain = report_prompt | llm | StrOutputParser()
    return chain.invoke({
        "legal_specification": legal_specification,
        "additional_responses": additional_responses,
        "extra_information": extra_information
    })

def generate_chat_response(messages):
    """채팅 응답을 생성합니다."""
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful legal assistant that has already generated a report. Answer any additional questions the user might have."},
            *[{"role": m["role"], "content": m["content"]} for m in messages]
        ]
    )
    
    return response.choices[0].message.content 
