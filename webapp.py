import streamlit as st
import pyotp
import pytz
from datetime import datetime

# --- 1. Page Configuration ---
st.set_page_config(page_title="TwoFactor Live", page_icon="🔐", layout="centered")

# --- 2. CSS Styling (Like 2Fa.Live) ---
st.markdown("""
    <style>
    /* Background Color */
    .stApp { background-color: #ffffff; }
    
    /* Input & Output Text Areas */
    .stTextArea textarea {
        background-color: white !important;
        border: 1px solid #ced4da !important;
        border-radius: 4px;
        color: #495057 !important;
        font-family: monospace;
    }

    /* Blue Submit Button (Like 2Fa.Live) */
    div.stButton > button {
        background-color: #0d6efd !important;
        color: white !important;
        font-weight: 500;
        border: none;
        padding: 0.375rem 0.75rem;
        border-radius: 0.25rem;
        font-size: 1rem;
        transition: color .15s ease-in-out,background-color .15s ease-in-out;
    }
    div.stButton > button:hover {
        background-color: #0b5ed7 !important;
    }

    /* Labels styling */
    .label-style {
        font-size: 16px;
        font-weight: normal;
        margin-bottom: 5px;
        color: #212529;
    }
    .bold-text { font-weight: bold; }
    
    /* Remove Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. Header ---
# Simple header like the website
st.markdown("""
    <h2 style='text-align: center; color: #333; margin-bottom: 30px;'>
        2Fa.Live <span style='font-size: 14px; color: grey; font-weight: normal;'>Two Factor Authenticator</span>
    </h2>
""", unsafe_allow_html=True)

# --- 4. Logic & Session State ---
if 'output_code' not in st.session_state:
    st.session_state.output_code = ""

# === BOX 1: INPUT ===
st.markdown("""
    <div class="label-style">
        <span class="bold-text">* 2FA Secret</span> Get code for two factor authentication easiest - Please store your 2FA secret safely
    </div>
""", unsafe_allow_html=True)

secret_input = st.text_area("input_label", height=150, label_visibility="collapsed", placeholder="BK5V TVQ7 D2RB...")

# === BUTTON: SUBMIT ===
st.write("") # Spacer
if st.button("Submit"):
    if secret_input.strip():
        keys = secret_input.strip().split('\n')
        results = []
        for key in keys:
            key = key.strip()
            if key:
                try:
                    totp = pyotp.TOTP(key.replace(" ", ""))
                    code = totp.now()
                    # Format: 000 000 (with space) or just 000000
                    results.append(code)
                except:
                    results.append("Invalid Key")
        
        # Save to session state
        st.session_state.output_code = "\n".join(results)

# === BOX 2: OUTPUT ===
st.write("") # Spacer
st.markdown("""
    <div class="label-style">
        <span class="bold-text">* 2FA Code</span> 2-step verification code
    </div>
""", unsafe_allow_html=True)

# Display result
st.text_area("output_label", value=st.session_state.output_code, height=150, label_visibility="collapsed", placeholder="The code will appear here...")

# === COPY BUTTON ===
if st.session_state.output_code:
    st.write("")
    st.caption("Click the icon below to copy:")
    st.code(st.session_state.output_code, language="text")

# --- Footer ---
st.markdown("""
    <div style="text-align: center; margin-top: 50px; border-top: 1px solid #eee; padding-top: 20px;">
        <p style="color: grey; font-size: 12px;">© 2026 TwoFactor Live Clone. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)