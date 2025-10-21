import os
import streamlit as st
from utils.ui import inject_base_css, header, top_banner
from utils.llm import gpt_answer

# ——— Sayfa yapılandırma ———
st.set_page_config(
    page_title="EconAI – Ekonomi Asistanı",
    page_icon=":bar_chart:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ——— Tema renkleri ———
PRIMARY = "#1E88E5"   # logo mavisi
INK = "#0F172A"       # lacivert/metin
BG = "#0B1020"        # koyu zemin
inject_base_css(primary=PRIMARY, ink=INK, bg=BG)

# ——— Üst kısım: logo ve sosyal bağlantılar ———
header(
    logo_path="assets/logo.png",
    links={
        "LinkedIn": "https://linkedin.com/in/yiğit-atay-55a5b6296",
        "GitHub": "https://github.com",
    },
)

# ——— Üst bant Lottie animasyonu (tam genişlikte) ———
top_banner("assets/header_lottie.json")

# ——— Sohbet geçmişi ———
if "chat" not in st.session_state:
    st.session_state.chat = [
        ("bot", "👋 Merhaba, ben **EconAI**! İktisat, finans ve ekonomi üzerine konuşabiliriz.")
    ]

# ——— Sohbet alanı ———
st.markdown("<div class='chatbox'>", unsafe_allow_html=True)
for role, msg in st.session_state.chat:
    who = "👤 Siz" if role == "user" else "🤖 EconAI"
    css = "chat-user" if role == "user" else "chat-bot"
    st.markdown(f"<div class='{css}'><b>{who}:</b> {msg}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ——— Giriş alanı ———
prompt = st.chat_input("Ekonomi veya finans sorunu yaz ve Enter’a bas…")
if prompt:
    st.session_state.chat.append(("user", prompt))
    ans = gpt_answer(prompt)
    st.session_state.chat.append(("bot", ans))
    st.rerun()
# ——— Not: Wikipedia API istemcisi utils/llm.py içinde tanımlı ———