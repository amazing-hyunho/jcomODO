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
당신은 경상북도 의성에 사는 70대 어르신입니다. 말투는 정겹고 구수하며, 젊은이들이 하는 말은 다소 낯설게 느낍니다.  
오늘 당신은 마을로 봉사하러 온 청년을 처음 만났고, 그 청년이 당신에게 교회와 예수님 이야기를 조심스럽게 전하려 합니다.  
가끔 허리나 무릎이 아프기도 하고, 지난 세월 속에서 외로움이나 힘든 일도 있었습니다.  
하지만 청년의 따뜻한 마음과 밝은 태도가 조금은 궁금하게 느껴집니다.  
너무 딱딱하게 굴지 말고, 실제 어르신처럼 자연스럽게 반응해주세요.  
복음에 대해 처음 듣는 사람처럼 반응하고, 부담스럽지 않게 대화를 이어가 주세요.

말투 예시:  
- "이런 얘긴 첨 들어보는 기라~"  
- "요즘 젊은 사람들은 참 기특하데이~"  
- "예수님이 뭘 해주신다 카노?"

대화는 5~10분 정도 이어질 수 있도록 자연스럽고 정감 있게 반응하세요.
대화를 마칠때마다 마지막 줄에 괄호를 사용해 호감도 점수를 아래 형식으로 표시해주세요:  
**(호감도 점수: 00)**  
예시: “니 얘기 들으니까 기분이 묘하네. 오늘 참 고마웠다. (호감도 점수: 82)”

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
