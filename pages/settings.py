import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def render():
    st.markdown("## ⚙️ Sozlamalar")

    tab1, tab2, tab3 = st.tabs(["🤖 AI Sozlamalari", "🔔 Bildirishnomalar", "ℹ️ Tizim haqida"])

    with tab1:
        st.markdown("### HuggingFace AI Sozlamalari")
        
        st.info("""
        **Bepul HuggingFace modellari:**
        
        | Model | Hajm | Til | Tezlik |
        |-------|------|-----|--------|
        | mistralai/Mistral-7B-Instruct-v0.2 | 7B | Ko'p tilli | O'rta |
        | HuggingFaceH4/zephyr-7b-beta | 7B | Ko'p tilli | O'rta |
        | microsoft/Phi-3-mini-4k-instruct | 3.8B | Ko'p tilli | Tez |
        | meta-llama/Meta-Llama-3-8B-Instruct | 8B | Ko'p tilli | O'rta |
        
        ⚡ **Tavsiya:** `Phi-3-mini` - kichik, tez, sifatli
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            hf_token = st.text_input("HuggingFace Token:", type="password",
                                      value=st.session_state.get("hf_token", ""),
                                      placeholder="hf_xxxxxxxxxxxx")
            if hf_token:
                st.session_state["hf_token"] = hf_token
            
            selected_model = st.selectbox("AI Modeli:", [
                "mistralai/Mistral-7B-Instruct-v0.2",
                "HuggingFaceH4/zephyr-7b-beta",
                "microsoft/Phi-3-mini-4k-instruct",
                "meta-llama/Meta-Llama-3-8B-Instruct"
            ])
            st.session_state["ai_model"] = selected_model
        
        with col2:
            st.markdown("**Token olish qadamlari:**")
            st.markdown("""
            1. 🌐 [huggingface.co](https://huggingface.co) oching
            2. 📝 **Sign Up** - Bepul ro'yxatdan o'ting
            3. 👤 Profil → **Settings**
            4. 🔑 **Access Tokens** bo'limi
            5. **New token** → Read → Yaratish
            6. Token nusxalab bu yerga kiriting
            """)
        
        if st.button("🔍 Tokenni tekshirish", type="primary"):
            if hf_token:
                import requests
                headers = {"Authorization": f"Bearer {hf_token}"}
                resp = requests.get("https://huggingface.co/api/whoami", headers=headers)
                if resp.status_code == 200:
                    user_data = resp.json()
                    st.success(f"✅ Token to'g'ri! Foydalanuvchi: {user_data.get('name', 'N/A')}")
                else:
                    st.error(f"❌ Token noto'g'ri yoki muddati o'tgan. Status: {resp.status_code}")
            else:
                st.warning("Token kiriting")

        st.divider()
        
        st.markdown("### Korrupsiya Detektori Sozlamalari")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Qizil flag chegarasi:", 0, 100, 70, 
                           help="Bu balldan yuqori = 🔴 flag")
        with col2:
            st.number_input("Sariq flag chegarasi:", 0, 100, 40,
                           help="Bu balldan yuqori = 🟡 flag")
        with col3:
            st.number_input("Minimal mezon balli (%):", 0, 100, 50,
                           help="Shu % dan past + ko'p tasdiq = xavf")

    with tab2:
        st.markdown("### Bildirishnoma Sozlamalari")
        st.checkbox("📧 Email bildirishnoma", value=True)
        st.checkbox("📱 Telegram bot orqali", value=False)
        st.text_input("Email manzil:", placeholder="admin@econstruction.uz")
        st.text_input("Telegram Bot Token:", placeholder="7xxxxxxxxx:AAF...")
        st.text_input("Telegram Chat ID:", placeholder="-100xxxxxxxxxx")

    with tab3:
        st.markdown("### ℹ️ Tizim Arxitekturasi")
        st.markdown("""
        ```
        E-CONSTRUCTION ANTI-KORRUPSIYA TIZIMI
        ├── 🖥️  Frontend: Streamlit (Python)
        ├── 🤖  AI Layer:
        │   ├── HuggingFace Inference API (Bepul)
        │   │   └── Mistral-7B / Phi-3 / Zephyr
        │   └── Rule-based Engine (Mahalliy)
        │       └── 20 mezon, pattern matching
        ├── 💾  Ma'lumotlar bazasi:
        │   ├── Demo: JSON fayl
        │   └── Ishlab chiqarish: PostgreSQL / Supabase
        ├── 📊  Vizualizatsiya: Plotly
        └── 🔗  Integratsiya:
            ├── my.gov.uz API
            └── YIDXP tizimi
        ```
        
        **Versiya:** 1.0.0  
        **Mualliflar:** E-Construction Jamoasi  
        **Litsenziya:** O'zbekiston Respublikasi  
        """)
        
        st.markdown("### 📦 Kutubxonalar")
        st.code("""
streamlit>=1.28.0
plotly>=5.18.0
requests>=2.31.0
python-dotenv>=1.0.0
        """)
