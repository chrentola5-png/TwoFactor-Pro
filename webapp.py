import streamlit as st
import pyotp
import pandas as pd
import time

# --- ការកំណត់ UI ---
st.set_page_config(page_title="TwoFactor Pro Online", page_icon="🔐")

st.title("🔐 TwoFactor Pro Online")
st.write("Created by EM PUNLOK @ 2026")

# --- ផ្នែកបញ្ចូលទិន្នន័យ ---
secret_input = st.text_area("បញ្ចូល Secret Keys (មួយក្នុងមួយជួរ):", height=150)

# --- ប៊ូតុងដំណើរការ ---
if st.button("GENERATE CODES", type="primary"):
    if secret_input.strip():
        keys = secret_input.split('\n')
        results = []
        
        # របារដំណើរការ (Progress Bar)
        progress_text = "កំពុងបង្កើតកូដ..."
        my_bar = st.progress(0, text=progress_text)
        
        for i, key in enumerate(keys):
            key = key.strip()
            if key:
                try:
                    # បង្កើតកូដ 2FA
                    totp = pyotp.TOTP(key.replace(" ", ""))
                    current_code = totp.now()
                    results.append({"Secret Key": key, "2FA Code": current_code})
                except Exception:
                    results.append({"Secret Key": key, "2FA Code": "Invalid Key!"})
            
            # Update Progress Bar
            time.sleep(0.1) # ដាក់ឱ្យយឺតបន្តិចដើម្បីមើលឃើញ
            my_bar.progress((i + 1) / len(keys), text=progress_text)
            
        time.sleep(0.5)
        my_bar.empty() # លុបរបារចោលពេលចប់
        
        # បង្ហាញលទ្ធផល
        if results:
            df = pd.DataFrame(results)
            st.table(df)
            st.success(f"✅ បានបង្កើតកូដចំនួន {len(results)} ជោគជ័យ!")
        else:
            st.error("❌ មិនមាន Key ត្រឹមត្រូវទេ")
    else:
        st.warning("⚠️ សូមបញ្ចូល Secret Key ជាមុនសិន!")

# --- Footer ---
st.divider()
st.markdown("""
    <style>
    .footer {
        font-size: 12px;
        color: grey;
        text-align: center;
    }
    </style>
    <div class="footer">
        © 2026 EM PUNLOK. All Rights Reserved.<br>
        This tool runs securely on Streamlit Cloud.
    </div>
    """, unsafe_allow_html=True)