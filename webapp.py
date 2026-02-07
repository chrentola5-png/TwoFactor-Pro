import streamlit as st
import pyotp
import random
import string
from datetime import datetime
import pytz

# --- 1. ការកំណត់ទំព័រ ---
st.set_page_config(page_title="TwoFactor Pro", page_icon="🔐", layout="centered")

# --- 2. CSS តុបតែងឱ្យដូច Desktop 100% ---
st.markdown("""
    <style>
    /* ផ្ទៃខាងក្រោយពណ៌ផ្កាឈូកស្រាល */
    .stApp {
        background-color: #FFF0F5;
    }
    
    /* កែពណ៌ Tabs */
    button[data-baseweb="tab"] {
        background-color: transparent;
        color: #000;
        font-weight: bold;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #E91E63;
        color: white;
        border-radius: 5px 5px 0 0;
    }

    /* ប្រអប់កណ្តាលពណ៌ប្រផេះ (Gray Card) */
    .block-container {
        background-color: #E0E0E0;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        max-width: 700px;
        margin-top: 20px;
    }

    /* ប៊ូតុងពណ៌ផ្កាឈូក */
    div.stButton > button {
        background-color: #E91E63 !important;
        color: white !important;
        font-weight: bold;
        border: none;
        width: 100%;
        height: 45px;
        border-radius: 5px;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: #C2185B !important;
    }

    /* Input Fields Background White */
    .stTextArea textarea, .stTextInput input {
        background-color: white !important;
        color: black !important;
    }

    /* សម្រាប់ Title និង Header */
    h1, h2, h3 {
        color: #E91E63 !important;
        padding: 0;
        margin: 0;
    }
    
    /* លាក់ Element ដែលមិនចាំបាច់ */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. Header & Time (ពណ៌ផ្កាឈូកខាងលើ) ---
tz = pytz.timezone('Asia/Phnom_Penh')
current_time = datetime.now(tz).strftime("%b %d %I:%M:%S %p")

# បង្កើត Header ដោយប្រើ HTML ផ្ទាល់
st.markdown(f"""
    <div style="background-color: #E91E63; padding: 15px; border-radius: 10px 10px 0 0; display: flex; justify-content: space-between; align-items: center; color: white; margin-bottom: -30px; position: relative; z-index: 100;">
        <div style="font-size: 24px; font-weight: bold; color: yellow;">TwoFactor <span style="color:yellow;">Pro</span></div>
        <div style="font-size: 14px;">{current_time}</div>
    </div>
    <br>
""", unsafe_allow_html=True)

# --- 4. Tabs ---
tab1, tab2, tab3 = st.tabs(["🔐 2FA", "🔑 Password", "📝 Names"])

# === TAB 1: 2FA ===
with tab1:
    st.write("### Secret Keys")
    secret_input = st.text_area("Paste keys...", height=100, label_visibility="collapsed", placeholder="Paste secret keys here...")
    
    if st.button("GENERATE CODES"):
        if secret_input.strip():
            keys = secret_input.strip().split('\n')
            result_text = ""
            valid_count = 0
            
            for key in keys:
                key = key.strip()
                if key:
                    try:
                        totp = pyotp.TOTP(key.replace(" ", ""))
                        code = totp.now()
                        result_text += f"{code}\n"
                        valid_count += 1
                    except:
                        result_text += "Invalid Key\n"
            
            st.write("### Codes")
            # st.code មានប៊ូតុង Copy នៅខាងស្តាំស្រាប់ (ល្អជាងប៊ូតុង Copy ធម្មតា)
            st.code(result_text, language="text")
            
            if valid_count > 0:
                st.toast(f"✅ បង្កើតបាន {valid_count} កូដ!", icon="🎉")
        else:
            st.error("សូមបញ្ចូល Secret Key ជាមុនសិន!")

# === TAB 2: Password Generator ===
with tab2:
    st.write("### Password Generator")
    length = st.slider("ប្រវែងលេខសម្ងាត់", 8, 32, 12)
    use_symbols = st.checkbox("ប្រើនិមិត្តសញ្ញា (@#$%)", value=True)
    
    if st.button("GENERATE PASSWORD"):
        chars = string.ascii_letters + string.digits
        if use_symbols:
            chars += "!@#$%^&*()"
        password = "".join(random.choice(chars) for _ in range(length))
        
        st.write("### Your Password")
        st.code(password, language="text")

# === TAB 3: Names (Example) ===
with tab3:
    st.write("### Random Name")
    if st.button("GENERATE NAME"):
        first_names = ["Sok", "Dara", "Vibol", "Nary", "Bopha", "Mony"]
        last_names = ["Sao", "Chan", "Keo", "Ly", "Sim", "Chea"]
        full_name = f"{random.choice(last_names)} {random.choice(first_names)}"
        
        st.write("### Result")
        st.code(full_name, language="text")

# --- Footer ---
st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <span style="color: grey; font-size: 12px;">created by EM PUNLOK @ 2026</span><br><br>
        <a href="https://t.me/empunlok787" target="_blank" style="background-color: #0088cc; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; margin-right: 5px;">Telegram</a>
        <a href="https://www.facebook.com/empunlok99" target="_blank" style="background-color: #1877F2; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px;">Facebook</a>
    </div>
""", unsafe_allow_html=True)