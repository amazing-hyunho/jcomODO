import streamlit as st
import pandas as pd
import numpy as np
from math import pi
from chatbot import get_response_stream
from config import OPENAI_API_KEY

# 🔧 기본 설정
st.set_page_config(page_title="의성 어르신", layout="centered")

st.title("의성 어르신")
st.caption("😊")

# 💬 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

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
        st.markdown(f"""
        <div style="background-color: {bg_color}; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            {content}
        </div>
        """, unsafe_allow_html=True)

# 🧠 사용자 질문
if question := st.chat_input(""):
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
