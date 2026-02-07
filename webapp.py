import streamlit as st
import pyotp
import pytz
from datetime import datetime

# --- 1. Page Configuration (ប្តូរឈ្មោះ Tab មកដើមវិញ) ---
st.set_page_config(page_title="TwoFactor Pro", page_icon="🔐", layout="centered")

# --- 2. CSS Styling (Blue & White Theme) ---
st.markdown("""
    <style>
    /* Background Color */
    .stApp { background-color: #ffffff; }
    
    /* Text Area Styling */
    .stTextArea textarea {
        background-color: white !important;
        border: 1px solid #ced4da !important;
        border-radius: 4px;
        color: #495057 !important;
        font-family: monospace;
        font-size: 16px;
    }

    /* Blue Buttons */
    div.stButton > button {
        background-color: #0d6efd !important;
        color: white !important;
        font-weight: 500;
        border: none;
        padding: 0.375rem 0.75rem;
        border-radius: 0.25rem;
        font-size: 1rem;
        width: 100%;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background-color: #0b5ed7 !important;
    }
    
    /* Labels Styling */
    .label-style {
        font-size: 16px;
        color: #212529;
        margin-bottom: 5px;
    }
    .bold-text { font-weight: bold; }

    /* Hide Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. Header (ប្តូរឈ្មោះមក TwoFactor Pro វិញ) ---
st.markdown("""
    <h2 style='text-align: center; color: #333; margin-bottom: 30px;'>
        TwoFactor <span style='color: #0d6efd;'>Pro</span> <span style='font-size: 14px; color: grey; font-weight: normal;'>Online Tool</span>
    </h2>
""", unsafe_allow_html=True)

# --- 4. Logic & Session State ---
if 'output_code' not in st.session_state:
    st.session_state.output_code = ""

# === BOX 1: INPUT ===
st.markdown("""
    <div class="label-style">
        <span class="bold-text">* Secret Keys</span> (Paste your keys here)
    </div>
""", unsafe_allow_html=True)

secret_input = st.text_area("input_label", height=150, label_visibility="collapsed", placeholder="Example: BK5V TVQ7 D2RB...")

# === BUTTON: SUBMIT ===
col_submit, col_dummy = st.columns([1, 4])
with col_submit:
    if st.button("Generate Code"):
        if secret_input.strip():
            keys = secret_input.strip().split('\n')
            results = []
            for key in keys:
                key = key.strip()
                if key:
                    try:
                        totp = pyotp.TOTP(key.replace(" ", ""))
                        results.append(totp.now())
                    except:
                        results.append("Invalid Key")
            st.session_state.output_code = "\n".join(results)

# === BOX 2: OUTPUT (Fixed Size) ===
st.write("")
st.markdown("""
    <div class="label-style">
        <span class="bold-text">* 2FA Codes</span> (Result)
    </div>
""", unsafe_allow_html=True)

st.text_area("output_label", 
             value=st.session_state.output_code, 
             height=150, 
             label_visibility="collapsed", 
             placeholder="Codes will appear here...", 
             disabled=False)

# === BOX 3: BLUE COPY BUTTONS ===
st.write("")
col1, col2, col3 = st.columns([1, 1, 3])

with col1:
    if st.button("Copy"):
        st.toast("Please copy manually from the box above.", icon="ℹ️")

with col2:
    if st.button("Copy Code"):
        st.toast("Please copy manually from the box above.", icon="ℹ️")

# --- Footer (ដាក់ឈ្មោះម្ចាស់ដើម) ---
st.markdown("""
    <div style="text-align: center; margin-top: 50px; border-top: 1px solid #eee; padding-top: 20px;">
        <p style="color: grey; font-size: 12px;">© 2026 TwoFactor Pro. Created by EM PUNLOK.</p>
    </div>
""", unsafe_allow_html=True)