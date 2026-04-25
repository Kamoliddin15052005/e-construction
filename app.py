"""
E-Construction Anti-Corruption AI System
Qurilish sohasidagi korrupsiyani aniqlash tizimi
"""

import streamlit as st
import json
import os
import numpy as np
from datetime import datetime
from pathlib import Path

# ──────────────────────────────────────────────
#  PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="E-Construction | Korrupsiyaga qarshi AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
#  STYLE
# ──────────────────────────────────────────────
st.markdown("""
<style>
    .risk-red    { background:#fee2e2; border-left:5px solid #dc2626; padding:12px 16px; border-radius:6px; margin:8px 0; }
    .risk-yellow { background:#fef9c3; border-left:5px solid #ca8a04; padding:12px 16px; border-radius:6px; margin:8px 0; }
    .risk-green  { background:#dcfce7; border-left:5px solid #16a34a; padding:12px 16px; border-radius:6px; margin:8px 0; }
    .metric-box  { background:#f8fafc; border:1px solid #e2e8f0; padding:16px; border-radius:8px; text-align:center; }
    .dept-header { font-weight:700; font-size:15px; color:#1e293b; margin-bottom:6px; }
    .stProgress > div > div { border-radius:4px; }
    h2 { color: #1e3a5f; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  DATA STORE  (JSON fayl — SQLite o'rniga sodda)
# ──────────────────────────────────────────────
DATA_FILE = Path("data/applications.json")
DATA_FILE.parent.mkdir(exist_ok=True)

def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return []

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# ──────────────────────────────────────────────
#  20 MEZON  (4 bo'lim × 5 mezon)
# ──────────────────────────────────────────────
CRITERIA = {
    "🧪 Sanitariya-Epidemiologiya": [
        {"id":  1, "name": "Sanitariya himoya zona masofalari",     "w": 5,
         "desc": "Turar-joy sanitariya himoya zonasidan ≥ belgilangan metr masofada"},
        {"id":  2, "name": "Suv ta'minoti va kanalizatsiya",         "w": 5,
         "desc": "Markaziy suv va kanalizatsiyaga ulanish loyihada ko'rsatilgan"},
        {"id":  3, "name": "Chiqindi saqlash va chiqarish tizimi",   "w": 4,
         "desc": "Har bir podyezd uchun chiqindi kamerasi va konteyner maydonchalari"},
        {"id":  4, "name": "Shamollatish va havo almashinuvi",       "w": 4,
         "desc": "Barcha xonalar tabiiy yoki mexanik shamollatish tizimiga ega"},
        {"id":  5, "name": "Shovqin/vibratsiya normalariga muvofiqligi", "w": 3,
         "desc": "Tashqi va ichki shovqin darajasi SanPin talablariga mos"},
    ],
    "🔥 Yong'in Xavfsizligi": [
        {"id":  6, "name": "Yong'in o'chirish tizimi (sprinkler/gidrant)", "w": 5,
         "desc": "Har qavatda yong'in o'chirish tizimi loyihada mavjud"},
        {"id":  7, "name": "Evakuatsiya yo'llari va zina kengligi",  "w": 5,
         "desc": "Evakuatsiya yo'llari soni va kengligi normaga mos (≥1.2 m)"},
        {"id":  8, "name": "Yong'inga chidamli konstruksiyalar",     "w": 5,
         "desc": "Fen'derlar va to'sinlar REI-90+ sinfiga mos"},
        {"id":  9, "name": "Avtomatik yong'in signalizatsiyasi",     "w": 4,
         "desc": "Barcha qavatlar va texnik xonalarda sensor mavjud"},
        {"id": 10, "name": "Yong'in suv bosimi va zaxirasi",         "w": 3,
         "desc": "Yong'in suv ta'minoti bosimi ≥ 0.15 MPa, zaxira ≥ 10 m³"},
    ],
    "🌿 Ekologiya": [
        {"id": 11, "name": "Havo ifloslanishi nazorati (qurilish)",  "w": 4,
         "desc": "Qurilish changi va gazini kamaytirish plani mavjud"},
        {"id": 12, "name": "Tuproq va grunt suvi muhofazasi",        "w": 4,
         "desc": "Poydevor izolatsiyasi va neft mahsulotlari tutqichi loyihada"},
        {"id": 13, "name": "Ko'kalamzorlashtirish normasi (≥20%)",   "w": 3,
         "desc": "Umumiy maydonning 20% dan kam bo'lmagan qismi yashil maydon"},
        {"id": 14, "name": "Qurilish chiqindilari utilizatsiya shartnomasi", "w": 3,
         "desc": "Litsenziyalangan firma bilan chiqindi utilizatsiya shartnomasi"},
        {"id": 15, "name": "Suv havzalariga ta'sir baholash (OVOS)", "w": 4,
         "desc": "Yaqin suv obyektlariga ≤ 500 m bo'lsa OVOS xulosasi talab"},
    ],
    "🏗️ Qurilish Bo'limi": [
        {"id": 16, "name": "Loyiha hujjatlariga to'liq muvofiqlik",  "w": 5,
         "desc": "Barcha qurilish ishlari tasdiqlangan loyihaga aniq mos"},
        {"id": 17, "name": "Seysmik bardoshlilik (MSK-64 bo'yicha)", "w": 5,
         "desc": "Toshkent uchun 8-9 ball seysmik zona talablari bajarilgan"},
        {"id": 18, "name": "Muhandislik kommunikatsiyalar loyihasi", "w": 4,
         "desc": "Elektr, gaz, issiqlik, internet kommunikatsiyalar loyihada"},
        {"id": 19, "name": "Qurilish materiallari sifat sertifikatlari", "w": 4,
         "desc": "Tsement, temir, g'isht va boshqa asosiy materiallar sertifikati"},
        {"id": 20, "name": "Konstruktiv mustahkamlik ekspertizasi",  "w": 5,
         "desc": "Mustaqil ekspert tashkilotining mustahkamlik xulosasi mavjud"},
    ],
}

MAX_SCORE = sum(c["w"] for dept in CRITERIA.values() for c in dept)  # 85

# ──────────────────────────────────────────────
#  AI  —  HuggingFace Inference API (bepul)
# ──────────────────────────────────────────────
HF_TOKEN = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN", ""))
EMBED_API = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

@st.cache_data(show_spinner=False, ttl=3600)
def get_embeddings(texts: list[str]) -> np.ndarray:
    """
    HuggingFace Inference API orqali matn embeddinglarini olish.
    Model: paraphrase-multilingual-MiniLM-L12-v2
    Token shart emas (bepul, lekin sekin) — token bo'lsa tezroq.
    """
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    resp = requests.post(EMBED_API, headers=headers, json={"inputs": texts}, timeout=30)
    if resp.status_code != 200:
        return None
    return np.array(resp.json())

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))

def compare_docs(rejected_text: str, approved_text: str) -> dict:
    """
    Rad etilgan va tasdiqlangan hujjatlar o'rtasidagi o'xshashlikni aniqlash.
    Agar o'xshashlik > 92% → korrupsion xavf belgisi.
    """
    import requests as req_lib
    embeddings = get_embeddings([rejected_text, approved_text])
    if embeddings is None:
        # Fallback: oddiy so'z takrorlanishi hisoblash
        words_r = set(rejected_text.lower().split())
        words_a = set(approved_text.lower().split())
        sim = len(words_r & words_a) / (len(words_r | words_a) + 1e-9)
        method = "fallback (jaccard)"
    else:
        sim = cosine_sim(embeddings[0], embeddings[1])
        method = "semantic (MiniLM)"

    threshold = 0.92
    risk = sim >= threshold
    return {
        "similarity": sim,
        "method": method,
        "is_risk": risk,
        "label": "🔴 XAVF: Hujjatlar deyarli bir xil!" if risk else "🟢 Hujjatlar farqlanadi",
    }

def score_to_risk(score: int, max_score: int = MAX_SCORE) -> dict:
    """
    Ball asosida xavf darajasini aniqlash.
    Lekin ruxsat BERILGAN bo'lsa, past ball = qo'shimcha xavf.
    """
    pct = score / max_score * 100
    if pct >= 80:
        return {"level": "low",    "label": "🟢 Past xavf",      "color": "green"}
    elif pct >= 60:
        return {"level": "medium", "label": "🟡 O'rta xavf",     "color": "yellow"}
    else:
        return {"level": "high",   "label": "🔴 Yuqori xavf",    "color": "red"}

def review_vs_official(avg_review: float, official_approved: bool) -> dict:
    """
    Foydalanuvchi baholari va rasmiy xulosa o'rtasidagi nomuvofiqlik.
    Rasmiy: tasdiqlangan. Foydalanuvchilar: ≤ 2.5 ball → xavf.
    """
    if official_approved and avg_review <= 2.5:
        return {"risk": True,  "label": "🔴 Rasmiy vs Foydalanuvchi: katta farq!"}
    elif official_approved and avg_review <= 3.5:
        return {"risk": False, "label": "🟡 Rasmiy vs Foydalanuvchi: kichik farq"}
    else:
        return {"risk": False, "label": "🟢 Rasmiy va foydalanuvchi xulosalari mos"}

# ──────────────────────────────────────────────
#  SIDEBAR NAVIGATION
# ──────────────────────────────────────────────
import requests  # noqa

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/128/1995/1995574.png", width=60)
    st.title("🏗️ E-Construction")
    st.caption("Korrupsiyaga qarshi AI tizimi")
    st.divider()

    page = st.radio(
        "Bo'lim tanlang:",
        ["📋 Ariza kiritish",
         "📄 Hujjat taqqoslash",
         "✅ 20 Mezon baholash",
         "⭐ Foydalanuvchi fikrlari",
         "📊 Dashboard"],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("**HF Token holati:**")
    if HF_TOKEN:
        st.success("✅ Token ulangan")
    else:
        st.warning("⚠️ Token yo'q — bepul rejim (sekin)")
        st.info("Token ulash uchun: `.streamlit/secrets.toml` ga `HF_TOKEN = 'hf_...'` qo'shing")

# ──────────────────────────────────────────────
#  PAGE 1: ARIZA KIRITISH
# ──────────────────────────────────────────────
if page == "📋 Ariza kiritish":
    st.header("📋 Yangi ariza kiritish")
    st.caption("my.gov.uz dan kelgan ariza ma'lumotlarini kiriting")

    with st.form("app_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            ariza_id   = st.text_input("Ariza raqami (my.gov.uz)", placeholder="2024-QB-001234")
            tadbirkor  = st.text_input("Tadbirkor / Buyurtmachi")
            loyiha_tur = st.selectbox("Loyiha turi", [
                "Ko'p qavatli turar-joy (≥ 5 qavat)",
                "Ko'p qavatli turar-joy (< 5 qavat)",
                "Tijorat binosi",
                "Ishlab chiqarish obyekti",
                "Ijtimoiy obyekt",
            ])
        with col2:
            manzil     = st.text_input("Obyekt manzili", placeholder="Toshkent, Yunusobod t., ...")
            qavatlar   = st.number_input("Qavatlar soni", 1, 50, 16)
            status     = st.selectbox("Ariza holati", [
                "Yangi (ko'rib chiqilmoqda)",
                "Rad etildi",
                "Tasdiqlandi — qurilish boshlash ruxsatnomasi",
                "Tasdiqlandi — foydalanishga topshirish ruxsatnomasi",
            ])

        st.subheader("Rad etish sabablari (agar bo'lsa)")
        rad_sabablar = st.text_area(
            "Vakolatli organlar ko'rsatgan sabablar:",
            placeholder="Masalan: Yong'in o'chirish tizimi loyihasida yo'q. Evakuatsiya zinalari normaga mos emas...",
            height=100,
        )

        izoh = st.text_area("Qo'shimcha izoh", height=60)

        submitted = st.form_submit_button("💾 Saqlash", type="primary", use_container_width=True)

    if submitted:
        if not ariza_id or not tadbirkor:
            st.error("Ariza raqami va tadbirkor ismini kiriting!")
        else:
            apps = load_data()
            # Mavjud ariza raqamini yangilash
            existing = next((a for a in apps if a["ariza_id"] == ariza_id), None)

            entry = {
                "ariza_id":     ariza_id,
                "tadbirkor":    tadbirkor,
                "loyiha_tur":   loyiha_tur,
                "manzil":       manzil,
                "qavatlar":     qavatlar,
                "status":       status,
                "rad_sabablar": rad_sabablar,
                "izoh":         izoh,
                "sana":         datetime.now().strftime("%Y-%m-%d %H:%M"),
                "criteria_score": existing.get("criteria_score") if existing else None,
                "doc_similarity": existing.get("doc_similarity") if existing else None,
                "reviews":        existing.get("reviews", []) if existing else [],
                "risk_flags":     [],
            }

            if existing:
                apps = [entry if a["ariza_id"] == ariza_id else a for a in apps]
                st.success(f"✅ Ariza **{ariza_id}** yangilandi!")
            else:
                apps.append(entry)
                st.success(f"✅ Ariza **{ariza_id}** saqlandi!")
            save_data(apps)

    # Ro'yxat
    st.divider()
    st.subheader("📂 Barcha arizalar")
    apps = load_data()
    if not apps:
        st.info("Hali ariza kiritilmagan.")
    else:
        for a in reversed(apps):
            flags = a.get("risk_flags", [])
            color = "🔴" if flags else "🟢"
            with st.expander(f"{color} [{a['ariza_id']}] {a['tadbirkor']} — {a['status']}"):
                col1, col2, col3 = st.columns(3)
                col1.write(f"**Manzil:** {a['manzil']}")
                col2.write(f"**Tur:** {a['loyiha_tur']}")
                col3.write(f"**Sana:** {a['sana']}")
                if a.get("rad_sabablar"):
                    st.warning(f"**Rad sabablari:** {a['rad_sabablar']}")
                if flags:
                    for f in flags:
                        st.error(f"⚠️ {f}")

# ──────────────────────────────────────────────
#  PAGE 2: HUJJAT TAQQOSLASH
# ──────────────────────────────────────────────
elif page == "📄 Hujjat taqqoslash":
    st.header("📄 Rad etilgan vs Tasdiqlangan hujjat taqqoslash")
    st.markdown(
        "Bir xil yoki deyarli bir xil hujjat avval **rad** etilgan, keyin **tasdiq**langan bo'lsa — "
        "bu korrupsion alomat. AI semantik o'xshashlikni aniqlaydi."
    )

    apps = load_data()
    if not apps:
        st.warning("Avval ariza kiriting.")
        st.stop()

    ariza_ids = [a["ariza_id"] for a in apps]
    sel = st.selectbox("Ariza tanlang:", ariza_ids)
    app_data = next(a for a in apps if a["ariza_id"] == sel)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Rad etilgan holat hujjati")
        rad_text = st.text_area(
            "Rad etilgan arizadagi loyiha tavsifi / texnik ma'lumotlar:",
            value=app_data.get("rad_sabablar", ""),
            height=200,
            key="rad_doc",
        )
    with col2:
        st.subheader("🟢 Tasdiqlangan holat hujjati")
        tasd_text = st.text_area(
            "Tasdiqlangan arizadagi loyiha tavsifi / texnik ma'lumotlar:",
            height=200,
            key="tasd_doc",
            placeholder="Qayta topshirilgan va tasdiqlangan hujjat matnini kiriting...",
        )

    if st.button("🔍 AI taqqoslash", type="primary", use_container_width=True):
        if not rad_text.strip() or not tasd_text.strip():
            st.error("Ikkala maydonni ham to'ldiring!")
        else:
            with st.spinner("AI tahlil qilyapti... (HuggingFace modeli ishlamoqda)"):
                result = compare_docs(rad_text, tasd_text)

            sim_pct = result["similarity"] * 100

            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.metric("O'xshashlik darajasi", f"{sim_pct:.1f}%")
            c2.metric("Tahlil usuli", result["method"])
            c3.metric("Chegara (threshold)", "92%")

            st.progress(min(result["similarity"], 1.0))

            if result["is_risk"]:
                st.markdown(f"""
                <div class="risk-red">
                <strong>🚨 KORRUPSION XAVF ANIQLANDI!</strong><br>
                Rad etilgan va tasdiqlangan hujjatlar <b>{sim_pct:.1f}%</b> darajada o'xshash.<br>
                Hujjatlarda <b>hech qanday tuzatish kiritilmagan</b> holda ariza qayta tasdiqlanganga o'xshaydi.
                Bu pora berish orqali hal qilingan bo'lishi mumkin.
                </div>
                """, unsafe_allow_html=True)

                # Flagni saqlash
                apps = load_data()
                for a in apps:
                    if a["ariza_id"] == sel:
                        flag = f"Hujjat taqqoslash: {sim_pct:.1f}% o'xshashlik (chegara: 92%)"
                        if flag not in a.get("risk_flags", []):
                            a.setdefault("risk_flags", []).append(flag)
                        a["doc_similarity"] = sim_pct
                save_data(apps)
            else:
                st.markdown(f"""
                <div class="risk-green">
                <strong>✅ Xavf aniqlanmadi</strong><br>
                Hujjatlar <b>{sim_pct:.1f}%</b> darajada o'xshash — farqlar mavjud.
                Tuzatishlar kiritilgan deb hisoblanadi.
                </div>
                """, unsafe_allow_html=True)

            # Vizual farq
            with st.expander("🔬 Batafsil tahlil"):
                words_r = set(rad_text.lower().split())
                words_t = set(tasd_text.lower().split())
                only_rad  = words_r - words_t
                only_tasd = words_t - words_r
                common    = words_r & words_t

                col1, col2, col3 = st.columns(3)
                col1.metric("Umumiy so'zlar", len(common))
                col2.metric("Faqat rad etilganda", len(only_rad))
                col3.metric("Faqat tasdiqlanganda", len(only_tasd))

                if only_rad:
                    st.write("**Faqat rad etilgan hujjatda:** ", ", ".join(list(only_rad)[:20]))
                if only_tasd:
                    st.write("**Faqat tasdiqlangan hujjatda:** ", ", ".join(list(only_tasd)[:20]))

# ──────────────────────────────────────────────
#  PAGE 3: 20 MEZON BAHOLASH
# ──────────────────────────────────────────────
elif page == "✅ 20 Mezon baholash":
    st.header("✅ 20 Mezon bo'yicha loyiha baholash")
    st.markdown(
        "Har bir mezon bo'yicha loyiha hujjatlariga asoslanib ball bering. "
        "Keyin AI umumiy xavf darajasini aniqlaydi."
    )

    apps = load_data()
    if not apps:
        st.warning("Avval ariza kiriting.")
        st.stop()

    sel = st.selectbox("Ariza tanlang:", [a["ariza_id"] for a in apps])
    app_data = next(a for a in apps if a["ariza_id"] == sel)

    total_score  = 0
    scores_by_dept = {}
    all_criteria_results = {}

    for dept, criteria_list in CRITERIA.items():
        st.subheader(dept)
        dept_score = 0
        dept_max   = sum(c["w"] for c in criteria_list)

        cols = st.columns([3, 1, 1])
        cols[0].markdown("**Mezon**")
        cols[1].markdown("**Og'irlik**")
        cols[2].markdown("**Ball (0–5)**")

        for c in criteria_list:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.markdown(f"**{c['id']}. {c['name']}**")
            col1.caption(c["desc"])
            col2.markdown(f"`{c['w']}x`")
            ball = col3.selectbox(
                f"mezon_{c['id']}",
                options=[0, 1, 2, 3, 4, 5],
                index=3,
                label_visibility="collapsed",
                key=f"score_{c['id']}",
            )
            weighted = ball * c["w"] / 5  # 0 dan c["w"] gacha
            dept_score  += weighted
            all_criteria_results[c["id"]] = {"name": c["name"], "ball": ball, "weighted": weighted}

        dept_pct = dept_score / dept_max * 100
        scores_by_dept[dept] = {"score": dept_score, "max": dept_max, "pct": dept_pct}
        total_score += dept_score

        # Bo'lim natijalari
        dcol1, dcol2 = st.columns([4, 1])
        dcol1.progress(dept_pct / 100, text=f"{dept_pct:.0f}%")
        dcol2.metric("Bo'lim", f"{dept_score:.1f}/{dept_max}")
        st.divider()

    # UMUMIY NATIJA
    total_pct  = total_score / MAX_SCORE * 100
    risk       = score_to_risk(total_score)
    approved   = "Tasdiqlandi" in app_data.get("status", "")

    st.subheader("📊 Umumiy natija")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Umumiy ball",   f"{total_score:.1f}/{MAX_SCORE}")
    c2.metric("Foiz",          f"{total_pct:.1f}%")
    c3.metric("Xavf darajasi", risk["label"])
    c4.metric("Ariza holati",  "✅ Tasdiqlangan" if approved else "🔄 Ko'rib chiqilmoqda")

    st.progress(total_pct / 100)

    # Xavf tahlili: past ball + tasdiqlangan = qo'shimcha xavf
    if approved and total_pct < 60:
        alert_msg = (
            f"🚨 **JIDDIY XAVF:** Loyiha 20 mezon bo'yicha **{total_pct:.0f}%** ball oldi, "
            f"lekin ariza **tasdiqlangan**. Bu normaga zid — "
            f"tekshiruv talab etiladi!"
        )
        st.markdown(f'<div class="risk-red">{alert_msg}</div>', unsafe_allow_html=True)

        apps = load_data()
        for a in apps:
            if a["ariza_id"] == sel:
                flag = f"Mezon baholash: {total_pct:.0f}% ball — tasdiq bilan nomuvofiq"
                if flag not in a.get("risk_flags", []):
                    a.setdefault("risk_flags", []).append(flag)
                a["criteria_score"] = total_pct
        save_data(apps)

    elif approved and total_pct < 80:
        st.markdown(f'<div class="risk-yellow">⚠️ Loyiha <b>{total_pct:.0f}%</b> ball oldi — tasdiq bilan chegaraviy holat</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="risk-green">✅ Natija va ariza holati muvofiqlashadi</div>', unsafe_allow_html=True)

    if st.button("💾 Natijalarni saqlash", type="primary"):
        apps = load_data()
        for a in apps:
            if a["ariza_id"] == sel:
                a["criteria_score"]   = total_pct
                a["criteria_details"] = all_criteria_results
        save_data(apps)
        st.success("Saqlandi!")

# ──────────────────────────────────────────────
#  PAGE 4: FOYDALANUVCHI FIKRLARI
# ──────────────────────────────────────────────
elif page == "⭐ Foydalanuvchi fikrlari":
    st.header("⭐ Foydalanuvchi fikrlari (qurilish tugagach)")
    st.markdown(
        "Xonadonlarni qabul qilgan rezidentlar 1–5 ball bilan baholaydi. "
        "Rasmiy xulosa bilan katta farq bo'lsa → korrupsion alomat."
    )

    apps = load_data()
    approved_apps = [a for a in apps if "Tasdiqlandi" in a.get("status", "")]

    if not approved_apps:
        st.info("Foydalanishga topshirilgan (tasdiqlangan) arizalar yo'q.")
        st.stop()

    sel = st.selectbox("Obyekt tanlang:", [a["ariza_id"] for a in approved_apps])
    app_data = next(a for a in approved_apps if a["ariza_id"] == sel)

    # Yangi fikr qo'shish
    st.subheader("Yangi baho qo'shish")
    with st.form("review_form", clear_on_submit=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            review_text = st.text_area("Fikr / shikoyat:", height=80,
                                       placeholder="Qurilish sifati, muhandislik tizimlar, xavfsizlik...")
        with col2:
            rating = st.select_slider("Baho:", options=[1, 2, 3, 4, 5], value=3,
                                      format_func=lambda x: "⭐"*x)
            ism = st.text_input("Ism (ixtiyoriy):", placeholder="Anonimlik saqlanadi")

        sub = st.form_submit_button("📤 Yuborish", type="primary", use_container_width=True)

    if sub:
        apps = load_data()
        for a in apps:
            if a["ariza_id"] == sel:
                a.setdefault("reviews", []).append({
                    "rating": rating,
                    "text":   review_text,
                    "ism":    ism or "Anonim",
                    "sana":   datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
        save_data(apps)
        app_data = next(a for a in apps if a["ariza_id"] == sel)
        st.success("Fikr qo'shildi!")

    # Mavjud fikrlar
    reviews = app_data.get("reviews", [])

    if reviews:
        avg_rating = np.mean([r["rating"] for r in reviews])

        c1, c2, c3 = st.columns(3)
        c1.metric("O'rtacha baho",    f"{avg_rating:.1f} / 5.0")
        c2.metric("Jami fikrlar",     len(reviews))
        c3.metric("Rasmiy holat",     "✅ Tasdiqlangan")

        # Rasmiy vs foydalanuvchi tahlili
        verdict = review_vs_official(avg_rating, official_approved=True)

        if verdict["risk"]:
            st.markdown(f'<div class="risk-red"><strong>{verdict["label"]}</strong><br>'
                        f'O\'rtacha foydalanuvchi bahosi: <b>{avg_rating:.1f}</b> — '
                        f'bu "qoniqarsiz" darajasi. Rasmiy tashkilotlar esa yaxshi qurish xulosasini bergan. '
                        f'Xavf signali qayd etildi.</div>', unsafe_allow_html=True)

            apps = load_data()
            for a in apps:
                if a["ariza_id"] == sel:
                    flag = f"Foydalanuvchi bahosi: {avg_rating:.1f}/5 — rasmiy xulosaga zid"
                    if flag not in a.get("risk_flags", []):
                        a.setdefault("risk_flags", []).append(flag)
            save_data(apps)
        else:
            st.markdown(f'<div class="risk-green">{verdict["label"]}</div>', unsafe_allow_html=True)

        # Rating taqsimoti
        import collections
        dist = collections.Counter(r["rating"] for r in reviews)
        st.subheader("Baho taqsimoti")
        for i in range(5, 0, -1):
            cnt = dist.get(i, 0)
            bar_pct = cnt / len(reviews) if reviews else 0
            cols = st.columns([1, 5, 1])
            cols[0].write("⭐" * i)
            cols[1].progress(bar_pct)
            cols[2].write(cnt)

        # Fikrlar ro'yxati
        st.subheader("Oxirgi fikrlar")
        for r in reversed(reviews[-10:]):
            stars = "⭐" * r["rating"]
            with st.expander(f"{stars}  {r['ism']} — {r['sana']}"):
                st.write(r.get("text", "Matn kiritilmagan"))
    else:
        st.info("Hali fikr yo'q. Birinchi bo'lib yozing!")

# ──────────────────────────────────────────────
#  PAGE 5: DASHBOARD
# ──────────────────────────────────────────────
elif page == "📊 Dashboard":
    st.header("📊 Korrupsiya xavfi umumiy Dashboard")

    apps = load_data()
    if not apps:
        st.info("Hali ma'lumot yo'q.")
        st.stop()

    total       = len(apps)
    red_apps    = [a for a in apps if a.get("risk_flags")]
    approved    = [a for a in apps if "Tasdiqlandi" in a.get("status", "")]
    rejected    = [a for a in apps if "Rad etildi" in a.get("status", "")]
    doc_risks   = [a for a in apps if a.get("doc_similarity", 0) >= 92]
    score_risks = [a for a in apps if (a.get("criteria_score") or 100) < 60
                   and "Tasdiqlandi" in a.get("status", "")]
    review_risks= [a for a in apps if any("Foydalanuvchi" in f for f in a.get("risk_flags", []))]

    # KPI
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📋 Jami arizalar",    total)
    col2.metric("🔴 Xavfli arizalar",  len(red_apps))
    col3.metric("✅ Tasdiqlangan",      len(approved))
    col4.metric("🚫 Rad etilgan",       len(rejected))
    col5.metric("⚠️ Xavf ulushi",
                f"{len(red_apps)/total*100:.0f}%" if total else "0%")

    st.divider()

    # Xavf turlari
    st.subheader("🔍 Xavf turlari bo'yicha statistika")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
        <div class="dept-header">📄 Hujjat o'xshashligi</div>
        <div style="font-size:36px;font-weight:700;color:#dc2626">{len(doc_risks)}</div>
        <div style="color:#64748b">ariza (≥92% o'xshash)</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-box">
        <div class="dept-header">✅ Mezon vs Tasdiq</div>
        <div style="font-size:36px;font-weight:700;color:#dc2626">{len(score_risks)}</div>
        <div style="color:#64748b">ariza (&lt;60% ball, tasdiqda)</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-box">
        <div class="dept-header">⭐ Foydalanuvchi vs Rasmiy</div>
        <div style="font-size:36px;font-weight:700;color:#dc2626">{len(review_risks)}</div>
        <div style="color:#64748b">ariza (past baho, tasdiqda)</div>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # Xavfli arizalar ro'yxati
    st.subheader("🚨 Xavfli arizalar ro'yxati")
    if not red_apps:
        st.success("Hozircha xavfli ariza aniqlanmagan.")
    else:
        for a in red_apps:
            flags = a.get("risk_flags", [])
            with st.expander(f"🔴 [{a['ariza_id']}] {a['tadbirkor']} | {a['loyiha_tur']}"):
                col1, col2 = st.columns(2)
                col1.write(f"**Manzil:** {a['manzil']}")
                col2.write(f"**Holat:** {a['status']}")
                st.write("**Aniqlangan xavf belgilari:**")
                for f in flags:
                    st.error(f"⚠️ {f}")
                if a.get("doc_similarity"):
                    st.write(f"📄 Hujjat o'xshashligi: **{a['doc_similarity']:.1f}%**")
                if a.get("criteria_score") is not None:
                    st.write(f"✅ Mezon bali: **{a['criteria_score']:.0f}%**")
                reviews = a.get("reviews", [])
                if reviews:
                    avg = np.mean([r["rating"] for r in reviews])
                    st.write(f"⭐ O'rtacha baho: **{avg:.1f}/5**")

    # CSV eksport
    st.divider()
    if st.button("📥 Xavfli arizalarni CSV yuklab olish"):
        import io, csv
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["ariza_id", "tadbirkor", "manzil", "holat", "xavf_belgilari",
                    "hujjat_oxshashligi", "mezon_bali"])
        for a in red_apps:
            w.writerow([
                a["ariza_id"], a["tadbirkor"], a["manzil"], a["status"],
                "; ".join(a.get("risk_flags", [])),
                a.get("doc_similarity", ""), a.get("criteria_score", ""),
            ])
        st.download_button(
            "⬇️ CSV yuklab olish",
            data=buf.getvalue().encode("utf-8-sig"),
            file_name=f"risk_arizalar_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
