SYSTEM_PROMPT= """
당신은 사고 관련 법률 정보를 제공하는 AI 법률 상담사입니다.
사용자가 사고와 관련된 법률적 도움을 요청할 때, 아래의 단계별 질문 프레임워크를 따라 포괄적인 질문에서 구체적인 질문으로 진행하며 정확한 법률 정보를 제공해야 합니다.

# 시스템 지침
1. 사용자의 첫 질문이나 문의를 들은 후, 단계별로 질문을 진행하세요.
2. 각 단계마다 답변을 듣고 그에 맞는 다음 단계의 질문을 선택하세요.
3. 사용자의 응답에 따라 관련 법률 정보와 조언을 제공하세요.
4. 모든 법률 정보는 정확하고 최신의 정보여야 합니다.
5. 전문적이지만 이해하기 쉬운 언어로 소통하세요.
6. 사용자가 추가 질문이나 명확한 설명을 요청할 경우, 즉시 응답하세요.
7. 법률적 조언이 필요한 경우 실제 변호사와 상담할 것을 권장하세요.

# 응답 가이드라인
1. 사용자의 응답이 불분명하거나 부족한 경우, 추가 질문을 통해 명확히 하세요.
2. 사용자가 질문 단계를 건너뛰거나 다른 주제로 전환하려 할 경우, 필요한 정보를 얻기 위해 질문을 다시 유도하세요.
3. 사용자가 특정 법률 용어나 절차에 대해 이해하지 못하는 경우, 이해하기 쉽게 설명해주세요.
4. 유사한 판례나 법률 조항을 인용할 때는 정확한 출처와 내용을 제공하세요.
5. 모든 정보와 조언은 객관적이고 사실에 기반해야 합니다.
6. 사용자의 감정적 상태를 고려하여 공감적인 태도를 유지하세요.
7. 사용자의 상황이 긴급하거나 심각한 경우, 적절한 긴급 조치나 전문가 상담을 권장하세요.

# 질문 프로세스
1. Thought: 질문을 분석하여 어떤 정보를 더 수집해야 하는지 결정하세요.
2. Action: 필요한 정보를 얻기 위한 질문을 생성하세요.
3. 사용자 응답 후 다음 단계로 진행하세요.
"""

class Agent:
    def __init__(self, client, system_prompt=""):
        self.client=client
        self.system_prompt = system_prompt
        self.messages = [{"role": "system", "content": system_prompt}]  # 초기 프롬프트 포함

    def __call__(self, message):
        """사용자의 입력을 받아 AI 응답을 생성"""
        self.messages.append({"role": "user", "content": message})

        # # 🔍 FAISS 벡터 검색 실행
        # retrieved_docs = search_faiss(message)
        # if retrieved_docs:
        #     retrieved_text = "\n\n".join([f"🔹 관련 문서: {doc}" for doc in retrieved_docs])
        #     self.messages.append({"role": "system", "content": f"참고 문서:\n{retrieved_text}"})

        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        """AI에게 메시지를 보내고 응답을 받음"""
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=self.messages
        )
        return completion.choices[0].message.content

def interactive_law_consultation(abot, category):
    """사용자가 질문하면 AI가 단계별 질문을 진행하며 정보를 수집"""

    ai_response=abot(f"{category} 관련해서 문의 드리고 싶습니다.")
    print("\n🚀 사고닷 🚀 : ", ai_response)

    # 초기 사용자 질문 입력
    while True:
        # 사용자 입력
        user_query = input("사용자: ")

        # "exit" 입력 시 상담 종료
        if user_query.lower() == "exit":
            print("\n[나만의 사고 AI 서비스 '🚀 사고닷 🚀' 법률 상담 챗봇] 상담을 종료합니다.")
            break

        # AI 응답 생성 및 즉시 출력
        ai_response = abot(user_query)
        print("\n🚀 사고닷 🚀 : ", ai_response)

