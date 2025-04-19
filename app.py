import streamlit as st
from chatbot import get_response_stream
from config import OPENAI_API_KEY  # API 키 로드

# 🔧 페이지 설정
st.set_page_config(page_title="📖 제이컴 사역 추천 봇", layout="centered")

# 💄 스타일 커스터마이징
st.markdown("""
    <style>
    /* 전체 배경색 */
    body {
        background-color: #f9f6f2;
    }
    /* 메인 컨테이너 */
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
    }
    /* 챗버블 스타일 */
    .stChatMessage {
        margin-bottom: 1.5rem;
    }
    .stChatMessage div[data-testid="stVerticalBlock"] {
        background-color: #f0f0f0;
        padding: 1rem;
        border-radius: 10px;
    }
    .stChatMessage.user div[data-testid="stVerticalBlock"] {
        background-color: #d6eaf8;
        text-align: right;
    }
    .stChatMessage.assistant div[data-testid="stVerticalBlock"] {
        background-color: #fceecf;
    }
    /* 입력창 크기 조절 */
    .stTextInput>div>div>input {
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ 키 입력 생략 (key를 True로 설정)
key = True

if key:
    st.title("📖 제이컴 사역 추천 봇")
    st.caption("순원들의 MBTI와 순 분위기를 알려주시면, 알맞은 사역을 추천해드려요!")

    # 💬 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 🔁 이전 대화 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ✍️ 사용자 입력 받기
    if question := st.chat_input("각 순원들의 MBTI 정보와 순의 분위기를 입력해주세요."):
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            response = st.write_stream(get_response_stream(question, st.session_state.messages, OPENAI_API_KEY))

        # 💾 대화 저장
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": response})

# 📜 자동 스크롤 스크립트 (선택사항)
st.components.v1.html("""
<script>
    var body = window.parent.document.querySelector(".main");
    body.scrollTop = body.scrollHeight;
</script>
""", height=0)
