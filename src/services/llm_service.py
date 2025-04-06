from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from openai import OpenAI
from src.data.ai_report_data import API_KEY, MODEL, TEMPERATURE
from prompts.ai_report_prompts import question_generation_prompt, re_write_prompt, report_prompt

def create_llm():
    """LLM 인스턴스를 생성합니다."""
    return ChatOpenAI(api_key=API_KEY, model=MODEL, temperature=TEMPERATURE)

def generate_questions(llm, specification):
    """추가 질문을 생성합니다."""
    chain = question_generation_prompt | llm | StrOutputParser()
    return chain.invoke({"specification": specification})

def improve_questions(llm, questions_text):
    """생성된 질문을 개선합니다."""
    question_rewriter = re_write_prompt | llm | StrOutputParser()
    return question_rewriter.invoke({"question": questions_text})

def generate_legal_report(llm, legal_specification, additional_responses, extra_information):
    """법률 보고서를 생성합니다."""
    chain = report_prompt | llm | StrOutputParser()
    return chain.invoke({
        "legal_specification": legal_specification,
        "additional_responses": additional_responses,
        "extra_information": extra_information
    })

def generate_chat_response(messages):
    """채팅 응답을 생성합니다."""
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful legal assistant that has already generated a report. Answer any additional questions the user might have."},
            *[{"role": m["role"], "content": m["content"]} for m in messages]
        ]
    )
    return response.choices[0].message.content 