import streamlit as st
from chatbot import get_response_stream
from config import OPENAI_API_KEY

# ✅ 사역 카테고리별 색상 맵
CATEGORY_COLOR_MAP = {
    "찬양": "#d6eaf8",    # 하늘색
    "음악": "#d6eaf8",
    "봉사": "#f9e79f",    # 노랑
    "섬김": "#f9e79f",
    "리더": "#fad7a0",    # 주황
    "인도": "#fad7a0",
    "진행": "#fad7a0",
    "기도": "#e8daef",    # 연보라
    "중보": "#e8daef",
    "말씀": "#d5f5e3",    # 연두
    "나눔": "#d5f5e3",
}

# 🔧 페이지 설정
st.set_page_config(page_title="📖 제이컴 사역 추천 봇", layout="centered")

# 💄 기본 CSS (유저 챗버블 포함)
st.markdown("""
    <style>
    body {
        background-color: #f9f6f2;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
    }
    .stChatMessage {
        margin-bottom: 1.5rem;
    }
    .stChatMessage.user div[data-testid="stVerticalBlock"] {
        background-color: #d6eaf8;
        text-align: right;
        border-radius: 10px;
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# 🧠 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔑 API 키 조건 생략
key = True

if key:
    st.title("📖 제이컴 사역 추천 봇")
    st.caption("MBTI와 순 분위기를 알려주시면 적절한 사역을 추천해드려요!")

    # 🔁 기존 메시지 출력
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            # 사역 키워드 찾기
            matched = next((color for keyword, color in CATEGORY_COLOR_MAP.items() if keyword in message["content"]), "#f0f0f0")

            # 다이내믹 스타일 삽입
            st.markdown(f"""
            <div style="background-color: {matched}; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)

    # ✍️ 사용자 입력
    if question := st.chat_input("각 순원들의 MBTI 정보와 순의 분위기를 입력해주세요."):
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            response = st.write_stream(get_response_stream(question, st.session_state.messages, OPENAI_API_KEY))

        # 💾 대화 저장
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": response})

# 📜 자동 스크롤
st.components.v1.html("""
<script>
    var body = window.parent.document.querySelector(".main");
    body.scrollTop = body.scrollHeight;
</script>
""", height=0)
