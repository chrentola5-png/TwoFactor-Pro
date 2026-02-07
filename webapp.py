import streamlit as st
import pyotp
import pytz
from datetime import datetime

# --- 1. Page Configuration ---
st.set_page_config(page_title="TwoFactor Live", page_icon="🔐", layout="centered")

# --- 2. CSS Styling (ដូច 2Fa.Live 100%) ---
st.markdown("""
    <style>
    /* Background Color */
    .stApp { background-color: #ffffff; }
    
    /* Input Text Area Styling */
    .stTextArea textarea {
        background-color: white !important;
        border: 1px solid #ced4da !important;
        border-radius: 4px;
        color: #495057 !important;
        font-family: monospace;
    }

    /* Blue Buttons (Submit, Copy, Copy Code) */
    div.stButton > button {
        background-color: #0d6efd !important; /* Blue color like 2fa.live */
        color: white !important;
        font-weight: 500;
        border: none;
        padding: 0.375rem 0.75rem;
        border-radius: 0.25rem;
        font-size: 1rem;
        width: 100%; /* Full width for Copy buttons */
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background-color: #0b5ed7 !important;
    }

    /* Output Box Styling (st.code) to look like Text Area */
    .stCode {
        background-color: white !important;
        border: 1px solid #ced4da !important;
        border-radius: 4px !important;
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

secret_input = st.text_area("input_label", height=150, label_visibility="collapsed", placeholder="BK5V TVQ7 D2RB...")

# === BUTTON: SUBMIT (Small Blue Button) ===
col_submit, col_dummy = st.columns([1, 4]) # Make button small aligned left
with col_submit:
    if st.button("Submit"):
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

# === BOX 2: OUTPUT ===
st.write("")
st.markdown("""
    <div class="label-style">
        <span class="bold-text">* 2FA Code</span> 2-step verification code
    </div>
""", unsafe_allow_html=True)

# បង្ហាញលទ្ធផលក្នុង st.code (ព្រោះវាអាច Copy បាន)
# ប៉ុន្តែយើងតុបតែងវាឱ្យដូច Text Area ពណ៌ស
if st.session_state.output_code:
    st.code(st.session_state.output_code, language="text")
else:
    # បង្ហាញប្រអប់ទទេពេលមិនទាន់មានកូដ
    st.text_area("output_placeholder", height=150, label_visibility="collapsed", placeholder="The code will appear here...", disabled=True)

# === BOX 3: BLUE COPY BUTTONS (ដូចរូបភាព) ===
st.write("")
col1, col2, col3 = st.columns([1, 1, 3]) # ដាក់ប៊ូតុង ២ នៅខាងឆ្វេង

with col1:
    if st.button("Copy"):
        if st.session_state.output_code:
            st.toast("Please use the copy icon inside the box! ↗️", icon="📋")

with col2:
    if st.button("Copy Code"):
        if st.session_state.output_code:
            st.toast("Please use the copy icon inside the box! ↗️", icon="📋")

st.caption("Please save your secret key for future use.")

# --- Footer ---
st.markdown("""
    <div style="text-align: center; margin-top: 50px; border-top: 1px solid #eee; padding-top: 20px;">
        <p style="color: grey; font-size: 12px;">© 2026 TwoFactor Live Clone. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)