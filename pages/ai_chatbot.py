
import os
import streamlit as st
import sys
# ✅ 강제로 pysqlite3를 sqlite3로 등록
os.environ["SQLITE_LIBRARY_PATH"] = "/usr/lib/sqlite3"  # 이 줄은 무시 가능 (서버 따라 다름)
import pysqlite3
sys.modules["sqlite3"] = pysqlite3

import sqlite3
import time

from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from chromadb.config import Settings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema.output_parser import StrOutputParser
from openai import OpenAI
from langchain_openai import ChatOpenAI
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain.prompts import PromptTemplate


st.set_page_config(
    page_title="실시간 AI 법률 상담",
    page_icon="💬",
    layout="centered",  # "wide"에서 "centered"로 변경
    initial_sidebar_state="expanded"
)


# 현재 파일(ai_chatbot.py)의 위치를 기반으로 lawChatBot 경로 추가
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # lawChatBot 디렉토리 경로
sys.path.append(BASE_DIR)  # Python import 경로에 추가

# agent 관리 파일
from agent import Agent
# key 값
from config import load_keys

# 현재 페이지 식별
current_page = "ai_chatbot"

# ####################################################
# [ code 순서 ]                              
# 1. openai-api key
# 2. 챗봇 프롬프트, agent 정의
# 3. chatbot객체(streamlit) 생성 및 기능 구현
# 4. DB구축 및 pdf_rag_chain 생성
# 5. tavily검색하는 web_rag_chain 생성
# 6. 디비, 웹 검색 기능 추가
####################################################


################ 1. openai-api key #################

# OpenAI 클라이언트 연결
# openai_api_key, tavily_api_key = load_keys()
openai_api_key = st.secrets["OPENAI_API_KEY"]
tavily_api_key = st.secrets["TAVILY_API_KEY"]


client = OpenAI(api_key=openai_api_key)
os.environ["TAVILY_API_KEY"] = tavily_api_key

os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ['USER_AGENT']='MyCustomAgent'
# 아래 코드 Warning 제거

# ChromaDB 미리 로드하여 검색 속도 최적화
@st.cache_resource
def load_chroma_db():
    return Chroma(
        persist_directory=os.path.join(os.path.dirname(__file__), "chroma_Web"),
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=openai_api_key),
        client_settings=Settings(chroma_db_impl="duckdb+parquet")
    )

db = load_chroma_db()
retriever = db.as_retriever()

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.1,
    openai_api_key=openai_api_key,
    max_tokens=256 # 최대 토근 256
)

# 프롬프트 로드 함수 추가
# def load_prompt(filename):
#     base_path = os.path.dirname(__file__)  # 현재 파일 기준 디렉토리
#     prompt_path = os.path.join(base_path, "prompts", filename)  # 절대 경로로 설정
#     with open(prompt_path, "r", encoding="utf-8") as file:
#         return file.read()
def load_prompt(filename):
    # lawChatBot 내 prompts 폴더 경로 설정
    prompt_path = os.path.join(BASE_DIR, "prompts", filename)  # 절대 경로 사용
    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()

# 이전 페이지를 기억하는 상태가 없거나, 변경된 경우 초기화
if "last_page" not in st.session_state or st.session_state.last_page != current_page:
    st.session_state.clear()  # 기존 상태 초기화
    st.session_state.last_page = current_page  # 현재 페이지를 저장하여 비교


st.title("💬 실시간 AI 법률 상담")
st.caption("💬 법률 관련 질문을 입력하고 AI 변호사와 상담해 보세요.")
####################################################

############# 2. 챗봇 프롬프트, agent 정의 ############
# ✅ 시스템 프롬프트 (단계별 상담 + 가이드라인 유지)
system_prompt = load_prompt("chatbot_prompt.txt")


##### 3. chatbot객체(streamlit) 생성 및 기능 구현 #####
# ✅ 챗봇 인스턴스 저장 (세션 상태 관리)
if "chatbot" not in st.session_state:
    st.session_state["chatbot"] = Agent(system_prompt=system_prompt, api_key=openai_api_key)
# ✅ 기존 대화 기록 관리
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 법률 상담이 필요하시면 질문해 주세요."}]

# ✅ 기존 대화 UI 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# ✅ 사용자 입력 받기
if user_input := st.chat_input("질문을 입력하세요..."):
    if not openai_api_key:
        st.info("🔑 OpenAI API Key를 입력해주세요.")
        st.stop()

    time.sleep(1) # 호출 전 1초 대기

    client = OpenAI(api_key=openai_api_key)

    # 사용자 입력 저장
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    time.sleep(1) # 1초 대기
    # 챗봇 응답 생성
    chatbot_response = st.session_state["chatbot"](user_input)
    st.session_state.messages.append({"role": "assistant", "content": chatbot_response})
    st.chat_message("assistant").write(chatbot_response)
####################################################


############ 4. DB 검색 pdf_rag_chain 생성 ###########

# PDF RAG 프롬프트 로드
pdf_prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template=load_prompt("pdf_rag_prompt.txt")
)

# 검색 결과를 포맷팅하는 함수
def format_docs(docs):
    return "\n\n---\n\n".join([doc.page_content + f"\n출처: {doc.metadata['source']}" for doc in docs])


# RAG 체인 구성
pdf_rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | pdf_prompt_template
    | llm
    | StrOutputParser()
)
####################################################


######## 5. Tavily 검색하는 web_rag_chain 생성 ########

# ✅ Tavily 검색 결과를 정리하는 함수
def format_docs(docs):
    """검색된 문서를 정리하여 반환"""
    formatted_docs = []
    for d in docs:
        text = f"Content: {d.page_content}"
        if hasattr(d, 'metadata') and 'source' in d.metadata:
            text += f"\nURL: {d.metadata['source']}"
        formatted_docs.append(text)
    return "\n\n---\n\n".join(formatted_docs)

# ✅ Tavily 검색 API 호출 (캐싱 적용)
@st.cache_data(show_spinner=False)
def web_search(query):
    retriever = TavilySearchAPIRetriever(k=3, search_depth="advanced", include_domains=["news"], verbose=False)
    return retriever.invoke(query)

# ✅ Tavily 검색 설정
# Web RAG 프롬프트 로드
web_prompt_template = ChatPromptTemplate.from_template(load_prompt("web_rag_prompt.txt"))

# ✅ Tavily 검색 RAG 체인 (LLM에 올바른 입력 타입 전달)
def web_rag_chain(query):
    """Tavily 검색을 수행한 후 LLM을 통해 최적의 답변 생성"""
    search_results = web_search(query)  # 검색 수행 (캐싱 적용)
    formatted_results = format_docs(search_results)  # 검색 결과 포맷팅

    # ✅ LLM이 올바르게 처리할 수 있도록 web_prompt_template.format() 사용
    final_prompt = web_prompt_template.format(context=formatted_results, question=query)

    time.sleep(1) # 1초 대기
    return llm.invoke(final_prompt)  # ✅ str 타입으로 변환된 프롬프트 전달

####################################################

############ 6. 디비, 웹 검색 기능 추가 ###############

# ✅ 검색 결과를 저장할 세션 상태 초기화
if "case_result" not in st.session_state:
    st.session_state["case_result"] = None  # 관련 사례 및 예상 결과
if "law_result" not in st.session_state:
    st.session_state["law_result"] = None  # 관련 법률 정보
if "loading" not in st.session_state:
    st.session_state["loading"] = False  # 스피너 상태


# 사이드바 - 기능 소개 및 버튼 추가
with st.sidebar:

    # 검색 기능 섹션
    st.subheader("🔍 검색 도구")
    st.caption("💬 버튼을 누르면 법률 검색이 진행됩니다. ")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 관련사례", use_container_width=True):
            st.session_state["loading"] = "case"
    
    with col2:
        if st.button("📜 법률정보", use_container_width=True):
            st.session_state["loading"] = "law"
    
    # 로고 또는 이미지 추가 (선택사항)
    st.markdown("---")
    
    # 기능 소개
    st.subheader("📋 기능 소개")
    st.markdown("""
    💬 **법률 상담**: AI 변호사와 법률 상담하기 \n
    🔎 **관련사례 검색**: 유사 사례 및 예상 결과 확인 \n 
    📚 **법률정보 검색**: 관련 법률 조항 및 정보 제공
    """)
    
    st.markdown("---")
    
    # 채팅 초기화 버튼
    st.subheader("💬 채팅 관리")
    if st.button("🔄 채팅 새로하기", use_container_width=True):
        # 완전히 새로운 챗봇 객체 생성 (기존 대화 내역 완전 초기화)
        st.session_state["chatbot"] = Agent(system_prompt=system_prompt, api_key=openai_api_key)
        # 표시되는 메시지 초기화
        st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 법률 상담이 필요하시면 질문해주세요."}]
        
        # 검색 결과 초기화
        st.session_state["case_result"] = None
        st.session_state["law_result"] = None
        
        # 페이지 새로고침
        st.rerun()

    
    
    # 하단 정보
    st.markdown("---")
    st.caption("고객센터: 02-1004-1004")
    st.caption("이메일: happy6team@skala.com")
    st.caption("운영시간: 연중무휴 24시간!")

if st.session_state["loading"]:
    with st.spinner("검색 중입니다... 잠시만 기다려 주세요.🙏"):
        summary = st.session_state["chatbot"].summarize_conversation()

        if summary.strip() == "질문 내용이 없습니다." or summary.strip() == "사용자가 질문을 입력하지 않았습니다.":   # Summary가 비어있는 경우 예외 처리
            st.warning("⚠️ 아무런 정보가 없습니다. 먼저 AI와 대화를 진행해 주세요.")
            st.session_state["loading"] = False  # 로딩 상태 초기화
        else:
            print(summary)
            if st.session_state["loading"] == "case":
                time.sleep(1) # 1초 대기
                st.session_state["case_result"] = web_rag_chain(f"{summary} 관련된 형량이나 벌금 정보")

            if st.session_state["loading"] == "law":
                time.sleep(1) # 1초 대기
                st.session_state["law_result"] = pdf_rag_chain.invoke(f"{summary} 관련된 법률 정보")

            st.session_state["loading"] = False  # 로딩 완료 후 상태 초기화

# ✅ 검색 결과 출력
if st.session_state["case_result"]:
    st.subheader("🔍 검색된 관련사례 및 예상결과")
    st.write(st.session_state["case_result"].content)  # 사례 정보 유지됨

if st.session_state["law_result"]:
    st.subheader("📚 검색된 법률정보")
    st.write(st.session_state["law_result"])  # 법률 정보 유지됨
