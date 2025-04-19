import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import pi
from chatbot import get_response_stream
from config import OPENAI_API_KEY

# 🌈 사역 카테고리 이모지 + 색상 정의
CATEGORIES = {
    "찬양": {"emoji": "🎵", "color": "#d6eaf8"},
    "음악": {"emoji": "🎸", "color": "#d6eaf8"},
    "봉사": {"emoji": "🧹", "color": "#f9e79f"},
    "섬김": {"emoji": "👐", "color": "#f9e79f"},
    "리더": {"emoji": "🔥", "color": "#fad7a0"},
    "인도": {"emoji": "🧭", "color": "#fad7a0"},
    "진행": {"emoji": "🎤", "color": "#fad7a0"},
    "기도": {"emoji": "🙏", "color": "#e8daef"},
    "중보": {"emoji": "🕊️", "color": "#e8daef"},
    "말씀": {"emoji": "📖", "color": "#d5f5e3"},
    "나눔": {"emoji": "💬", "color": "#d5f5e3"},
}

# 🔧 기본 설정
st.set_page_config(page_title="📖 제이컴 사역 추천 봇", layout="centered")
st.title("📖 제이컴 사역 추천 봇")
st.caption("MBTI와 분위기를 기반으로 사역을 추천해드릴게요. 😊")

# 💬 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "scores" not in st.session_state:
    st.session_state.scores = initialize_score()

# 🔁 기존 대화 표시
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        # 사역 키워드 매칭 및 이모지 삽입
        content = message["content"]
        bg_color = "#f0f0f0"
        for keyword, config in CATEGORIES.items():
            if keyword in content:
                content = content.replace(keyword, f'{config["emoji"]} **{keyword}**')
                bg_color = config["color"]
                st.session_state.scores[keyword] += 1  # 점수 추가
        st.markdown(f"""
        <div style="background-color: {bg_color}; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            {content}
        </div>
        """, unsafe_allow_html=True)

# 🧠 사용자 질문
if question := st.chat_input("각 순원들의 MBTI 정보와 순의 분위기를 입력해주세요."):
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        response = st.write_stream(get_response_stream(question, st.session_state.messages, OPENAI_API_KEY))

    # 대화 기록 저장
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({"role": "assistant", "content": response})

# 🔽 자동 스크롤
st.components.v1.html("""
<script>
    var body = window.parent.document.querySelector(".main");
    body.scrollTop = body.scrollHeight;
</script>
""", height=0)
