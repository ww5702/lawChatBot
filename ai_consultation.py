from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_KEY = os.environ.get('OPENAI_KEY')
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')
USER_AGENT = os.environ.get('USER_AGENT')

from openai import OpenAI
from agents.chat_agent import SYSTEM_PROMPT, Agent, interactive_law_consultation
import streamlit as st

# 페이지 제목
st.title("🚀 AI 법률 상담 챗봇입니다.")

# 서브 타이틀
st.subheader("당신의 고민을 해결해드립니다.")

# 소개 메시지
st.write("""
이 서비스는 사기, 폭행/상해, 교통사고, 이혼과 관련된 법률 상담을 제공합니다.
아래에서 원하는 상담 유형을 선택해주세요!
""")

# 세션 상태에서 카테고리 저장 (초기값: None)
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# 카테고리 선택 버튼 UI
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("⚖️ 사기"):
        st.session_state.selected_category = "사기"

with col2:
    if st.button("🛡️ 폭행/상해"):
        st.session_state.selected_category = "폭행/상해"

with col3:
    if st.button("🚗 교통사고"):
        st.session_state.selected_category = "교통사고"

with col4:
    if st.button("💔 이혼"):
        st.session_state.selected_category = "이혼"


# 카테고리가 선택되었을 때
if st.session_state.selected_category:
    # OpenAI 클라이언트 연결
    api_key = OPENAI_KEY
    client = OpenAI(api_key=api_key)

    print(f"✅ 선택된 카테고리: {st.session_state.selected_category}")

    print("\n[나만의 사고 AI 서비스 '🚀 사고닷 🚀' 법률 상담 챗봇] 상담을 시작합니다. (종료하려면 'exit' 입력)\n")
    # AI 에이전트 생성 
    abot = Agent(client,system_prompt=SYSTEM_PROMPT)
    interactive_law_consultation(abot,st.session_state.selected_category )

