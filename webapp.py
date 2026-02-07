import streamlit as st
import pyotp
import pytz
from datetime import datetime

# --- 1. Page Configuration ---
st.set_page_config(page_title="TwoFactor Live", page_icon="🔐", layout="centered")

# --- 2. CSS Styling (Clean & Professional) ---
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

    /* Blue Submit Button */
    div.stButton > button {
        background-color: #0d6efd !important;
        color: white !important;
        font-weight: 500;
        border: none;
        padding: 0.375rem 0.75rem;
        border-radius: 0.25rem;
        font-size: 1rem;
        width: 100%;
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
    
    /* Hide Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. Header ---
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

secret_input = st.text_area("input_label", height=150, label_visibility="collapsed", placeholder="Example: BK5V TVQ7 D2RB...")

# === BUTTONS: SUBMIT & CLEAR ===
col1, col2 = st.columns([4, 1])
with col1:
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
            st.session_state.output_code = "\n".join(results)
        else:
            st.warning("Please enter your secret key first.")

with col2:
    if st.button("Clear"):
        st.session_state.output_code = ""
        st.rerun()

# === BOX 2: OUTPUT (VISUAL ONLY) ===
st.write("")
st.markdown("""
    <div class="label-style">
        <span class="bold-text">* 2FA Code</span> 2-step verification code
    </div>
""", unsafe_allow_html=True)

# បង្ហាញលទ្ធផលក្នុង Text Area (ដើម្បីឱ្យស្អាតដូច input)
st.text_area("output_display", value=st.session_state.output_code, height=150, label_visibility="collapsed", placeholder="The code will appear here...", disabled=True)

# === BOX 3: COPY SECTION (នៅខាងក្រោម) ===
# នេះជាកន្លែង Copy នៅខាងក្រោមប្រអប់ ដូចដែលអ្នកចង់បាន
if st.session_state.output_code:
    st.write("") # ចន្លោះ
    st.info("👇 **Click the copy icon below:**") # ដាក់សញ្ញាប្រាប់
    st.code(st.session_state.output_code, language="text")

# --- Footer ---
st.markdown("""
    <div style="text-align: center; margin-top: 50px; border-top: 1px solid #eee; padding-top: 20px;">
        <p style="color: grey; font-size: 12px;">© 2026 TwoFactor Live Clone. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)