import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="E-Construction | Korrupsiya Detektori",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #1565c0 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #1565c0;
    }
    .red-flag {
        background: linear-gradient(135deg, #ffebee, #ffcdd2);
        border: 2px solid #f44336;
        border-radius: 10px;
        padding: 1.2rem;
        animation: pulse 1.5s infinite;
    }
    .green-flag {
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        border: 2px solid #4caf50;
        border-radius: 10px;
        padding: 1.2rem;
    }
    .yellow-flag {
        background: linear-gradient(135deg, #fffde7, #fff9c4);
        border: 2px solid #ff9800;
        border-radius: 10px;
        padding: 1.2rem;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(244,67,54,0.4); }
        70% { box-shadow: 0 0 0 10px rgba(244,67,54,0); }
        100% { box-shadow: 0 0 0 0 rgba(244,67,54,0); }
    }
    .dept-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }
    .criteria-row {
        border-bottom: 1px solid #eee;
        padding: 0.5rem 0;
    }
    .score-bar {
        height: 8px;
        border-radius: 4px;
        background: #eee;
    }
    .timeline-step {
        display: flex;
        align-items: flex-start;
        margin-bottom: 1rem;
        padding: 0.8rem;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 3px solid #1565c0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🏗️ E-Construction Anti-Korrupsiya Tizimi</h1>
    <p style="font-size:1.1rem; opacity:0.9;">
        Qurilish ruxsatnomalari bo'yicha korrupsion holatlarni aniqlash va oldini olish
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Flag_of_Uzbekistan.svg/200px-Flag_of_Uzbekistan.svg.png", width=120)
    st.markdown("### 📋 Navigatsiya")
    
    page = st.radio("", [
        "🏠 Bosh sahifa",
        "📝 Ariza kiritish",
        "🔍 AI Tahlil",
        "🚨 Korrupsiya Detektori",
        "⭐ Foydalanuvchi Baholari",
        "📊 Statistika & Dashboard",
        "⚙️ Sozlamalar"
    ])
    
    st.divider()
    
    # System stats
    st.markdown("### 📈 Tizim Statistikasi")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Jami ariza", "1,247")
        st.metric("🚨 Xavfli", "89")
    with col2:
        st.metric("✅ Toza", "1,091")
        st.metric("⚠️ Tekshiruvda", "67")
    
    st.divider()
    st.caption("Versiya: 1.0.0 | 2025")
    st.caption("O'zbekiston Respublikasi")

# Route pages
if page == "🏠 Bosh sahifa":
    from pages import home
    home.render()
elif page == "📝 Ariza kiritish":
    from pages import application
    application.render()
elif page == "🔍 AI Tahlil":
    from pages import ai_analysis
    ai_analysis.render()
elif page == "🚨 Korrupsiya Detektori":
    from pages import corruption_detector
    corruption_detector.render()
elif page == "⭐ Foydalanuvchi Baholari":
    from pages import user_reviews
    user_reviews.render()
elif page == "📊 Statistika & Dashboard":
    from pages import dashboard
    dashboard.render()
elif page == "⚙️ Sozlamalar":
    from pages import settings
    settings.render()
