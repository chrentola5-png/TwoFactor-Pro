import streamlit as st
import pyotp
import random
import string
from datetime import datetime
import pytz

# --- 1. ការកំណត់ទំព័រ ---
st.set_page_config(page_title="TwoFactor Pro", page_icon="🔐", layout="centered")

# --- 2. CSS (តុបតែងឱ្យដូចកម្មវិធី Desktop ១០០%) ---
st.markdown("""
    <style>
    /* ផ្ទៃខាងក្រោយពណ៌ផ្កាឈូកស្រាល */
    .stApp { background-color: #FFF0F5; }
    
    /* កែពណ៌ Tabs ឱ្យទៅជាពណ៌ប្រផេះ/ផ្កាឈូក */
    button[data-baseweb="tab"] {
        background-color: transparent;
        color: #000;
        font-weight: bold;
        font-size: 14px;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #E91E63;
        color: white;
        border-radius: 5px 5px 0 0;
    }

    /* ប្រអប់កណ្តាលពណ៌ប្រផេះ (Gray Card Container) */
    .block-container {
        background-color: #E0E0E0;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        max-width: 700px;
    }

    /* ប៊ូតុងពណ៌ផ្កាឈូក (ដូច Desktop) */
    div.stButton > button {
        background-color: #E91E63 !important;
        color: white !important;
        font-weight: bold;
        border: none;
        width: 100%;
        height: 45px;
        border-radius: 5px;
        font-size: 16px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #C2185B !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* ប្រអប់ Input ពណ៌ស */
    .stTextArea textarea, .stTextInput input {
        background-color: white !important;
        color: black !important;
        border-radius: 5px;
    }
    
    /* ផ្លាស់ប្តូរពណ៌ចំណងជើង */
    h3 { color: #E91E63 !important; font-size: 18px; margin-bottom: 5px; }

    /* លាក់ Element មិនចាំបាច់របស់ Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. Header & Clock (ក្បាលខាងលើ) ---
tz = pytz.timezone('Asia/Phnom_Penh')
current_time = datetime.now(tz).strftime("%b %d %I:%M:%S %p")

st.markdown(f"""
    <div style="background-color: #E91E63; padding: 15px; border-radius: 10px 10px 0 0; 
                display: flex; justify-content: space-between; align-items: center; color: white; 
                margin-bottom: -20px; position: relative; z-index: 100;">
        <div style="font-size: 22px; font-weight: bold; color: yellow;">TwoFactor <span style="color:yellow;">Pro</span></div>
        <div style="font-size: 14px;">{current_time}</div>
    </div>
    <br>
""", unsafe_allow_html=True)

# --- 4. ផ្នែក Tabs (មុខងារសំខាន់) ---
tab1, tab2, tab3 = st.tabs(["🔐 2FA", "🔑 Password", "📝 Names"])

# === TAB 1: 2FA Generator ===
with tab1:
    st.markdown("### Secret Keys")
    secret_input = st.text_area("2fa_input", height=120, label_visibility="collapsed", placeholder="Paste secret keys here...")
    
    if st.button("GENERATE CODES"):
        if secret_input.strip():
            keys = secret_input.strip().split('\n')
            result_text = ""
            for key in keys:
                key = key.strip()
                if key:
                    try:
                        totp = pyotp.TOTP(key.replace(" ", ""))
                        result_text += f"{totp.now()}\n"
                    except:
                        result_text += "Invalid Key\n"
            
            st.markdown("### Codes")
            # st.code មានប៊ូតុង Copy នៅជ្រុងខាងស្តាំស្រាប់ (ល្អបំផុតសម្រាប់ Web)
            st.code(result_text, language="text")
        else:
            st.warning("សូមបញ្ចូល Secret Key ជាមុនសិន!")

# === TAB 2: Password Generator ===
with tab2:
    st.markdown("### Password Options")
    col1, col2 = st.columns(2)
    with col1:
        length = st.slider("Length (ប្រវែង)", 8, 32, 12)
    with col2:
        use_symbols = st.checkbox("Symbols (!@#)", value=True)
        use_digits = st.checkbox("Numbers (123)", value=True)
    
    if st.button("GENERATE PASSWORD"):
        chars = string.ascii_letters
        if use_digits: chars += string.digits
        if use_symbols: chars += "!@#$%^&*()"
        
        password = "".join(random.choice(chars) for _ in range(length))
        st.markdown("### Your Password")
        st.code(password, language="text")

# === TAB 3: Random Names ===
with tab3:
    st.markdown("### Generate Name")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("ភេទ", ["Male", "Female", "Any"])
    with col2:
        count = st.number_input("ចំនួនឈ្មោះ", 1, 50, 5)
        
    if st.button("GENERATE NAMES"):
        # ទិន្នន័យឈ្មោះគំរូ
        first_names = ["Sok", "Dara", "Vibol", "Nary", "Bopha", "Mony", "Visal", "Chea", "Pov", "Roth"]
        last_names = ["Sao", "Chan", "Keo", "Ly", "Sim", "Heng", "Lim", "Kong", "Meas", "Seng"]
        
        results = ""
        for _ in range(count):
            name = f"{random.choice(last_names)} {random.choice(first_names)}"
            results += name + "\n"
            
        st.markdown("### Result Names")
        st.code(results, language="text")

# --- 5. Footer (ប៊ូតុងខាងក្រោម) ---
st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <div style="color: grey; font-size: 12px; margin-bottom: 10px;">created by EM PUNLOK @ 2026</div>
        <a href="https://t.me/empunlok787" target="_blank" style="background-color: #0088cc; color: white; padding: 8px 20px; text-decoration: none; border-radius: 5px; margin: 5px; font-weight: bold;">Telegram</a>
        <a href="https://www.facebook.com/empunlok99" target="_blank" style="background-color: #1877F2; color: white; padding: 8px 20px; text-decoration: none; border-radius: 5px; margin: 5px; font-weight: bold;">Facebook</a>
    </div>
""", unsafe_allow_html=True)