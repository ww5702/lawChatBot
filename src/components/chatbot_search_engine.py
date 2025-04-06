import time
import streamlit as st
from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from .chatbot_setup import load_prompt
from .chatbot_db_manager import load_chroma_db, format_docs

@st.cache_data(show_spinner=False)
def web_search(query):
    """Perform web search using Tavily API"""
    retriever = TavilySearchAPIRetriever(
        k=3, 
        search_depth="advanced", 
        include_domains=["news"], 
        verbose=False
    )
    return retriever.invoke(query)

def web_rag_chain(query, llm):
    """Create RAG chain for web search results"""
    # Load web RAG prompt
    web_prompt_template = ChatPromptTemplate.from_template(load_prompt("web_rag_prompt.txt"))
    
    # Perform search and format results
    search_results = web_search(query)
    formatted_results = format_docs(search_results)
    
    # Create final prompt and invoke LLM
    final_prompt = web_prompt_template.format(context=formatted_results, question=query)
    
    time.sleep(1)
    return llm.invoke(final_prompt)

def create_pdf_rag_chain(llm):
    """Create RAG chain for PDF documents"""
    db = load_chroma_db()
    retriever = db.as_retriever()
    
    # Load PDF RAG prompt
    pdf_prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template=load_prompt("pdf_rag_prompt.txt")
    )
    
    # Create and return the RAG chain
    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | pdf_prompt_template
        | llm
        | StrOutputParser()
    )

def process_searches(llm):
    """Process search requests based on loading state"""
    if st.session_state["loading"]:
        with st.spinner("검색 중입니다... 잠시만 기다려 주세요.🙏"):
            # Get conversation summary
            summary = st.session_state["chatbot"].summarize_conversation()
            
            # Check if summary is empty
            if summary.strip() == "질문 내용이 없습니다." or summary.strip() == "사용자가 질문을 입력하지 않았습니다.":
                st.warning("⚠️ 아무런 정보가 없습니다. 먼저 AI와 대화를 진행해 주세요.")
                st.session_state["loading"] = False
            else:
                print(summary)
                
                # Handle case search
                if st.session_state["loading"] == "case":
                    time.sleep(1)
                    st.session_state["case_result"] = web_rag_chain(f"{summary} 관련된 형량이나 벌금 정보", llm)
                
                # Handle law search
                if st.session_state["loading"] == "law":
                    time.sleep(1)
                    pdf_rag_chain = create_pdf_rag_chain(llm)
                    st.session_state["law_result"] = pdf_rag_chain.invoke(f"{summary} 관련된 법률 정보")
                
                # Reset loading state
                st.session_state["loading"] = False
