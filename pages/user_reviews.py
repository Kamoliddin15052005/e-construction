import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_store import load_applications, update_application
from utils.ai_analyzer import calculate_corruption_score, analyze_rejection_reasons


def render():
    st.markdown("## ⭐ Foydalanuvchi Baholari")
    st.markdown("Qurilish tugagach, xonadon egolari loyihani 1-5 yulduz bilan baholaydi")

    applications = load_applications()
    
    # Faqat tasdiqlangan arizalar
    approved_apps = [a for a in applications if a.get("holat") == "tasdiqlangan" or 
                     all(a.get("dept_approvals", {}).values())]

    if not approved_apps:
        st.info("Hozircha tasdiqlangan loyiha yo'q. Demo ma'lumotlarda tasdiqlangan ariza mavjud.")
        approved_apps = applications  # Demo uchun hammasini ko'rsatish
    
    st.divider()

    for app in approved_apps:
        with st.container():
            flag = app.get("flag", "green")
            flag_icon = {"red": "🔴", "orange": "🟠", "yellow": "🟡", "green": "🟢"}.get(flag, "⚪")
            
            st.markdown(f"""
            <div style="background:#f8f9fa;border-radius:10px;padding:1rem;margin-bottom:0.5rem;
                        border-left:4px solid #1565c0">
                <strong>{flag_icon} {app.get('loyiha_nomi','?')}</strong> | 
                {app.get('id','?')} | 📍 {app.get('manzil','?')}
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander(f"⭐ Baho qo'shish / ko'rish - {app.get('id','?')}"):
                current_rating = app.get("user_rating")
                
                if current_rating:
                    stars = "⭐" * int(current_rating) + "☆" * (5 - int(current_rating))
                    rating_color = "#4caf50" if current_rating >= 4 else "#ff9800" if current_rating >= 3 else "#f44336"
                    
                    st.markdown(f"""
                    <div style="background:{rating_color}22;border:2px solid {rating_color};
                                border-radius:8px;padding:1rem;text-align:center">
                        <h3 style="color:{rating_color};margin:0">{stars}</h3>
                        <h2 style="color:{rating_color};margin:0">{current_rating:.1f} / 5.0</h2>
                        <p style="margin:0.3rem 0 0;color:#555">O'rtacha foydalanuvchi bahosi</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Hali baho berilmagan")

                st.markdown("---")
                st.markdown("**Yangi baho qo'shish:**")
                
                col1, col2 = st.columns([2, 3])
                with col1:
                    new_rating = st.slider(
                        "Yulduz baho:", 1, 5, 3,
                        key=f"rating_{app.get('id')}",
                        help="1=Juda yomon, 5=Juda yaxshi"
                    )
                    
                    rating_labels = {1: "⭐ Juda yomon", 2: "⭐⭐ Yomon", 
                                    3: "⭐⭐⭐ O'rtacha", 4: "⭐⭐⭐⭐ Yaxshi", 
                                    5: "⭐⭐⭐⭐⭐ Juda yaxshi"}
                    st.markdown(f"**{rating_labels[new_rating]}**")
                
                with col2:
                    review_text = st.text_area(
                        "Izoh (ixtiyoriy):",
                        placeholder="Qurilish sifati, qoidalarga rioya, muammolar haqida...",
                        height=100,
                        key=f"review_{app.get('id')}"
                    )

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button(f"💾 Bahoni saqlash", key=f"save_rating_{app.get('id')}", type="primary"):
                        # O'rtacha hisoblash (demo: yangi qiymat = hozirgi baho)
                        avg_rating = float(new_rating)
                        
                        # Korrupsiya ballini qayta hisoblash
                        criteria_scores = app.get("criteria_scores", {})
                        dept_approvals = app.get("dept_approvals", {})
                        rad_sabab = app.get("rad_sabab", "")
                        ozgartirishlar = app.get("ozgartirishlar", "")
                        
                        rej_analysis = analyze_rejection_reasons(rad_sabab, ozgartirishlar)
                        
                        new_corruption = calculate_corruption_score(
                            criteria_scores=criteria_scores,
                            dept_approvals=dept_approvals,
                            rejection_analysis=rej_analysis,
                            user_rating=avg_rating
                        )
                        
                        success = update_application(app.get("id"), {
                            "user_rating": avg_rating,
                            "review_text": review_text,
                            "risk_score": new_corruption["total_risk_score"],
                            "flag": new_corruption["flag_color"],
                            "corruption_result": new_corruption
                        })
                        
                        if success:
                            st.success(f"✅ Baho saqlandi! Yangi xavf balli: {new_corruption['total_risk_score']}/100")
                            
                            if new_corruption["flag_color"] == "red":
                                st.error(f"🚨 Diqqat! Foydalanuvchi bahosi qo'shilgach xavf oshdi: {new_corruption['verdict']}")
                            
                            st.rerun()
                        else:
                            st.error("Saqlashda xato")

                with col_b:
                    # AI taqqoslash ko'rsatish
                    if current_rating and app.get("dept_approvals"):
                        approved_count = sum(1 for v in app.get("dept_approvals", {}).values() if v)
                        
                        if current_rating < 3 and approved_count >= 3:
                            st.warning(f"⚠️ NOMOS: {approved_count} organ tasdiqlagan lekin baho {current_rating:.1f}/5!")
                        elif current_rating >= 4:
                            st.success("✅ Baho yuqori, mos keladi")
