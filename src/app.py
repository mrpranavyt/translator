import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Nepali & Sinhala Translator",
    page_icon="🌐",
    layout="centered"
)

# ---------------- GLOBAL STYLES ----------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0f172a, #020617);
}
.main-card {
    background: rgba(30, 41, 59, 0.65);
    backdrop-filter: blur(14px);
    border-radius: 20px;
    padding: 35px;
    box-shadow: 0 30px 80px rgba(0,0,0,0.45);
}
.title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}
.result-box {
    background: linear-gradient(135deg, #064e3b, #022c22);
    padding: 18px;
    border-radius: 14px;
    color: #d1fae5;
    font-size: 18px;
}
.example-chip {
    background: #1e293b;
    border-radius: 18px;
    padding: 6px 14px;
    display: inline-block;
    margin-right: 8px;
    cursor: pointer;
}
.footer {
    text-align: center;
    color: #64748b;
    margin-top: 30px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD API ----------------
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------- FUNCTIONS ----------------
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

# ---------------- UI ----------------
st.markdown("<div class='main-card'>", unsafe_allow_html=True)

st.markdown("<div class='title'>🌐 Nepali & Sinhala Translator</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>AI-powered translation using Gemini Large Language Model</div>",
    unsafe_allow_html=True
)

text = st.text_area(
    "Enter Nepali or Sinhala text",
    height=140,
    placeholder="म आज धेरै खुशी छु\n\nමම පරිගණක විද්‍යාව ඉගෙන ගන්නවා"
)

# ---- Example Buttons ----
st.markdown("**Try examples:**")
col1, col2, col3 = st.columns(3)

if col1.button("🇳🇵 Nepali"):
    text = "म आज धेरै खुशी छु"

if col2.button("🇱🇰 Sinhala"):
    text = "මම පරිගණක විද්‍යාව ඉගෙන ගන්නවා"

if col3.button("👋 Greeting"):
    text = "ඔබට කොහොමද"

# ---- Translate Button ----
st.markdown("<br>", unsafe_allow_html=True)
translate_btn = st.button("🚀 Translate", use_container_width=True)

if translate_btn and text.strip():
    lang = detect_language(text)
    st.markdown(f"**Detected:** {lang}")

    with st.spinner("Translating with Gemini..."):
        output = translate(text)

    st.markdown("<br><b>English Translation</b>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-box'>{output}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown(
    "<div class='footer'>Professional AIML Project • Gemini LLM • Streamlit</div>",
    unsafe_allow_html=True
)
