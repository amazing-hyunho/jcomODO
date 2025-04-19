import os
import streamlit as st
from dotenv import load_dotenv

# 🔹 .env 파일 로드 (로컬 환경)
load_dotenv()

# 🔹 Streamlit Cloud인지 로컬인지 체크 후 API 키 불러오기
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]  # Streamlit Cloud 환경
except Exception:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # 로컬 환경 (.env 사용)

# 🔹 API 키가 없을 경우 오류 발생 방지
if not OPENAI_API_KEY:
    raise ValueError("🚨 API 키가 설정되지 않았습니다! .env 파일 또는 Streamlit Secrets를 확인하세요.")
