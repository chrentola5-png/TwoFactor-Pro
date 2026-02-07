import streamlit as st
import pyotp
import time

# --- 1. ការកំណត់ទំព័រ និង Style (CSS) ---
st.set_page_config(page_title="TwoFactor Pro", page_icon="🔐", layout="centered")

# CSS ដើម្បីតុបតែងឱ្យដូចកម្មវិធី Desktop របស់អ្នក
st.markdown("""
    <style>
    /* ប្តូរពណ៌ប៊ូតុងឱ្យទៅជាពណ៌ផ្កាឈូក */
    div.stButton > button:first-child {
        background-color: #E91E63;
        color: white;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #C2185B;
        color: white;
    }
    
    /* ធ្វើ Header ពណ៌ផ្កាឈូក */
    .header-style {
        background-color: #E91E63;
        padding: 15px;
        border-radius: 10px 10px 0 0;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    /* ធ្វើ Footer */
    .footer-link {
        text-decoration: none;
        background-color: #03A9F4;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        margin: 0 5px;
        font-size: 14px;
    }
    .footer-fb { background-color: #1877F2; }
    .footer-tg { background-color: #0088cc; }
    </style>
""", unsafe_allow_html=True)

# --- 2. បង្ហាញ Header ---
st.markdown('<div class="header-style">TwoFactor Pro</div>', unsafe_allow_html=True)

# --- 3. បង្កើត Tabs (2FA, Password, Names) ---
tab1, tab2, tab3 = st.tabs(["🔐 2FA", "🔑 Password", "📝 Names"])

# === ផ្នែកទី 1: 2FA ===
with tab1:
    st.write("### Secret Keys")
    secret_input = st.text_area("Paste keys...", height=150, label_visibility="collapsed", placeholder="Paste your secret keys here...")
    
    # ប៊ូតុង Generate
    if st.button("GENERATE CODES"):
        if secret_input.strip():
            keys = secret_input.strip().split('\n')
            output_text = ""
            
            for key in keys:
                key = key.strip()
                if key:
                    try:
                        totp = pyotp.TOTP(key.replace(" ", ""))
                        code = totp.now()
                        output_text += f"{code}\n"
                    except:
                        output_text += "Invalid Key\n"
            
            st.write("### Codes")
            # បង្ហាញកូដក្នុងប្រអប់ដែលអាច Copy បានងាយ
            st.code(output_text, language="text")
            st.success("បង្កើតកូដជោគជ័យ!")
        else:
            st.warning("សូមបញ្ចូល Secret Key សិន!")

# === ផ្នែកទី 2: Password (បន្ថែមជាគំរូ) ===
with tab2:
    st.info("មុខងារបង្កើត Password នឹងដាក់ឱ្យប្រើឆាប់ៗនេះ...")

# === ផ្នែកទី 3: Names (បន្ថែមជាគំរូ) ===
with tab3:
    st.info("មុខងារបង្កើតឈ្មោះនឹងដាក់ឱ្យប្រើឆាប់ៗនេះ...")

# --- 4. Footer (Telegram & Facebook) ---
st.divider()
st.markdown("""
    <div style="text-align: center; color: grey; font-size: 12px;">
        created by EM PUNLOK @ 2026 <br><br>
        <a href="https://t.me/empunlok787" target="_blank" class="footer-link footer-tg">Telegram</a>
        <a href="https://www.facebook.com/empunlok99" target="_blank" class="footer-link footer-fb">Facebook</a>
    </div>
""", unsafe_allow_html=True)