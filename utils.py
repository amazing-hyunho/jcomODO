import streamlit as st
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY

def check_openai_api_key(key):
    """OpenAI API 키 유효성 검사"""
    try:
        llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=key)
        llm.invoke('API 키 테스트 중...')
        del llm
        return True
    except Exception as e:
        st.sidebar.error(f"🔴 API 키 오류: {e}")
        return False