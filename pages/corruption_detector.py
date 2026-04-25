import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_store import load_applications
from utils.ai_analyzer import calculate_corruption_score, analyze_rejection_reasons


def render():
    st.markdown("## 🚨 Korrupsiya Detektori")
    st.markdown("Barcha arizalar bo'yicha korrupsion xavf tahlili")

    applications = load_applications()
    
    if not applications:
        st.warning("Hali ariza yo'q.")
        return

    # Filter
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_flag = st.multiselect("🎨 Filter (rang):", ["red", "orange", "yellow", "green"], 
                                      default=["red", "orange", "yellow", "green"])
    with col2:
        min_risk = st.slider("Minimal xavf balli:", 0, 100, 0)
    with col3:
        sort_by = st.selectbox("Saralash:", ["Xavf balli (yuqori-past)", "Sana (yangi)", "ID"])

    st.divider()

    # Arizalarni filtrlash va saralash
    filtered = [a for a in applications if a.get("flag", "green") in filter_flag
                and a.get("risk_score", 0) >= min_risk]
    
    if sort_by == "Xavf balli (yuqori-past)":
        filtered = sorted(filtered, key=lambda x: x.get("risk_score", 0), reverse=True)

    # Umumiy statistika
    if filtered:
        col1, col2, col3, col4 = st.columns(4)
        red_count = sum(1 for a in filtered if a.get("flag") == "red")
        orange_count = sum(1 for a in filtered if a.get("flag") == "orange")
        yellow_count = sum(1 for a in filtered if a.get("flag") == "yellow")
        green_count = sum(1 for a in filtered if a.get("flag") == "green")
        
        with col1:
            st.markdown(f"""<div style="background:#ffebee;border-radius:8px;padding:0.8rem;text-align:center;border:2px solid #f44336">
                <h3 style="color:#f44336;margin:0">🔴 {red_count}</h3><p style="margin:0">Jiddiy xavf</p></div>""",
                unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div style="background:#fff3e0;border-radius:8px;padding:0.8rem;text-align:center;border:2px solid #ff9800">
                <h3 style="color:#ff9800;margin:0">🟠 {orange_count}</h3><p style="margin:0">O'rta xavf</p></div>""",
                unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div style="background:#fffde7;border-radius:8px;padding:0.8rem;text-align:center;border:2px solid #ffc107">
                <h3 style="color:#ff9800;margin:0">🟡 {yellow_count}</h3><p style="margin:0">Past xavf</p></div>""",
                unsafe_allow_html=True)
        with col4:
            st.markdown(f"""<div style="background:#e8f5e9;border-radius:8px;padding:0.8rem;text-align:center;border:2px solid #4caf50">
                <h3 style="color:#4caf50;margin:0">🟢 {green_count}</h3><p style="margin:0">Xavfsiz</p></div>""",
                unsafe_allow_html=True)
    
    st.divider()

    # Ariza kartochkalari
    for app in filtered:
        flag = app.get("flag", "green")
        risk = app.get("risk_score", 0)
        
        # Rang tanlash
        if flag == "red":
            border_color = "#f44336"
            bg_color = "#fff5f5"
            flag_icon = "🔴"
        elif flag == "orange":
            border_color = "#ff9800"
            bg_color = "#fffbf0"
            flag_icon = "🟠"
        elif flag == "yellow":
            border_color = "#ffc107"
            bg_color = "#fffff0"
            flag_icon = "🟡"
        else:
            border_color = "#4caf50"
            bg_color = "#f5fff5"
            flag_icon = "🟢"

        with st.container():
            st.markdown(f"""
            <div style="background:{bg_color};border:2px solid {border_color};border-radius:12px;
                        padding:1.2rem;margin-bottom:1rem">
                <div style="display:flex;justify-content:space-between;align-items:flex-start">
                    <div>
                        <span style="font-size:1.5rem">{flag_icon}</span>
                        <strong style="font-size:1.1rem"> {app.get('loyiha_nomi','N/A')}</strong><br>
                        <span style="color:#666">📋 {app.get('id','?')} | 👤 {app.get('tadbirkor','?')}</span><br>
                        <span style="color:#666">📍 {app.get('manzil','?')} | 🏢 {app.get('tur','?')}</span>
                    </div>
                    <div style="text-align:right">
                        <div style="background:{border_color};color:white;padding:0.5rem 1rem;
                                    border-radius:20px;font-weight:bold;font-size:1.2rem">
                            {risk}/100
                        </div>
                        <small style="color:#888">{app.get('sana','')}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander(f"🔍 {app.get('id','?')} - Tafsilotlar ko'rish"):
                col1, col2, col3 = st.columns(3)
                
                # Mezon balli
                criteria_scores = app.get("criteria_scores", {})
                total_score = sum(criteria_scores.values()) if criteria_scores else 0
                with col1:
                    st.metric("📊 Mezon balli", f"{total_score}/350", 
                              delta=f"{(total_score/350*100):.0f}%")
                
                # Tasdiqlovchilar
                depts = app.get("dept_approvals", {})
                approved_count = sum(1 for v in depts.values() if v)
                with col2:
                    st.metric("✅ Tasdiqlovchilar", f"{approved_count}/4")
                
                # Foydalanuvchi bahosi
                user_rating = app.get("user_rating")
                with col3:
                    if user_rating:
                        st.metric("⭐ Foydalanuvchi", f"{user_rating:.1f}/5.0")
                    else:
                        st.metric("⭐ Foydalanuvchi", "Hali yo'q")

                # Korrupsiya belgilari
                corruption_result = app.get("corruption_result", {})
                indicators = corruption_result.get("indicators", [])
                
                if indicators:
                    st.markdown("**🚨 Aniqlangan korrupsion belgilar:**")
                    for ind in indicators:
                        st.markdown(f"""
                        <div style="background:{ind.get('rang','#999')}22;border-left:3px solid {ind.get('rang','#999')};
                                    padding:0.5rem 0.8rem;margin:0.3rem 0;border-radius:0 6px 6px 0">
                            {ind['matn']}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("✅ Korrupsion belgilar aniqlanmadi")

                # Bo'limlar tasdiqlashlari
                st.markdown("**Bo'limlar holati:**")
                dept_names = {
                    "sanitariya": "🧪 Sanitariya",
                    "yonghin": "🔥 Yong'in",
                    "ekologiya": "🌿 Ekologiya",
                    "qurilish": "🏗️ Qurilish"
                }
                
                cols = st.columns(4)
                for i, (dept_key, dept_name) in enumerate(dept_names.items()):
                    with cols[i]:
                        approved = depts.get(dept_key, False)
                        if approved:
                            st.success(f"{dept_name} ✅")
                        else:
                            st.error(f"{dept_name} ❌")

                # Rad etish sababi
                if app.get("rad_sabab"):
                    with st.expander("📄 Rad etish sabablari"):
                        st.markdown(f"""
                        <div style="background:#ffebee;border-radius:8px;padding:0.8rem">
                            {app.get('rad_sabab')}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if app.get("ozgartirishlar"):
                        with st.expander("🔧 O'zgartirishlar"):
                            st.markdown(app.get("ozgartirishlar"))

                # Qaror tugmalari
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    if st.button(f"📧 Hisobot yuborish", key=f"report_{app.get('id')}"):
                        st.info("Hisobot yuborildi (demo rejim)")
                with col_b:
                    if st.button(f"🔍 Tekshiruvga yuborish", key=f"check_{app.get('id')}"):
                        st.warning("Tekshiruv uchun yuborildi (demo rejim)")
                with col_c:
                    if st.button(f"✅ Toza deb belgilash", key=f"clean_{app.get('id')}"):
                        st.success("Toza deb belgilandi (demo rejim)")
