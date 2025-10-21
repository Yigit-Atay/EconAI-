import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie

def inject_base_css(primary="#1E88E5", ink="#0F172A", bg="#0B1020"):
    """Koyu arka plan ve okunaklı chat görünümü için CSS."""
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(180deg, {bg} 0%, #0E1324 100%);
        color: #E2E8F0;
        font-family: 'Segoe UI', sans-serif;
    }}
    .econ-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 14px;
        margin-bottom: 10px;
    }}
    .econ-left {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .econ-left img {{
        width: 45px;
        height: auto;
        border-radius: 6px;
    }}
    .econ-title {{
        font-weight: 700;
        font-size: 1.3rem;
        color: #E8EEF8;
    }}
    .econ-links a {{
        color: {primary};
        margin-left: 12px;
        text-decoration: none;
        font-weight: 500;
    }}
    .econ-links a:hover {{
        text-decoration: underline;
    }}
    .chatbox {{
        max-height: 520px;
        overflow-y: auto;
        padding: 14px;
        border-radius: 14px;
        background: rgba(255,255,255,0.05);
        box-shadow: 0 0 12px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
    }}
    .chat-user {{
        background: rgba(255,255,255,0.12);
        color: #F0F4F8;
        padding: 8px 10px;
        border-radius: 10px;
        margin: 6px 0;
    }}
    .chat-bot {{
        background: rgba(0,0,0,0.4);
        color: #E2E8F0;
        padding: 8px 10px;
        border-radius: 10px;
        margin: 6px 0;
    }}
    footer {{visibility:hidden}}
    </style>
    """, unsafe_allow_html=True)

def _load_lottie(source):
    try:
        if source.startswith("http"):
            r = requests.get(source, timeout=10)
            if r.status_code == 200:
                return r.json()
        else:
            with open(source, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        return None

def header(logo_path, links=None):
    """Küçük logo sol üstte, sağda sosyal bağlantılar."""
    st.markdown("<div class='econ-header'>", unsafe_allow_html=True)
    st.markdown("<div class='econ-left'>", unsafe_allow_html=True)
    st.image(logo_path, width=45)  # 🟢 düzeltildi: artık width parametresiyle
    st.markdown("<div class='econ-title'>EconAI</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    if links:
        link_html = " ".join([f"<a href='{v}' target='_blank'>{k}</a>" for k, v in links.items()])
        st.markdown(f"<div class='econ-links'>{link_html}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def top_banner(lottie_path):
    """Tam genişlikte Lottie banner."""
    data = _load_lottie(lottie_path)
    if data:
        st_lottie(data, height=160, width="stretch", key="top-banner", speed=1, loop=True)
