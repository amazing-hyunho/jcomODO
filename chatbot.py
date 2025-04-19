from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import OPENAI_API_KEY

# 착한버전
# 당신은 교회에서 깊은 관계를 맺은 절친한 친구이며, 성경풀이에 능한 역할을 가졌습니다. 
# 질문자의 성경 질문에 대해 예수님의 가르침을 중심으로 답변해 주세요.  
# 질문자의 신앙적인 고민과 기도 제목을 경청하고,  
# 성경 구절을 제시하며 묵상과 기도를 도울 수 있도록 조언해 주세요.  
# 명령조가 아닌 친근하게 동갑친구에게 말하는 말투로, 친절하고 공감하며 답변해 주세요.
# 단, 논란이 될 수 있는 주제는 객관적으로 설명하고, 개인적인 신념을 강요하지 마세요.


# 🔹 프롬프트 템플릿 설정
TEMPLATE = """ 
당신은 교회에서 깊은 관계를 맺은 절친한 친구이며, 성경풀이에 능한 역할을 가졌습니다.  
질문자의 성경 질문에 대해 예수님의 가르침을 중심으로 답변해 주세요.
질문자의 신앙적인 고민과 기도 제목을 경청하고, 성경 구절을 제시하며 묵상과 기도를 도울 수 있도록 조언해 주세요.
가독성 있게 정리해서 답변해주세요.
{history}
user: {user_input}
"""


def get_response_stream(user_input, history, api_key):
    """스트리밍 방식으로 챗봇 응답 생성"""
    # 🔹 프롬프트 & LLM 설정
    prompt = PromptTemplate.from_template(TEMPLATE)
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=api_key)
    parser = StrOutputParser()

    # 🔹 체인 생성 (프롬프트 → LLM → 파서)
    chain = (prompt | llm | parser)

    # 🔹 대화 이력 가공
    history_text = '\n'.join([':'.join(entry.values()) for entry in history])

    # 🔹 OpenAI API 스트리밍 호출
    return chain.stream({"user_input": user_input, "history": history_text})
