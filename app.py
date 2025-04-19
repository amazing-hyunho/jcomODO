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

# 📊 카테고리 레이더용 기본값 초기화
def initialize_score():
    return {category: 0 for category in CATEGORIES}

# 📊 레이더 차트 그리기
def render_radar_chart(scores):
    labels = list(scores.keys())
    values = list(scores.values())

    angles = [n / float(len(labels)) * 2 * pi for n in range(len(labels))]
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2, linestyle='solid', color='#5D6D7E')
    ax.fill(angles, values, '#AED6F1', alpha=0.4)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12)
    st.pyplot(fig)

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

# 📊 사역 성향 차트 시각화
with st.expander("📈 추천 사역 성향 차트 보기", expanded=True):
    st.markdown("사역 추천에 언급된 항목들을 시각화한 그래프입니다.")
    render_radar_chart(st.session_state.scores)

# 🔽 자동 스크롤
st.components.v1.html("""
<script>
    var body = window.parent.document.querySelector(".main");
    body.scrollTop = body.scrollHeight;
</script>
""", height=0)
