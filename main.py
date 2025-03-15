from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_KEY = os.environ.get('OPENAI_KEY')
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')
USER_AGENT = os.environ.get('USER_AGENT')

import requests
from bs4 import BeautifulSoup
import os

import fitz  # PyMuPDF 라이브러리

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from openai import OpenAI

from langchain_openai import ChatOpenAI
from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.schema import Document

from rawChatBot.agents.chat_agent import SYSTEM_PROMPT, Agent, interactive_law_consultation

# OpenAI 클라이언트 연결
api_key = OPENAI_KEY
client = OpenAI(api_key=api_key)

# AI 상담 Agent 생성
abot = Agent(client, system_prompt=SYSTEM_PROMPT)

# **실행**
interactive_law_consultation(abot)