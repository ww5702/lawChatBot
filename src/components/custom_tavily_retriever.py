from tavily import TavilyClient
from langchain_core.documents import Document

class CustomTavilyRetriever:
    def __init__(self, k=3):
        self.k = k
        self.client = TavilyClient()  # 환경변수 TAVILY_API_KEY 사용

    def get_relevant_documents(self, query: str) -> list[Document]:
        response = self.client.search(query=query, max_results=self.k)
        return [
            Document(page_content=result["content"], metadata={"source": result["url"]})
            for result in response["results"]
        ]
