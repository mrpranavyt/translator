import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
import re

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Nepali & Sinhala Translator",
    page_icon="🌐",
    layout="centered"
)

# ---------------- LOAD API ----------------
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------- UTILS ----------------
def detect_language(text):
    if re.search(r"[\u0900-\u097F]", text):
        return "Nepali 🇳🇵"
    if re.search(r"[\u0D80-\u0DFF]", text):
        return "Sinhala 🇱🇰"
    return "Unknown"

def translate(text):
    prompt = f"""
Translate the following text to English.
The text may be in Nepali or Sinhala.
Return ONLY the English translation.

Text:
{text}
"""
    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )
    return response.text.strip() if response and response.text else "No translation returned."

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🌐 Translator App")
    st.markdown("**Nepali & Sinhala → English**")
    st.markdown("---")
    st.markdown("### 🔧 Tech Stack")
    st.markdown("- Python")
    st.markdown("- Gemini LLM")
    st.markdown("- Streamlit")
    st.markdown("---")
    st.markdown("👨‍🎓 AIML Academic Project")

# ---------------- MAIN UI ----------------
st.markdown(
    "<h1 style='text-align:center;'>Nepali & Sinhala → English</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:gray;'>AI-powered text translation using Gemini LLM</p>",
    unsafe_allow_html=True
)

st.markdown("### ✍️ Enter Text")
user_input = st.text_area(
    "",
    height=140,
    placeholder="म आज धेरै खुशी छु\n\nමම පරිගණක විද්‍යාව ඉගෙන ගන්නවා"
)

if user_input.strip():
    detected = detect_language(user_input)
    st.info(f"Detected Language: **{detected}**")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    translate_btn = st.button("🚀 Translate", use_container_width=True)

if translate_btn:
    if not user_input.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Translating with Gemini..."):
            result = translate(user_input)

        st.markdown("### ✅ English Translation")
        st.success(result)

        st.code(result, language="text")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#9ca3af;'>"
    "Professional AIML Project • Gemini LLM • Streamlit UI"
    "</p>",
    unsafe_allow_html=True
)
