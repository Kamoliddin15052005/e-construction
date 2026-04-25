import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_store import load_applications
from utils.ai_analyzer import analyze_with_hf_api, local_text_analysis
from utils.criteria_engine import CRITERIA, get_max_total_score


def render():
    st.markdown("## 🔍 AI Tahlil Markazi")

    # HF Token
    with st.expander("⚙️ HuggingFace API Sozlamalari", expanded=False):
        st.markdown("""
        **Bepul token olish:**
        1. [huggingface.co](https://huggingface.co) ga o'ting
        2. Ro'yxatdan o'ting (bepul)
        3. Settings → Access Tokens → New Token (Read)
        4. Tokenni quyida kiriting
        
        **Bepul modellar:** Mistral-7B, Zephyr-7B, Phi-2, Llama-3-8B
        """)
        hf_token = st.text_input("HuggingFace Token", type="password",
                                  placeholder="hf_xxxxxxxxxxxxxxxxxxxx",
                                  value=st.session_state.get("hf_token", ""))
        if hf_token:
            st.session_state["hf_token"] = hf_token
            st.success("✅ Token saqlandi!")

    st.divider()

    # Arizalar tanlash
    applications = load_applications()
    if not applications:
        st.warning("Hali ariza yo'q. Avval ariza kiritish kerak.")
        return

    app_options = {f"{a['id']} - {a.get('loyiha_nomi','?')} ({a.get('flag','?').upper()})": a
                   for a in applications}
    
    selected_label = st.selectbox("📋 Arizani tanlang:", list(app_options.keys()))
    app = app_options[selected_label]

    st.divider()

    tab1, tab2, tab3 = st.tabs(["📊 Mezon Tahlili", "🔄 Rad Etish Tahlili", "🤖 AI Matn Tahlili"])

    with tab1:
        st.markdown("### 📊 20 Mezon Bo'yicha Tafsilotli Tahlil")
        
        criteria_scores = app.get("criteria_scores", {})
        total_max = get_max_total_score()
        total_score = sum(criteria_scores.values()) if criteria_scores else 0
        pct = (total_score / total_max * 100) if total_max > 0 else 0
        
        # Umumiy ball
        color = "#4caf50" if pct >= 70 else "#ff9800" if pct >= 50 else "#f44336"
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{color}22,{color}11);border:2px solid {color};
                    border-radius:12px;padding:1.5rem;text-align:center;margin-bottom:1rem">
            <h2 style="color:{color};margin:0">{total_score} / {total_max} ball ({pct:.1f}%)</h2>
            <p style="color:#555;margin:0.5rem 0 0">Umumiy mezon balli</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(pct / 100)
        
        # Bo'limlar bo'yicha
        for dept_key, dept_data in CRITERIA.items():
            dept_max = sum(m["max_ball"] for m in dept_data["mezonlar"])
            dept_score = sum(criteria_scores.get(m["id"], 0) for m in dept_data["mezonlar"])
            dept_pct = (dept_score / dept_max * 100) if dept_max > 0 else 0
            
            approved = app.get("dept_approvals", {}).get(dept_key, False)
            approved_icon = "✅" if approved else "❌"
            
            with st.expander(f"{dept_data['nomi']} - {dept_score}/{dept_max} ({dept_pct:.0f}%) {approved_icon}"):
                for mezon in dept_data["mezonlar"]:
                    score = criteria_scores.get(mezon["id"], 0)
                    m_pct = (score / mezon["max_ball"] * 100) if mezon["max_ball"] > 0 else 0
                    bar_color = "#4caf50" if m_pct >= 70 else "#ff9800" if m_pct >= 40 else "#f44336"
                    
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{mezon['nomi']}**")
                        st.markdown(f"""
                        <div style="background:#eee;border-radius:4px;height:8px;margin:4px 0">
                            <div style="background:{bar_color};width:{m_pct}%;height:8px;border-radius:4px"></div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"**{score}/{mezon['max_ball']}**")

    with tab2:
        st.markdown("### 🔄 Rad Etish ~ O'zgartirishlar Taqqoslaması")
        
        rad_sabab = app.get("rad_sabab", "")
        ozgartirishlar = app.get("ozgartirishlar", "")
        
        if not rad_sabab:
            st.success("✅ Bu ariza hali qaytarilmagan yoki rad etish sababi yo'q.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**❌ Rad etish sabablari:**")
                st.markdown(f"""
                <div style="background:#ffebee;border:1px solid #f44336;border-radius:8px;padding:1rem">
                    {rad_sabab}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("**🔧 Amalga oshirilgan o'zgartirishlar:**")
                st.markdown(f"""
                <div style="background:#e8f5e9;border:1px solid #4caf50;border-radius:8px;padding:1rem">
                    {ozgartirishlar if ozgartirishlar else "O'zgartirishlar ko'rsatilmagan"}
                </div>
                """, unsafe_allow_html=True)
            
            # Tahlil
            from utils.ai_analyzer import analyze_rejection_reasons
            analysis = analyze_rejection_reasons(rad_sabab, ozgartirishlar)
            
            st.markdown("#### 🔍 Avtomatik Taqqoslash Natijasi:")
            
            addr_rate = analysis.get("address_rate", 0)
            color = "#4caf50" if addr_rate > 0.7 else "#ff9800" if addr_rate > 0.4 else "#f44336"
            
            st.markdown(f"""
            <div style="background:{color}22;border:2px solid {color};border-radius:8px;padding:1rem">
                <strong>Hal qilinish darajasi: {addr_rate*100:.0f}%</strong><br>
                Rad etish sabablaridan {analysis.get('rejection_issues_count',0)} ta topildi
            </div>
            """, unsafe_allow_html=True)
            
            for inc in analysis.get("inconsistencies", []):
                st.warning(inc)

    with tab3:
        st.markdown("### 🤖 HuggingFace AI Matn Tahlili")
        
        # Mahalliy tahlil
        all_text = f"{app.get('tavsif','')} {rad_sabab} {ozgartirishlar}"
        local = local_text_analysis(all_text)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**⚡ Mahalliy (tezkor) tahlil:**")
            if local["risk_words"]:
                st.warning(f"Xavfli kalit so'zlar: {', '.join(local['risk_words'][:5])}")
            else:
                st.success("Xavfli kalit so'zlar topilmadi")
            
            if local.get("suspicious"):
                st.error("⚠️ Shubhali pattern: Ko'p ijobiy, hech qanday muammo yo'q")
        
        with col2:
            st.markdown("**🤖 Mistral-7B (HuggingFace API) tahlili:**")
            
            hf_token = st.session_state.get("hf_token", "")
            if not hf_token:
                st.info("💡 HuggingFace tokeni kiriting (yuqorida ⚙️)")
            else:
                analyze_text = st.text_area("Tahlil qilinadigan matn:", value=all_text[:500], height=100)
                
                if st.button("🚀 AI Tahlil Boshlash", type="primary"):
                    with st.spinner("Mistral-7B tahlil qilmoqda..."):
                        result = analyze_with_hf_api(analyze_text, hf_token)
                    
                    if result:
                        st.markdown("**AI Xulosasi:**")
                        st.markdown(f"""
                        <div style="background:#f3e5f5;border:1px solid #9c27b0;border-radius:8px;padding:1rem">
                            {result}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("AI dan javob olinmadi. Tokenni tekshiring.")
