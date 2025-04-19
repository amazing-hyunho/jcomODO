import streamlit as st
from chatbot import get_response_stream
from config import OPENAI_API_KEY  # API 키 로드

# 🔹 OpenAI API 키 입력 받기 (사이드바에서 입력 가능)
#key = st.sidebar.text_input('OPENAI API KEY', type='password', value=OPENAI_API_KEY)
key = True
# 🔹 API 키가 입력된 경우 실행
if key:
    st.title("📖 제이컴 사역 추천")

    # 🔹 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 🔹 이전 대화 기록 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # 🔹 사용자 입력 받기
    if question := st.chat_input("궁금한 성경 지식을 입력하세요:"):
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            # 🔹 스트리밍 응답 출력
            response = st.write_stream(get_response_stream(question, st.session_state.messages, OPENAI_API_KEY))

        # 🔹 세션 상태에 대화 저장
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": response})
# 🔹 자동 스크롤 스크립트
js = '''
<script>
    var body = window.parent.document.querySelector(".main");
    body.scrollTop = 0;
</script>
'''
st.components.v1.html(js)
