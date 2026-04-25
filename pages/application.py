import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.criteria_engine import CRITERIA, get_max_total_score, get_dept_max_score
from utils.data_store import save_application, load_applications
from utils.ai_analyzer import calculate_corruption_score, analyze_rejection_reasons


def render():
    st.markdown("## 📝 Yangi Ariza Kiritish")
    st.info("my.gov.uz dan keladigan ariza ma'lumotlarini kiriting yoki demo yuklang")

    # Demo yuklash
    col_demo, _ = st.columns([2, 5])
    with col_demo:
        if st.button("🔄 Demo Ariza Yuklash", type="secondary"):
            st.session_state["demo_loaded"] = True

    st.divider()

    # Demo ma'lumotlar
    demo = {}
    if st.session_state.get("demo_loaded"):
        demo = {
            "tadbirkor": "Karimov Sherzod Alisher o'g'li",
            "loyiha_nomi": "12 qavatli turar-joy kompleksi 'Yangi Hayot'",
            "inn": "314568921",
            "ariza_id": "RUX-2025-08745",
            "manzil": "Toshkent sh., Mirzo Ulug'bek tumani, Qorasaroy ko'chasi 45",
            "tur": "Ko'p qavatli turar-joy",
            "maydon": 3200,
            "qavatlar": 12,
            "tavsif": "12 qavatli turar-joy kompleksi. Yer maydoni 0.5 gektar. Binoda 96 ta kvartira rejalashtirilgan. Qurilish materiali - temir-beton.",
            "rad_sabab": "Loyiha seysmoturgunlik bo'yicha talablariga javob bermaydi. Sanitariya me'yorlari buzilgan. Hujjat yetishmaydi - yong'in xavfsizligi loyihasi.",
            "ozgartirishlar": "Ba'zi hujjatlar to'ldirildi."
        }
        st.success("✅ Demo ariza yuklandi!")

    # FORM
    with st.form("application_form"):
        st.markdown("### 👤 Tadbirkor ma'lumotlari")
        col1, col2, col3 = st.columns(3)
        with col1:
            tadbirkor = st.text_input("F.I.O", value=demo.get("tadbirkor", ""), placeholder="To'liq ism...")
        with col2:
            inn = st.text_input("STIR / INN", value=demo.get("inn", ""), placeholder="123456789")
        with col3:
            ariza_id = st.text_input("Ariza raqami (my.gov.uz)", value=demo.get("ariza_id", ""), placeholder="RUX-2025-XXXXX")

        st.markdown("### 🏗️ Loyiha ma'lumotlari")
        col1, col2 = st.columns(2)
        with col1:
            loyiha_nomi = st.text_input("Loyiha nomi", value=demo.get("loyiha_nomi", ""), placeholder="Loyiha nomi...")
            manzil = st.text_input("Qurilish manzili", value=demo.get("manzil", ""), placeholder="Shahar, tuman, ko'cha...")
        with col2:
            tur = st.selectbox("Qurilish turi", [
                "Ko'p qavatli turar-joy",
                "Yakka tartibdagi uy",
                "Tijorat bino",
                "Sanoat binosi",
                "Ijtimoiy obyekt",
                "Boshqa"
            ], index=0 if not demo.get("tur") else [
                "Ko'p qavatli turar-joy","Yakka tartibdagi uy","Tijorat bino",
                "Sanoat binosi","Ijtimoiy obyekt","Boshqa"
            ].index(demo.get("tur", "Ko'p qavatli turar-joy")))
            
            col2a, col2b = st.columns(2)
            with col2a:
                maydon = st.number_input("Maydon (m²)", min_value=10, max_value=100000, value=demo.get("maydon", 500))
            with col2b:
                qavatlar = st.number_input("Qavatlar soni", min_value=1, max_value=100, value=demo.get("qavatlar", 5))

        tavsif = st.text_area("Loyiha tavsifi", value=demo.get("tavsif", ""), height=100,
                              placeholder="Loyiha haqida qisqa tavsif...")

        st.divider()
        
        # Vakolatli organlar tasdiqlashlari
        st.markdown("### ✅ Vakolatli Organlar Tasdiqlashlari")
        st.caption("Qaysi organlar ruxsatnoma berdi?")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            san_approved = st.checkbox("🧪 Sanitariya-Epidemiologiya", value=False)
        with col2:
            yon_approved = st.checkbox("🔥 Yong'in Xavfsizligi", value=False)
        with col3:
            eko_approved = st.checkbox("🌿 Ekologiya", value=False)
        with col4:
            qur_approved = st.checkbox("🏗️ Qurilish Bo'limi", value=False)

        st.divider()

        # Rad etish va o'zgartirishlar
        st.markdown("### 🔄 Qaytarish Tarixchasi (agar bo'lsa)")
        col1, col2 = st.columns(2)
        with col1:
            rad_sabab = st.text_area(
                "Rad etish sabablari",
                value=demo.get("rad_sabab", ""),
                height=120,
                placeholder="Vakolatli organ nima sababda qaytardi?"
            )
        with col2:
            ozgartirishlar = st.text_area(
                "Amalga oshirilgan o'zgartirishlar",
                value=demo.get("ozgartirishlar", ""),
                height=120,
                placeholder="Tadbirkor nima o'zgartirdi?"
            )

        st.divider()

        # 20 Mezon baholash
        st.markdown("### 📊 20 Mezon Bo'yicha Baholash")
        st.info("Har bir mezon uchun loyiha holatini tanlang. AI avtomatik ball hisoblaydi.")
        
        all_scores = {}
        
        for dept_key, dept_data in CRITERIA.items():
            with st.expander(f"{dept_data['nomi']} - {get_dept_max_score(dept_key)} ball", expanded=False):
                for mezon in dept_data["mezonlar"]:
                    st.markdown(f"**{mezon['nomi']}** *(max: {mezon['max_ball']} ball)*")
                    st.caption(mezon["tavsif"])
                    
                    selected = st.radio(
                        mezon["savol"],
                        options=list(mezon["variantlar"].keys()),
                        key=f"mezon_{mezon['id']}",
                        horizontal=False
                    )
                    all_scores[mezon["id"]] = mezon["variantlar"][selected]
                    st.divider()

        submitted = st.form_submit_button("💾 Ariza Saqlash va Tahlil Qilish", type="primary", use_container_width=True)

    if submitted:
        if not tadbirkor or not loyiha_nomi:
            st.error("❌ Tadbirkor va loyiha nomi majburiy!")
            return

        dept_approvals = {
            "sanitariya": san_approved,
            "yonghin": yon_approved,
            "ekologiya": eko_approved,
            "qurilish": qur_approved
        }

        # Rad etish tahlili
        rej_analysis = analyze_rejection_reasons(rad_sabab, ozgartirishlar)

        # Korrupsiya hisoblash
        corruption_result = calculate_corruption_score(
            criteria_scores=all_scores,
            dept_approvals=dept_approvals,
            rejection_analysis=rej_analysis,
            user_rating=None
        )

        # Ariza saqlash
        app_data = {
            "tadbirkor": tadbirkor,
            "inn": inn,
            "ariza_id": ariza_id,
            "loyiha_nomi": loyiha_nomi,
            "manzil": manzil,
            "tur": tur,
            "maydon": maydon,
            "qavatlar": qavatlar,
            "tavsif": tavsif,
            "dept_approvals": dept_approvals,
            "criteria_scores": all_scores,
            "rad_sabab": rad_sabab,
            "ozgartirishlar": ozgartirishlar,
            "risk_score": corruption_result["total_risk_score"],
            "flag": corruption_result["flag_color"],
            "holat": "tekshiruvda" if not any(dept_approvals.values()) else
                     ("tasdiqlangan" if all(dept_approvals.values()) else "qaytarilgan"),
            "corruption_result": corruption_result
        }

        success = save_application(app_data)

        if success:
            st.success(f"✅ Ariza muvaffaqiyatli saqlandi! ID: {app_data.get('id', 'N/A')}")
            
            # Natija ko'rsatish
            flag = corruption_result["flag_color"]
            verdict = corruption_result["verdict"]
            risk_score = corruption_result["total_risk_score"]
            
            if flag == "red":
                st.markdown(f"""
                <div class="red-flag">
                    <h3>🚨 {verdict}</h3>
                    <h2 style="color:#f44336">Xavf darajasi: {risk_score}/100</h2>
                    <p>{corruption_result['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)
            elif flag == "orange":
                st.warning(f"⚠️ {verdict} | Xavf: {risk_score}/100 | {corruption_result['recommendation']}")
            elif flag == "yellow":
                st.warning(f"🟡 {verdict} | Xavf: {risk_score}/100")
            else:
                st.success(f"✅ {verdict} | Xavf: {risk_score}/100")

            if corruption_result["indicators"]:
                st.markdown("**Aniqlangan muammolar:**")
                for ind in corruption_result["indicators"]:
                    st.markdown(f"- {ind['matn']}")
            
            st.session_state["demo_loaded"] = False
        else:
            st.error("❌ Saqlashda xato yuz berdi!")
