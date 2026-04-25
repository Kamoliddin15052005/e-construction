import streamlit as st


def render():
    st.markdown("## 🏠 Tizim haqida")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div style="background:#e3f2fd;border-radius:10px;padding:1.2rem;text-align:center;border-left:4px solid #1565c0">
            <h2 style="color:#1565c0;margin:0">1,247</h2>
            <p style="margin:0;color:#555">Jami arizalar</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#ffebee;border-radius:10px;padding:1.2rem;text-align:center;border-left:4px solid #f44336">
            <h2 style="color:#f44336;margin:0">89</h2>
            <p style="margin:0;color:#555">🔴 Xavfli arizalar</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:#e8f5e9;border-radius:10px;padding:1.2rem;text-align:center;border-left:4px solid #4caf50">
            <h2 style="color:#4caf50;margin:0">1,091</h2>
            <p style="margin:0;color:#555">🟢 Toza arizalar</p>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div style="background:#fff8e1;border-radius:10px;padding:1.2rem;text-align:center;border-left:4px solid #ff9800">
            <h2 style="color:#ff9800;margin:0">67</h2>
            <p style="margin:0;color:#555">🟡 Tekshiruvda</p>
        </div>""", unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### 📋 Tizim qanday ishlaydi?")
        
        steps = [
            ("1️⃣", "Ariza kiritish", "Tadbirkor my.gov.uz orqali ruxsatnoma so'raydi. Tizim arizani avtomatik qabul qiladi.", "#e3f2fd"),
            ("2️⃣", "AI Tahlil (20 mezon)", "Loyiha 4 bo'lim bo'yicha 20 ta mezon asosida baholanadi. Har bir mezon uchun ball beriladi.", "#f3e5f5"),
            ("3️⃣", "Vakolatli organlar", "4 ta vakolatli organ (sanitariya, yong'in, ekologiya, qurilish) ruxsatnoma beradi yoki rad etadi.", "#e8f5e9"),
            ("4️⃣", "Korrupsiya Detektori", "AI 3 komponentni taqqoslaydi: mezon balli, rad etish sabablari, foydalanuvchi fikri.", "#fff8e1"),
            ("5️⃣", "Signal va Hisobot", "Anomaliya aniqlansa, ariza qizil rangga o'tadi va hisobot yaratiladi.", "#ffebee"),
        ]
        
        for icon, title, desc, color in steps:
            st.markdown(f"""
            <div style="background:{color};border-radius:8px;padding:0.8rem 1rem;margin-bottom:0.5rem;display:flex;align-items:flex-start;gap:0.8rem">
                <span style="font-size:1.5rem">{icon}</span>
                <div>
                    <strong>{title}</strong><br>
                    <span style="color:#555;font-size:0.9rem">{desc}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 🔍 Tizim nimani aniqlaydi?")
        
        signals = [
            ("🚨", "Past ball + Ko'p tasdiqlash", "Loyiha balli 50% dan past, lekin barcha organlar tasdiqlagan"),
            ("🔄", "Rad etish ~ O'zgartirishlar", "Qaytarish sabablari o'zgartirishlarga mos kelmaydi"),
            ("⭐", "Rəsmi OK + Past baho", "Rasmiy tasdiqlangan, lekin foydalanuvchilar 2/5 baho bergan"),
            ("📊", "Tez tasdiqlash", "Oddiy loyiha uchun g'ayritabiiy tez tasdiqlash"),
            ("🔁", "Ko'p qaytarish", "Bir loyiha bir necha marta qaytarilganligi"),
        ]
        
        for icon, title, desc in signals:
            st.markdown(f"""
            <div style="border:1px solid #ddd;border-radius:8px;padding:0.8rem;margin-bottom:0.5rem">
                <strong>{icon} {title}</strong><br>
                <span style="color:#666;font-size:0.85rem">{desc}</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    
    st.markdown("### 🤖 AI Texnologiyasi")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **HuggingFace (Bepul)**
        
        🤗 Mistral-7B-Instruct
        - Matn tahlili
        - Rad etish sabablari
        - Ko'p tilli qo'llab-quvvatlash
        """)
    with col2:
        st.success("""
        **Mahalliy Tahlil**
        
        ⚡ Rule-based Engine
        - 20 mezon baholash
        - Kalit so'z tahlili
        - Real vaqt natija
        """)
    with col3:
        st.warning("""
        **Gibrid Yondashuv**
        
        🔀 AI + Qoidalar
        - Pattern recognition
        - Anomaliya aniqlash
        - Uch tomonlama taqqoslash
        """)
