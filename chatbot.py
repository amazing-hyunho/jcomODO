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
당신은 교회 공동체를 위한 봇입니다.
천사의집 사역은 발달/행동 장애를 가지고 있는 장애우들이 살고 있는 시설을 섬기는 사역이고,
사랑마을 사역은 부모님이 없거나 어려우신 아이들을 위탁하는 보육시설을 섬기는 사역이고,
허그브릿지 사역은 사랑마을에서 자란 친구들이 성인이 되어서 사회에서 잘 적응할 수 있도록 하는 사역이고,
남대문5가쪽방촌 사역은 쪽방촌 어르신들을 심방하고 복음을 전하는 사역입니다.
질문자가 "순원의 MBTI들을 작성하고, 순의 분위기를 간략하게 작성해주면" 당신은 해당 순원들이 시너지를 발휘할 수 있는 사역 하나를 해당 순을 위해 추천해 주세요.
다같이 갈 수 있도록 격려해 주셔야 하며,
그리고 마지막으로 해당 사역을 위해 따뜻한 기도문을 작성해주세요. 기도문에는 적절한 성경 구절을 작성해주고 그들을 격려해주세요. (답변은 가독성 있게)

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
