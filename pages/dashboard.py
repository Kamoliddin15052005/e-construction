import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_store import load_applications, get_statistics

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


def render():
    st.markdown("## 📊 Statistika & Dashboard")

    applications = load_applications()
    stats = get_statistics()

    # KPI kartochkalar
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = [
        ("📋 Jami", stats["total"], None, "#1565c0"),
        ("🔴 Xavfli", stats["red"], None, "#f44336"),
        ("🟡 Tekshiruvda", stats["yellow"], None, "#ff9800"),
        ("🟢 Toza", stats["green"], None, "#4caf50"),
        ("📈 O'rt.xavf", f"{stats['avg_risk']:.0f}%", None, "#9c27b0"),
    ]
    
    for col, (label, value, delta, color) in zip([col1,col2,col3,col4,col5], metrics):
        with col:
            st.markdown(f"""
            <div style="background:{color}11;border:2px solid {color};border-radius:10px;
                        padding:1rem;text-align:center">
                <h3 style="color:{color};margin:0">{value}</h3>
                <p style="margin:0;color:#555;font-size:0.85rem">{label}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    if not applications:
        st.warning("Ma'lumot yo'q")
        return

    if PLOTLY_AVAILABLE:
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk taqsimoti - Pie chart
            flags = [a.get("flag", "green") for a in applications]
            flag_counts = {
                "🔴 Jiddiy xavf": flags.count("red"),
                "🟠 O'rta xavf": flags.count("orange"),
                "🟡 Past xavf": flags.count("yellow"),
                "🟢 Xavfsiz": flags.count("green")
            }
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=list(flag_counts.keys()),
                values=list(flag_counts.values()),
                marker_colors=["#f44336", "#ff9800", "#ffc107", "#4caf50"],
                hole=0.4
            )])
            fig_pie.update_layout(title="Risk Taqsimoti", height=350,
                                   font=dict(family="Arial"))
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Risk ball taqsimoti - Histogram
            risk_scores = [a.get("risk_score", 0) for a in applications]
            
            fig_hist = go.Figure(data=[go.Histogram(
                x=risk_scores,
                nbinsx=10,
                marker_color="#1565c0",
                opacity=0.8
            )])
            fig_hist.update_layout(
                title="Xavf Bali Taqsimoti",
                xaxis_title="Xavf Bali (0-100)",
                yaxis_title="Arizalar soni",
                height=350
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        # Vaqt bo'yicha tendensiya
        if len(applications) >= 3:
            dates = [a.get("sana", "2025-01-01") for a in applications]
            risks = [a.get("risk_score", 0) for a in applications]
            names = [a.get("loyiha_nomi", "?")[:20] for a in applications]
            
            fig_scatter = go.Figure(data=[go.Scatter(
                x=list(range(len(applications))),
                y=risks,
                mode="markers+lines",
                marker=dict(
                    size=12,
                    color=risks,
                    colorscale="RdYlGn_r",
                    showscale=True,
                    colorbar=dict(title="Xavf")
                ),
                text=names,
                hovertemplate="<b>%{text}</b><br>Xavf: %{y}<extra></extra>"
            )])
            
            fig_scatter.add_hline(y=70, line_dash="dash", line_color="red",
                                   annotation_text="Kritik chegara (70)")
            fig_scatter.add_hline(y=40, line_dash="dash", line_color="orange",
                                   annotation_text="Ogohlantirish (40)")
            
            fig_scatter.update_layout(
                title="Arizalar Bo'yicha Xavf Tendensiyasi",
                xaxis_title="Ariza raqami",
                yaxis_title="Xavf bali",
                height=350
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    else:
        st.warning("Chartlar uchun: `pip install plotly`")

    st.divider()

    # Arizalar jadvali
    st.markdown("### 📋 Barcha Arizalar")
    
    # Jadval sarlavhalari
    header_cols = st.columns([1.5, 2.5, 1.5, 1, 1, 1, 1])
    headers = ["ID", "Loyiha", "Tadbirkor", "Xavf", "Flag", "Holat", "Sana"]
    for col, header in zip(header_cols, headers):
        with col:
            st.markdown(f"**{header}**")
    
    st.markdown("---")
    
    sorted_apps = sorted(applications, key=lambda x: x.get("risk_score", 0), reverse=True)
    
    for app in sorted_apps:
        flag = app.get("flag", "green")
        flag_icon = {"red": "🔴", "orange": "🟠", "yellow": "🟡", "green": "🟢"}.get(flag, "⚪")
        risk = app.get("risk_score", 0)
        
        row_cols = st.columns([1.5, 2.5, 1.5, 1, 1, 1, 1])
        with row_cols[0]:
            st.markdown(f"`{app.get('id','?')}`")
        with row_cols[1]:
            st.markdown(f"{app.get('loyiha_nomi','?')[:25]}")
        with row_cols[2]:
            st.markdown(f"{app.get('tadbirkor','?')[:20]}")
        with row_cols[3]:
            color = "#f44336" if risk >= 70 else "#ff9800" if risk >= 40 else "#4caf50"
            st.markdown(f"<span style='color:{color};font-weight:bold'>{risk}</span>", 
                       unsafe_allow_html=True)
        with row_cols[4]:
            st.markdown(flag_icon)
        with row_cols[5]:
            st.markdown(f"{app.get('holat','?')}")
        with row_cols[6]:
            st.markdown(f"{app.get('sana','?')}")
