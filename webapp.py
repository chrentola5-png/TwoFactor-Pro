import streamlit as st
import pyotp
import pytz
from datetime import datetime

# --- 1. Page Configuration ---
st.set_page_config(page_title="TwoFactor Pro", page_icon="🔐", layout="centered")

# --- 2. CSS Styling (Clean & Professional) ---
st.markdown("""
    <style>
    /* Background Color */
    .stApp { background-color: #f0f2f6; }
    
    /* Input & Output Text Areas */
    .stTextArea textarea {
        background-color: white !important;
        border: 1px solid #ccc !important;
        border-radius: 5px;
        color: black !important;
        font-family: monospace;
    }

    /* Submit Button */
    div.stButton > button {
        background-color: #007bff !important; /* Blue color like 2Fa.Live */
        color: white !important;
        font-weight: bold;
        border: none;
        width: 100%;
        padding: 10px;
        border-radius: 5px;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: #0056b3 !important;
    }

    /* Remove Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. Header & Clock ---
tz = pytz.timezone('Asia/Phnom_Penh')
current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

st.markdown(f"""
    <div style="background-color: #E91E63; padding: 15px; border-radius: 8px 8px 0 0; 
                display: flex; justify-content: space-between; align-items: center; color: white; margin-bottom: 20px;">
        <div style="font-size: 20px; font-weight: bold;">TwoFactor <span style="color:#ffeb3b;">Live</span></div>
        <div style="font-size: 14px; font-family: monospace;">{current_time}</div>
    </div>
""", unsafe_allow_html=True)

# --- 4. Logic & Session State ---
if 'output_code' not in st.session_state:
    st.session_state.output_code = ""

# === BOX 1: INPUT ===
st.markdown("### 2FA Secret")
st.caption("Get code for two factor authentication easiest - Please store your 2FA secret safely")
secret_input = st.text_area("input_label", height=150, label_visibility="collapsed", placeholder="Example: JBSWY3DPEHPK3PXP...")

# === BUTTON: SUBMIT ===
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
                    results.append(code)
                except:
                    results.append("Invalid Key")
        
        # Save to session state to display in the second box
        st.session_state.output_code = "\n".join(results)
    else:
        st.warning("Please enter your secret key first.")

# === BOX 2: OUTPUT ===
st.markdown("### 2FA Code")
st.caption("2-step verification code")

# Display the result in a text area (Copyable)
st.text_area("output_label", value=st.session_state.output_code, height=150, label_visibility="collapsed", placeholder="The code will appear here...")

# Quick Copy Button (Optional but useful)
if st.session_state.output_code:
    st.markdown("---")
    st.caption("Click to copy codes:")
    st.code(st.session_state.output_code, language="text")

# --- Footer ---
st.markdown("""
    <div style="text-align: center; margin-top: 40px; border-top: 1px solid #ccc; padding-top: 10px;">
        <p style="color: grey; font-size: 12px;">© 2026 TwoFactor Pro. All rights reserved.</p>
        <a href="https://t.me/empunlok787" target="_blank" style="text-decoration: none; color: #0088cc; font-weight: bold; margin-right: 15px;">Telegram</a>
        <a href="https://www.facebook.com/empunlok99" target="_blank" style="text-decoration: none; color: #1877F2; font-weight: bold;">Facebook</a>
    </div>
""", unsafe_allow_html=True)