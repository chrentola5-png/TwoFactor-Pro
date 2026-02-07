import streamlit as st
import pyotp
import pytz
from datetime import datetime

# --- 1. Page Configuration ---
st.set_page_config(page_title="2Fa.Live", page_icon="🔐", layout="centered")

# --- 2. CSS Styling (រចនាឱ្យដូច 2Fa.Live ១០០%) ---
st.markdown("""
    <style>
    /* ផ្ទៃខាងក្រោយពណ៌ស */
    .stApp { background-color: #ffffff; }
    
    /* Input & Output Text Areas (ពណ៌ស គែមប្រផេះ) */
    .stTextArea textarea {
        background-color: white !important;
        border: 1px solid #ced4da !important;
        border-radius: 4px;
        color: #495057 !important;
        font-family: monospace;
        font-size: 16px;
    }

    /* ប៊ូតុងពណ៌ខៀវ (Bootstrap Blue ដូចរូបភាព) */
    div.stButton > button {
        background-color: #0d6efd !important;
        color: white !important;
        font-weight: 500;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-size: 1rem;
        width: auto; /* មិនឱ្យពេញអេក្រង់ពេក */
        min-width: 100px;
    }
    div.stButton > button:hover {
        background-color: #0b5ed7 !important;
    }

    /* កែ st.code ឱ្យមើលទៅដូចប្រអប់ Copy */
    .stCode {
        margin-top: -10px;
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
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='color: #333; font-size: 32px; display: inline-block;'>2Fa.Live</h1>
        <span style='font-size: 14px; color: grey; font-weight: normal; margin-left: 10px;'>Two Factor Authenticator</span>
    </div>
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

secret_input = st.text_area("input_label", height=120, label_visibility="collapsed", placeholder="BK5V TVQ7 D2RB...")

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
                    results.append(code)
                except:
                    results.append("Invalid Key")
        st.session_state.output_code = "\n".join(results)

# === BOX 2: OUTPUT & COPY BUTTONS ===
st.write("")
st.markdown("""
    <div class="label-style">
        <span class="bold-text">* 2FA Code</span> 2-step verification code
    </div>
""", unsafe_allow_html=True)

# ប្រអប់លទ្ធផល (Output Box)
st.text_area("output_display", value=st.session_state.output_code, height=120, label_visibility="collapsed", placeholder="The code will appear here...", disabled=True)

# === COPY SECTION (នៅខាងក្រោមដូចរូប) ===
if st.session_state.output_code:
    st.write("")
    # ប្រើ Columns ដើម្បីដាក់ប៊ូតុង Copy នៅខាងឆ្វេង (ដូចរូប)
    col1, col2 = st.columns([1, 4])
    with col1:
        # st.code គឺជា "ប៊ូតុង Copy" ដ៏ល្អបំផុតនៅក្នុង Streamlit
        # វាមាន Icon Copy នៅជ្រុងខាងស្តាំស្រាប់
        st.caption("Copy here:")
        st.code(st.session_state.output_code, language="text")
    
    with col2:
        # បន្ថែមប៊ូតុង Clear នៅក្បែរនោះ
        st.write("") # Spacer ឱ្យស្មើគ្នា
        st.write("")
        if st.button("Clear / Reset"):
            st.session_state.output_code = ""
            st.rerun()

# --- Footer ---
st.markdown("""
    <div style="text-align: center; margin-top: 50px; border-top: 1px solid #eee; padding-top: 20px;">
        <p style="color: grey; font-size: 12px;">© 2026 TwoFactor Live Clone.</p>
    </div>
""", unsafe_allow_html=True)