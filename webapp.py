import streamlit as st
import pyotp
import pytz
from datetime import datetime

# --- 1. ការកំណត់ទំព័រ ---
st.set_page_config(page_title="TwoFactor Pro", page_icon="🔐", layout="centered")

# --- 2. CSS (តុបតែងឱ្យស្អាតដូច 2FA.Live) ---
st.markdown("""
    <style>
    /* ផ្ទៃខាងក្រោយ */
    .stApp { background-color: #FFF0F5; }
    
    /* តុបតែងប្រអប់ Text Area ទាំងពីរឱ្យពណ៌ស និងមានគែម */
    .stTextArea textarea {
        background-color: white !important;
        border: 1px solid #ccc !important;
        border-radius: 5px;
        color: black !important;
        font-size: 16px;
    }

    /* ប៊ូតុង Submit ពណ៌ខៀវ/ផ្កាឈូក */
    div.stButton > button {
        background-color: #007bff !important; /* ដាក់ពណ៌ខៀវដូច 2fa.live */
        color: white !important;
        font-weight: bold;
        border: none;
        width: 150px;
        height: 40px;
        border-radius: 5px;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: #0056b3 !important;
    }
    
    /* លាក់ Element មិនចាំបាច់ */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. Header & Clock ---
tz = pytz.timezone('Asia/Phnom_Penh')
current_time = datetime.now(tz).strftime("%b %d %I:%M:%S %p")

st.markdown(f"""
    <div style="background-color: #E91E63; padding: 15px; border-radius: 10px 10px 0 0; 
                display: flex; justify-content: space-between; align-items: center; color: white; margin-bottom: 20px;">
        <div style="font-size: 22px; font-weight: bold; color: yellow;">TwoFactor <span style="color:white;">Live</span></div>
        <div style="font-size: 14px;">{current_time}</div>
    </div>
""", unsafe_allow_html=True)

# --- 4. Logic សម្រាប់រក្សាទុកតម្លៃ (Session State) ---
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = ""

# === ប្រអប់ទី ១: 2FA Secret (Input) ===
st.markdown("##### * 2FA Secret (ដាក់ Secret Key នៅទីនេះ)")
secret_input = st.text_area("input_box", height=150, label_visibility="collapsed", placeholder="Example: BK5V TVQ7 D2RB...")

# === ប៊ូតុង Submit (នៅកណ្តាល) ===
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
                    # បង្ហាញតែលេខកូដសុទ្ធ (ដូច 2fa.live)
                    results.append(code) 
                except:
                    results.append("Invalid Key")
        
        # បញ្ចូលលទ្ធផលទៅក្នុង Session State ដើម្បីបង្ហាញនៅប្រអប់ទី ២
        st.session_state.generated_code = "\n".join(results)
    else:
        st.warning("សូមបញ្ចូល Secret Key ជាមុនសិន!")

# === ប្រអប់ទី ២: 2FA Code (Output) ===
st.markdown("##### * 2FA Code (លទ្ធផលកូដ)")
# ប្រអប់នេះបង្ហាញតម្លៃចេញពី Session State
st.text_area("output_box", value=st.session_state.generated_code, height=150, label_visibility="collapsed", placeholder="The code will appear here...")

# === ប៊ូតុង Copy ===
# ដោយសារ Text Area មិនមានប៊ូតុង Copy ស្វ័យប្រវត្តិ ខ្ញុំដាក់ st.code បន្ថែមនៅខាងក្រោម
# ដើម្បីឱ្យអ្នកងាយស្រួលចុច Copy តែម្តង
if st.session_state.generated_code:
    st.write("---")
    st.caption("ចុចប៊ូតុងខាងក្រោមដើម្បី Copy លឿនៗ:")
    st.code(st.session_state.generated_code, language="text")

# --- Footer ---
st.markdown("""
    <div style="text-align: center; margin-top: 30px; color: grey; font-size: 12px;">
        created by EM PUNLOK @ 2026<br>
        <a href="https://t.me/empunlok787">Telegram</a> | <a href="https://www.facebook.com/empunlok99">Facebook</a>
    </div>
""", unsafe_allow_html=True)