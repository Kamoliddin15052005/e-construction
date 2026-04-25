"""
E-Construction — Korrupsiyaga qarshi AI tizimi
Asosiy vazifa: AI orqali korrupsion alomatlarni aniqlash va sabab keltirish
"""

import streamlit as st
import json, os, requests, numpy as np, time
from datetime import datetime
from pathlib import Path

# ════════════════════════════════════════════════════════════
#  CONFIG
# ════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="E-Construction AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.card-red    {background:#fff1f2;border-left:5px solid #dc2626;padding:14px 18px;border-radius:8px;margin:8px 0}
.card-yellow {background:#fefce8;border-left:5px solid #d97706;padding:14px 18px;border-radius:8px;margin:8px 0}
.card-green  {background:#f0fdf4;border-left:5px solid #16a34a;padding:14px 18px;border-radius:8px;margin:8px 0}
.card-blue   {background:#eff6ff;border-left:5px solid #2563eb;padding:14px 18px;border-radius:8px;margin:8px 0}
.kpi {background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:18px 12px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.kpi-val {font-size:38px;font-weight:800;line-height:1.1}
.kpi-lab {font-size:12px;color:#64748b;margin-top:4px}
.step {display:inline-block;background:#1e3a5f;color:#fff;border-radius:50%;width:28px;height:28px;text-align:center;line-height:28px;font-weight:700;font-size:14px;margin-right:8px}
.verdict-box {border-radius:12px;padding:20px 24px;margin:12px 0;font-size:15px;line-height:1.7}
.verdict-red    {background:#fef2f2;border:2px solid #dc2626}
.verdict-yellow {background:#fffbeb;border:2px solid #f59e0b}
.verdict-green  {background:#f0fdf4;border:2px solid #16a34a}
h2,h3 {color:#1e3a5f}
.stProgress>div>div {border-radius:4px}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  DATA STORE
# ════════════════════════════════════════════════════════════
DATA_FILE = Path("data/apps.json")
DATA_FILE.parent.mkdir(exist_ok=True)

SAMPLE_DATA = [
    {
        "id": "QB-2024-001",
        "loyiha": "Navruz-Servis 16-qavatli turar-joy majmuasi",
        "tadbirkor": 'MChJ "Navruz-Servis Qurilish"',
        "manzil": "Toshkent, Yunusobod t., Navruz ko'ch. 12",
        "tur": "Ko'p qavatli turar-joy (≥5 qavat)",
        "qavatlar": 16,
        "bosqich": "qurilish",
        "sana": "2024-03-15",
        "holat": "rad_keyin_tasdiq",
        "mezon_ballari": {
            "san1":4,"san2":4,"san3":3,"san4":4,"san5":3,
            "yong1":2,"yong2":2,"yong3":3,"yong4":2,"yong5":3,
            "eko1":3,"eko2":4,"eko3":2,"eko4":3,"eko5":3,
            "qur1":3,"qur2":4,"qur3":3,"qur4":3,"qur5":3
        },
        "organlar": [
            {
                "nom": "Sanitariya-Epidemiologiya Inspeksiyasi",
                "qaror_1": "rad",
                "sabab_1": "Sanitariya himoya zona masofasi talabga mos emas (15m, norma 25m). Loyihada suv oqova tizimi sxemasi to'liq ko'rsatilmagan. Chiqindi saqlash kamerasi loyihaga kiritilmagan.",
                "qaror_2": "tasdiq",
                "sabab_2": "Sanitariya himoya zona masofasi talabga mos. Suv oqova tizimi loyihada ko'rsatilgan."
            },
            {
                "nom": "Yong'in Xavfsizligi Inspeksiyasi",
                "qaror_1": "rad",
                "sabab_1": "Yong'in o'chirish tizimi (sprinkler) loyihada yo'q. Evakuatsiya zinasi kengligi 0.9m — normadan past (1.2m talab). 9-15 qavatlar uchun avtomatik signal tizimi ko'rsatilmagan.",
                "qaror_2": "tasdiq",
                "sabab_2": "Yong'in o'chirish tizimi loyihaga qo'shildi. Evakuatsiya zinasi 1.2m ga kengaytirildi."
            },
            {
                "nom": "Ekologiya Inspeksiyasi",
                "qaror_1": "tasdiq",
                "sabab_1": "",
                "qaror_2": "tasdiq",
                "sabab_2": ""
            },
            {
                "nom": "Qurilish Bosh Inspeksiyasi",
                "qaror_1": "rad",
                "sabab_1": "Mustahkamlik ekspertizasi xulosasi yo'q. Seysmik bardoshlilik hisob-kitoblari loyihada to'liq emas.",
                "qaror_2": "tasdiq",
                "sabab_2": "Mustahkamlik xulosasi taqdim etildi. Seysmik hisob-kitoblar to'ldirildi."
            }
        ],
        "rad_hujjat": "16-qavatli turar-joy binosi loyihasi. Umumiy yer maydoni 0.42 ga. 128 ta xonadon. Poydevor: plitali temir-beton. Tashqi devor: g'isht va penoplex izolyatsiya. Liftlar: 2 dona. Zina: 2 dona kenglik 0.9 metr. Yong'in o'chirish tizimi loyihada ko'rsatilmagan. Sanitariya zona masofasi 15 metr. Suv oqova tizimi loyihaga kiritilmagan. Seysmik zona 8 ball, hisob-kitoblar to'liq emas. Mustahkamlik xulosasi taqdim etilmagan.",
        "tasdiq_hujjat": "16-qavatli turar-joy binosi loyihasi. Umumiy yer maydoni 0.42 ga. 128 ta xonadon. Poydevor: plitali temir-beton. Tashqi devor: g'isht va penoplex izolyatsiya. Liftlar: 2 dona. Zina: 2 dona kenglik 0.9 metr. Yong'in o'chirish tizimi loyihada ko'rsatilmagan. Sanitariya zona masofasi 15 metr. Suv oqova tizimi loyihaga kiritilmagan. Seysmik zona 8 ball, hisob-kitoblar to'liq emas. Mustahkamlik xulosasi taqdim etilmagan.",
        "reviews": [
            {"ism":"Aziz N.","baho":2,"fikr":"Liftlar ishlamayapti, zina juda tor. Qurilish sifati yomon","sana":"2024-09-10"},
            {"ism":"Malika R.","baho":1,"fikr":"Yong'in sensori yo'q umuman! Xavfli bino. Shikoyat qilaman","sana":"2024-09-15"},
            {"ism":"Jahongir T.","baho":2,"fikr":"Derazalar sifatsiz. Issiqlik yo'qoladi. Va'da qilingan narsalar yo'q","sana":"2024-09-20"},
            {"ism":"Nodira K.","baho":1,"fikr":"Kanalizatsiya muammosi bor. Hid keladi. Inspeksiya qilish kerak!","sana":"2024-10-01"},
            {"ism":"Sardor M.","baho":2,"fikr":"Suv bosimi past. Yuqori qavatlar azob chekmoqda","sana":"2024-10-05"}
        ],
        "ai_tahlil": None,
        "_doc_sim": None
    },
    {
        "id": "QB-2024-002",
        "loyiha": "Chilonzor Biznes-Markaz 9-qavatli ofis binosi",
        "tadbirkor": 'AJ "CityBuild Invest"',
        "manzil": "Toshkent, Chilonzor t., Bunyodkor sh.yo'li 45",
        "tur": "Tijorat binosi",
        "qavatlar": 9,
        "bosqich": "foydalanish",
        "sana": "2024-05-20",
        "holat": "tasdiq",
        "mezon_ballari": {
            "san1":5,"san2":5,"san3":4,"san4":5,"san5":4,
            "yong1":5,"yong2":5,"yong3":5,"yong4":5,"yong5":4,
            "eko1":4,"eko2":4,"eko3":4,"eko4":4,"eko5":4,
            "qur1":5,"qur2":5,"qur3":4,"qur4":5,"qur5":5
        },
        "organlar": [
            {"nom":"Sanitariya-Epidemiologiya","qaror_1":"tasdiq","sabab_1":"","qaror_2":"tasdiq","sabab_2":""},
            {"nom":"Yong'in Xavfsizligi","qaror_1":"tasdiq","sabab_1":"","qaror_2":"tasdiq","sabab_2":""},
            {"nom":"Ekologiya","qaror_1":"tasdiq","sabab_1":"","qaror_2":"tasdiq","sabab_2":""},
            {"nom":"Qurilish Inspeksiyasi","qaror_1":"tasdiq","sabab_1":"","qaror_2":"tasdiq","sabab_2":""}
        ],
        "rad_hujjat": "",
        "tasdiq_hujjat": "9-qavatli ofis binosi loyihasi. Maydon 0.18 ga. Poydevor: monolitik. Yong'in: sprinkler va signal va gidrant to'liq. Evakuatsiya: 3 ta zina kenglik 1.4 metr. Seysmik hisob-kitob 8 ball, REI-90. Ko'kalamzor 22 foiz. Mustahkamlik xulosasi mavjud. Material sertifikatlari taqdim etilgan.",
        "reviews": [
            {"ism":"Bekzod O.","baho":5,"fikr":"Ajoyib bino. Barcha talablar bajarilgan","sana":"2024-11-01"},
            {"ism":"Dilnoza A.","baho":4,"fikr":"Yaxshi, faqat parking kichikroq","sana":"2024-11-10"},
            {"ism":"Farrux H.","baho":5,"fikr":"Hammasi zo'r. Sifatli qurilish","sana":"2024-11-15"}
        ],
        "ai_tahlil": None,
        "_doc_sim": None
    },
    {
        "id": "QB-2024-003",
        "loyiha": "Elite-Home 12-qavatli Mirzo-Ulug'bek turar-joy",
        "tadbirkor": 'MChJ "Premium Construction"',
        "manzil": "Toshkent, Mirzo-Ulug'bek t., Qoratosh ko'ch. 8",
        "tur": "Ko'p qavatli turar-joy (≥5 qavat)",
        "qavatlar": 12,
        "bosqich": "foydalanish",
        "sana": "2024-07-10",
        "holat": "rad_keyin_tasdiq",
        "mezon_ballari": {
            "san1":3,"san2":3,"san3":2,"san4":3,"san5":2,
            "yong1":1,"yong2":2,"yong3":2,"yong4":1,"yong5":2,
            "eko1":3,"eko2":2,"eko3":2,"eko4":2,"eko5":2,
            "qur1":2,"qur2":3,"qur3":2,"qur4":3,"qur5":2
        },
        "organlar": [
            {
                "nom": "Sanitariya-Epidemiologiya",
                "qaror_1": "rad",
                "sabab_1": "Sanitariya zona 12m, norma 25m. Suv oqova tizimi sxemasi yo'q.",
                "qaror_2": "tasdiq",
                "sabab_2": "Sanitariya zona 12m. Suv oqova loyihaga qo'shildi."
            },
            {
                "nom": "Yong'in Xavfsizligi",
                "qaror_1": "rad",
                "sabab_1": "Sprinkler tizimi yo'q. Evakuatsiya zinasi 1 ta, kenglik 0.8m. Sensor yo'q.",
                "qaror_2": "tasdiq",
                "sabab_2": "Yong'in tizimi va evakuatsiya yo'llari loyihaga qo'shildi."
            },
            {
                "nom": "Ekologiya",
                "qaror_1": "rad",
                "sabab_1": "Ko'kalamzor 8%, norma 20%. Chiqindi utilizatsiya shartnomasi yo'q.",
                "qaror_2": "tasdiq",
                "sabab_2": "Ko'kalamzor va chiqindi masalalari hal etildi."
            },
            {
                "nom": "Qurilish Inspeksiyasi",
                "qaror_1": "rad",
                "sabab_1": "Mustahkamlik xulosasi yo'q. Seysmik hisob-kitob to'liq emas. Material sertifikatlari taqdim etilmagan.",
                "qaror_2": "tasdiq",
                "sabab_2": "Mustahkamlik xulosasi va seysmik hisob-kitob taqdim etildi."
            }
        ],
        "rad_hujjat": "12-qavatli turar-joy binosi loyihasi. 96 ta xonadon. Poydevor: plitali. Devor: g'isht. Zina: 1 dona kenglik 0.8 metr. Lift: 1 dona. Yong'in o'chirish tizimi loyihada ko'rsatilmagan. Sanitariya zona 12 metr. Ko'kalamzor 8 foiz. Seysmik hisob-kitob yo'q. Material sertifikat yo'q. Mustahkamlik xulosasi taqdim etilmagan.",
        "tasdiq_hujjat": "12-qavatli turar-joy binosi loyihasi. 96 ta xonadon. Poydevor: plitali. Devor: g'isht. Zina: 1 dona kenglik 0.8 metr. Lift: 1 dona. Yong'in o'chirish tizimi loyihada ko'rsatilmagan. Sanitariya zona 12 metr. Ko'kalamzor 8 foiz. Seysmik hisob-kitob yo'q. Material sertifikat yo'q. Mustahkamlik xulosasi taqdim etilmagan.",
        "reviews": [
            {"ism":"Ulmas V.","baho":1,"fikr":"Dahshat. Bino qurilayotganda ham muammo bor edi, endi aholini joylashtirmoqchi","sana":"2024-10-20"},
            {"ism":"Zulfiya M.","baho":1,"fikr":"Yong'in signali yo'q! Bolalarim bilan xavfli binoda yashamayman","sana":"2024-10-25"},
            {"ism":"Sherzod B.","baho":2,"fikr":"Sifat past. Derazalar va eshiklar arzon material","sana":"2024-11-01"}
        ],
        "ai_tahlil": None,
        "_doc_sim": None
    }
]


def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    save_data(SAMPLE_DATA)
    return SAMPLE_DATA


def save_data(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ════════════════════════════════════════════════════════════
#  20 MEZON
# ════════════════════════════════════════════════════════════
CRITERIA = [
    ("san1",  "🧪 Sanitariya", "Sanitariya himoya zona masofasi",       5),
    ("san2",  "🧪 Sanitariya", "Suv ta'minoti va kanalizatsiya sxemasi", 5),
    ("san3",  "🧪 Sanitariya", "Chiqindi saqlash va kamera tizimi",      4),
    ("san4",  "🧪 Sanitariya", "Shamollatish va havo almashinuvi",       4),
    ("san5",  "🧪 Sanitariya", "Shovqin/vibratsiya normalariga mos",     3),
    ("yong1", "🔥 Yong'in",    "Sprinkler/gidrant o'chirish tizimi",     5),
    ("yong2", "🔥 Yong'in",    "Evakuatsiya yo'llari va zina ≥1.2m",    5),
    ("yong3", "🔥 Yong'in",    "Yong'inga chidamli konstruksiya REI-90+",5),
    ("yong4", "🔥 Yong'in",    "Avtomatik yong'in signalizatsiyasi",     4),
    ("yong5", "🔥 Yong'in",    "Yong'in suv bosimi va zaxirasi",         3),
    ("eko1",  "🌿 Ekologiya",  "Qurilish changi va gaz nazorat plani",   4),
    ("eko2",  "🌿 Ekologiya",  "Tuproq va grunt suvi muhofazasi",         4),
    ("eko3",  "🌿 Ekologiya",  "Ko'kalamzorlashtirish norma ≥20%",       3),
    ("eko4",  "🌿 Ekologiya",  "Chiqindi utilizatsiya shartnomasi",       3),
    ("eko5",  "🌿 Ekologiya",  "OVOS xulosasi (suv havzasi yaqin)",      4),
    ("qur1",  "🏗️ Qurilish",   "Loyiha hujjatlariga to'liq muvofiqlik", 5),
    ("qur2",  "🏗️ Qurilish",   "Seysmik bardoshlilik 8-9 ball",         5),
    ("qur3",  "🏗️ Qurilish",   "Muhandislik kommunikatsiyalar loyihasi", 4),
    ("qur4",  "🏗️ Qurilish",   "Qurilish materiallari sifat sertifikati",4),
    ("qur5",  "🏗️ Qurilish",   "Mustaqil ekspert mustahkamlik xulosasi", 5),
]
MAX_SCORE = sum(c[3] for c in CRITERIA)  # 85


def calc_score(ballari: dict) -> float:
    total = sum((ballari.get(key, 0) / 5) * w for key, _, _, w in CRITERIA)
    return round(total / MAX_SCORE * 100, 1)


# ════════════════════════════════════════════════════════════
#  HUGGINGFACE
# ════════════════════════════════════════════════════════════
HF_TOKEN = ""
try:
    HF_TOKEN = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN", ""))
except Exception:
    HF_TOKEN = os.getenv("HF_TOKEN", "")

EMBED_URL = (
    "https://api-inference.huggingface.co/pipeline/feature-extraction/"
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
FLAN_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"


def hf_headers():
    h = {"Content-Type": "application/json"}
    if HF_TOKEN:
        h["Authorization"] = f"Bearer {HF_TOKEN}"
    return h


@st.cache_data(show_spinner=False, ttl=1800)
def embed(texts: list):
    for _ in range(3):
        try:
            r = requests.post(
                EMBED_URL, headers=hf_headers(),
                json={"inputs": texts, "options": {"wait_for_model": True}},
                timeout=45,
            )
            if r.status_code == 200:
                return np.array(r.json())
            if r.status_code == 503:
                time.sleep(8)
        except Exception:
            time.sleep(4)
    return None


def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


def jaccard(t1: str, t2: str) -> float:
    w1, w2 = set(t1.lower().split()), set(t2.lower().split())
    return len(w1 & w2) / (len(w1 | w2) + 1e-9)


def doc_similarity(t1: str, t2: str) -> dict:
    if not t1.strip() or not t2.strip():
        return {"sim": 0.0, "method": "—", "ok": False}
    vecs = embed([t1, t2])
    if vecs is not None:
        return {"sim": round(cosine(vecs[0], vecs[1]), 4), "method": "Semantic AI (MiniLM)", "ok": True}
    return {"sim": round(jaccard(t1, t2), 4), "method": "Jaccard (fallback)", "ok": False}


@st.cache_data(show_spinner=False, ttl=600)
def flan_analysis(loyiha, mezon_pct, organ_holat, doc_sim_pct, avg_review, reviews_count):
    prompt = (
        f"Analyze for corruption: Project='{loyiha}', "
        f"Technical compliance={mezon_pct:.0f}% (need 70%+), "
        f"Authority decision='{organ_holat}', "
        f"Document similarity rejected-vs-approved={doc_sim_pct:.0f}% (>92%=bribery), "
        f"Public rating={avg_review:.1f}/5 ({reviews_count} reviews, <2.5=fraud). "
        f"Give: corruption risk level (HIGH/MEDIUM/LOW), top 2 reasons, one recommendation. Max 100 words."
    )
    try:
        r = requests.post(
            FLAN_URL, headers=hf_headers(),
            json={"inputs": prompt, "parameters": {"max_new_tokens": 150, "temperature": 0.2},
                  "options": {"wait_for_model": True}},
            timeout=40,
        )
        if r.status_code == 200:
            out = r.json()
            return (out[0].get("generated_text", "") if isinstance(out, list) else str(out)).strip()
    except Exception:
        pass
    return ""


# ════════════════════════════════════════════════════════════
#  RULE-BASED VERDICT
# ════════════════════════════════════════════════════════════
def verdict(mezon_pct, doc_sim_pct, avg_rev, holat, rad_bor, reviews):
    flags = []
    score = 0
    approved = holat in ("tasdiq", "rad_keyin_tasdiq")

    # Flag 1: Hujjat o'xshashligi
    if rad_bor and doc_sim_pct >= 92 and approved:
        flags.append({
            "icon": "📄",
            "sarlavha": f"Hujjat o'xshashligi {doc_sim_pct:.0f}% — chegara (92%) oshib ketdi",
            "tavsif": (
                f"Rad etilgan va tasdiqlangan hujjatlar semantik jihatdan deyarli bir xil ({doc_sim_pct:.0f}%). "
                f"Bu shuni ko'rsatadiki, hujjatga hech qanday tuzatish kiritilmagan holda qayta tasdiq berilgan. "
                f"Vakolatli organlar rad etgan kamchiliklar bartaraf etilmagan bo'lishi mumkin."
            ),
            "tavsiya": "Hujjat o'zgarishlari ro'yxatini (diff) talab qiling. Rad sabablari va yangi hujjatni parallel ekspertiza qiling.",
        })
        score += 40
    elif rad_bor and doc_sim_pct >= 78 and approved:
        flags.append({
            "icon": "📄",
            "sarlavha": f"Hujjat o'xshashligi {doc_sim_pct:.0f}% — shubhali daraja",
            "tavsif": f"Minimal o'zgarish aniqlandi. Rad etish sabablari to'liq bartaraf etilmagan bo'lishi mumkin.",
            "tavsiya": "Qo'shimcha ekspertiza buyurtma qiling.",
        })
        score += 20

    # Flag 2: Mezon bali
    if mezon_pct < 55 and approved:
        flags.append({
            "icon": "✅",
            "sarlavha": f"Texnik bali {mezon_pct:.0f}% — juda past, tasdiq berilgan",
            "tavsif": (
                f"20 mezon bo'yicha loyiha faqat {mezon_pct:.0f}% ball oldi (talab: 70%+). "
                f"Texnik talablarning katta qismi bajarilmagan holda vakolatli organlar ruxsatnoma bergan. "
                f"Bu normal adminstrativ jarayon doirasida mumkin emas."
            ),
            "tavsiya": "Ruxsatnoma berishda qaysi mezonlar e'tiborga olinmagonini so'rang. Texnik ekspertiza buyurtma qiling.",
        })
        score += 30
    elif mezon_pct < 68 and approved:
        flags.append({
            "icon": "✅",
            "sarlavha": f"Texnik bali {mezon_pct:.0f}% — me'yordan past ({mezon_pct:.0f}% < 70%)",
            "tavsif": "Texnik talablar to'liq bajarilmagan, lekin tasdiq berilgan.",
            "tavsiya": "Qo'shimcha texnik tekshiruv o'tkazing.",
        })
        score += 15

    # Flag 3: Aholi bahosi
    if reviews and avg_rev <= 2.0 and approved:
        flags.append({
            "icon": "⭐",
            "sarlavha": f"Aholi bahosi {avg_rev:.1f}/5 — kritik past, rasmiy tasdiqqa zid",
            "tavsif": (
                f"{len(reviews)} ta rezident o'rtacha {avg_rev:.1f} ball berdi — bu 'qoniqarsiz' darajasi. "
                f"Rasmiy inspeksiyalar qurilish sifatini yaxshi deb topgan, lekin aholining kundalik kuzatuvlari "
                f"buning aksini ko'rsatmoqda. Bu qurilish sifati bo'yicha hujjatlar soxtalashtirilib, "
                f"inspeksiya to'liq o'tkazilmagan bo'lishi mumkin."
            ),
            "tavsiya": "Qurilish va foydalanishga topshirish aktlarini qayta ko'rib chiqing. Aholi shikoyatlarini rasman qayd eting.",
        })
        score += 28
    elif reviews and avg_rev <= 2.8 and approved:
        flags.append({
            "icon": "⭐",
            "sarlavha": f"Aholi bahosi {avg_rev:.1f}/5 — rasmiy xulosadan past",
            "tavsif": "Aholining qurilish sifatiga bahosi o'rtacha darajadan past. Tekshiruv tavsiya etiladi.",
            "tavsiya": "Yangi texnik inspeksiya o'tkazing.",
        })
        score += 12

    if score >= 50:
        level = "🔴 YUQORI XAVF"
        cls   = "verdict-red"
        umumiy = (
            "Bir nechta jiddiy korrupsion alomat aniqlandi. "
            "Prokuratura va ichki nazorat organlariga darhol xabar berilishi tavsiya etiladi. "
            "Loyiha hujjatlari va moliyaviy to'lovlar bo'yicha mustaqil audit zarur. "
            "Ariza tizimda 🔴 XAVF guruhiga kiritildi."
        )
    elif score >= 20:
        level = "🟡 O'RTA XAVF"
        cls   = "verdict-yellow"
        umumiy = (
            "Ba'zi shubhali ko'rsatkichlar aniqlandi. "
            "30 kun ichida qo'shimcha texnik ekspertiza o'tkazilishi va hujjatlar qayta ko'rib chiqilishi tavsiya etiladi. "
            "Monitoring kuchaytirilib, ariza kuzatuv ro'yxatiga kiritildi."
        )
    else:
        level = "🟢 PAST XAVF"
        cls   = "verdict-green"
        umumiy = (
            "Ko'rsatkichlar o'zaro muvofiq. Hujjatlar, texnik ballari va aholi baholari moslikda. "
            "Oddiy monitoring tartibida davom ettirilsin."
        )

    return {"level": level, "cls": cls, "flags": flags, "score": score, "umumiy": umumiy}


# ════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🏗️ E-Construction")
    st.caption("Korrupsiyaga qarshi AI tizimi")
    st.divider()

    page = st.radio("", [
        "🏠 Bosh sahifa",
        "🔍 AI Tahlil",
        "📋 Arizalar ro'yxati",
        "➕ Yangi ariza",
        "📊 Statistika",
    ], label_visibility="collapsed")

    st.divider()
    st.caption("**HuggingFace holati:**")
    if HF_TOKEN:
        st.success("✅ Token ulangan — Semantic AI faol")
    else:
        st.warning("⚠️ Token yo'q — Jaccard fallback")
        with st.expander("🔑 Token qanday ulash?"):
            st.markdown("""
**1.** [huggingface.co](https://huggingface.co) — ro'yxat

**2.** `Profile → Settings → Access Tokens`

**3.** `New token` → Role: `Read` → Generate

**4.** `.streamlit/secrets.toml` yarating:
```toml
HF_TOKEN = "hf_siz_token"
```

**Natija:** Jaccard o'rniga semantic AI tahlil ishlaydi — aniqlik 3-4x oshadi.
            """)
    st.caption("**Model:** `paraphrase-multilingual-MiniLM-L12-v2`")


# ════════════════════════════════════════════════════════════
#  PAGE: BOSH SAHIFA
# ════════════════════════════════════════════════════════════
if page == "🏠 Bosh sahifa":
    st.title("🏗️ E-Construction — Korrupsiyaga qarshi AI")
    st.markdown("##### Qurilish ruxsatnomalari jarayonidagi korrupsion alomatlarni aniqlash tizimi")

    st.markdown("""
    <div class="card-blue">
    <b>🤖 AI 4 qadam orqali korrupsiyani aniqlaydi:</b><br><br>
    <span class="step">1</span><b>Mezon baholash</b> — 20 texnik mezon bo'yicha loyiha bali (sanitariya, yong'in, ekologiya, qurilish)<br>
    <span class="step">2</span><b>Organ qarorlari</b> — rad etilgan va tasdiqlangan hujjatlar AI tomonidan semantik taqqoslanadi<br>
    <span class="step">3</span><b>Jamoat nazorati</b> — rezidentlar 1–5 yulduz bilan baholaydi va fikr yozadi<br>
    <span class="step">4</span><b>AI xulosasi</b> — barcha ma'lumot birlashtiriladi, korrupsiya xavfi va sabablari keltiriladi
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    apps = load_data()

    all_v = []
    for a in apps:
        pct = calc_score(a.get("mezon_ballari", {}))
        rad_bor = a["holat"] == "rad_keyin_tasdiq"
        w1 = set(a.get("rad_hujjat", "").lower().split())
        w2 = set(a.get("tasdiq_hujjat", "").lower().split())
        dsim = len(w1 & w2) / (len(w1 | w2) + 1e-9) * 100 if (w1 and w2) else 0
        revs = a.get("reviews", [])
        avg = np.mean([r["baho"] for r in revs]) if revs else 0
        v = verdict(pct, dsim, avg, a["holat"], rad_bor, revs)
        all_v.append(v["score"])

    red_cnt = sum(1 for s in all_v if s >= 50)
    yel_cnt = sum(1 for s in all_v if 20 <= s < 50)

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f'<div class="kpi"><div class="kpi-val">{len(apps)}</div><div class="kpi-lab">Jami arizalar</div></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="kpi"><div class="kpi-val" style="color:#dc2626">{red_cnt}</div><div class="kpi-lab">🔴 Yuqori xavf</div></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="kpi"><div class="kpi-val" style="color:#d97706">{yel_cnt}</div><div class="kpi-lab">🟡 O\'rta xavf</div></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="kpi"><div class="kpi-val" style="color:#7c3aed">{len([a for a in apps if a["holat"]=="rad_keyin_tasdiq"])}</div><div class="kpi-lab">⚠️ Rad→Tasdiq</div></div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("⚡ Tezkor ko'rinish")

    for i, a in enumerate(apps):
        pct = calc_score(a.get("mezon_ballari", {}))
        rad_bor = a["holat"] == "rad_keyin_tasdiq"
        w1 = set(a.get("rad_hujjat", "").lower().split())
        w2 = set(a.get("tasdiq_hujjat", "").lower().split())
        dsim = len(w1 & w2) / (len(w1 | w2) + 1e-9) * 100 if (w1 and w2) else 0
        revs = a.get("reviews", [])
        avg = np.mean([r["baho"] for r in revs]) if revs else 0
        v = verdict(pct, dsim, avg, a["holat"], rad_bor, revs)
        icon = "🔴" if v["score"] >= 50 else ("🟡" if v["score"] >= 20 else "🟢")

        with st.expander(f"{icon} **{a['id']}** — {a['loyiha']}"):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Mezon bali",       f"{pct:.0f}%")
            c2.metric("Hujjat o'xshash.", f"{dsim:.0f}%" if rad_bor else "—")
            c3.metric("Aholi bahosi",     f"{avg:.1f}⭐" if revs else "—")
            c4.metric("Xavf",            v["level"])

            if v["flags"]:
                for fl in v["flags"]:
                    st.markdown(f'<div class="card-red"><b>{fl["icon"]} {fl["sarlavha"]}</b></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="card-green">✅ Aniqlanadigan korrupsion alomat yo\'q</div>', unsafe_allow_html=True)

            if st.button("🔍 To'liq AI tahlil →", key=f"h_{i}"):
                st.session_state["sel_id"] = a["id"]
                st.rerun()


# ════════════════════════════════════════════════════════════
#  PAGE: AI TAHLIL (ASOSIY)
# ════════════════════════════════════════════════════════════
elif page == "🔍 AI Tahlil":
    st.title("🔍 AI Korrupsiya Tahlili")
    apps = load_data()

    default_idx = 0
    if "sel_id" in st.session_state:
        ids = [a["id"] for a in apps]
        if st.session_state["sel_id"] in ids:
            default_idx = ids.index(st.session_state["sel_id"])

    sel_id = st.selectbox(
        "Ariza:",
        [a["id"] for a in apps],
        index=default_idx,
        format_func=lambda x: f"{x} — {next(a['loyiha'] for a in apps if a['id']==x)}",
    )
    app = next(a for a in apps if a["id"] == sel_id)

    # Info
    col1, col2, col3 = st.columns(3)
    hol_map = {"tasdiq": "✅ Tasdiqlandi", "rad_keyin_tasdiq": "⚠️ Rad → Keyin tasdiq", "rad": "🚫 Rad etildi"}
    col1.info(f"**{app['loyiha']}**\n\n📍 {app['manzil']}")
    col2.info(f"**Tur:** {app['tur']}\n\n**Qavatlar:** {app['qavatlar']}")
    col3.info(f"**Holat:** {hol_map.get(app['holat'], app['holat'])}\n\n**Sana:** {app['sana']}")

    st.markdown("---")

    # ════ QADAM 1 ════
    st.markdown('<span class="step">1</span> **20 Mezon bo\'yicha texnik muvofiqlik bali**', unsafe_allow_html=True)

    mezon_pct = calc_score(app.get("mezon_ballari", {}))
    cbar, cval = st.columns([4, 1])
    cbar.progress(mezon_pct / 100, text=f"Texnik muvofiqlik: **{mezon_pct:.0f}%**  (chegara: 70%)")
    cval.metric("", f"{mezon_pct:.0f}/100")

    # Bo'lim breakdown
    dept_data = {}
    for key, dept, name, w in CRITERIA:
        if dept not in dept_data:
            dept_data[dept] = {"s": 0, "m": 0, "low": []}
        ball = app.get("mezon_ballari", {}).get(key, 0)
        dept_data[dept]["s"] += (ball / 5) * w
        dept_data[dept]["m"] += w
        if ball <= 2:
            dept_data[dept]["low"].append(name)

    dcols = st.columns(4)
    for i, (dept, d) in enumerate(dept_data.items()):
        dp = d["s"] / d["m"] * 100
        clr = "#dc2626" if dp < 60 else ("#d97706" if dp < 75 else "#16a34a")
        low_html = f'<br><small style="color:#dc2626">⚠️ {", ".join(d["low"][:2])}</small>' if d["low"] else ""
        dcols[i].markdown(
            f'<div style="background:#f8fafc;border-radius:8px;padding:10px 12px;border-top:3px solid {clr}">'
            f'<b style="font-size:13px">{dept}</b><br>'
            f'<span style="font-size:26px;font-weight:800;color:{clr}">{dp:.0f}%</span>'
            f'{low_html}</div>', unsafe_allow_html=True,
        )

    with st.expander("📋 Barcha 20 mezon bali"):
        for dept_n in set(d for _, d, _, _ in CRITERIA):
            st.markdown(f"**{dept_n}**")
            for key, d, name, w in CRITERIA:
                if d != dept_n:
                    continue
                ball = app.get("mezon_ballari", {}).get(key, 0)
                clr = "#dc2626" if ball <= 2 else ("#d97706" if ball <= 3 else "#16a34a")
                stars = "●" * ball + "○" * (5 - ball)
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:10px;padding:4px 0">'
                    f'<span style="flex:1;font-size:13px">{name}</span>'
                    f'<span style="color:{clr};font-size:14px">{stars}</span>'
                    f'<span style="color:{clr};font-weight:700;width:30px;text-align:right">{ball}/5</span></div>',
                    unsafe_allow_html=True,
                )

    st.markdown("---")

    # ════ QADAM 2 ════
    st.markdown('<span class="step">2</span> **Vakolatli organlar qarorlari va hujjat taqqoslash**', unsafe_allow_html=True)

    rad_bor = app["holat"] == "rad_keyin_tasdiq"
    doc_sim_pct = 0.0
    doc_method = "—"

    for org in app.get("organlar", []):
        q1 = org["qaror_1"]
        q2 = org["qaror_2"]
        icon1 = "🔴 Rad" if q1 == "rad" else "✅ Tasdiq"
        icon2 = "🔴 Rad" if q2 == "rad" else "✅ Tasdiq"

        with st.expander(f"**{org['nom']}** │ 1-qaror: {icon1} → 2-qaror: {icon2}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**1-qaror: {icon1}**")
                if org.get("sabab_1"):
                    st.markdown(f'<div class="card-red">{org["sabab_1"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="card-green">Rad sababi yo\'q — tasdiq</div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f"**2-qaror: {icon2}**")
                if org.get("sabab_2") and q2 == "tasdiq" and q1 == "rad":
                    st.markdown(f'<div class="card-green">{org["sabab_2"]}</div>', unsafe_allow_html=True)
                elif q2 == "tasdiq":
                    st.markdown('<div class="card-green">To\'g\'ridan to\'g\'ri tasdiq</div>', unsafe_allow_html=True)

    if rad_bor and app.get("rad_hujjat") and app.get("tasdiq_hujjat"):
        st.markdown('<div class="card-yellow">📄 <b>Hujjat o\'xshashligini tekshirish:</b> Rad etilgan va tasdiqlangan hujjatlar qanchalik bir xil?</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.caption("🔴 Rad etilgan holat hujjati:")
            st.text_area("", value=app["rad_hujjat"], height=100, disabled=True, key="rad_show")
        with col2:
            st.caption("✅ Tasdiqlangan holat hujjati:")
            st.text_area("", value=app["tasdiq_hujjat"], height=100, disabled=True, key="tasd_show")

        if st.button("🤖 AI semantik taqqoslash", key="doc_btn", type="primary"):
            with st.spinner("MiniLM modeli hujjatlarni taqqoslamoqda..." if HF_TOKEN else "Jaccard usuli bilan taqqoslanmoqda..."):
                res = doc_similarity(app["rad_hujjat"], app["tasdiq_hujjat"])
            sim = res["sim"] * 100
            doc_sim_pct = sim
            doc_method = res["method"]
            thresh = 92
            clr_cls = "card-red" if sim >= thresh else ("card-yellow" if sim >= 78 else "card-green")
            msg = (
                f"🚨 <b>O'xshashlik {sim:.1f}%</b> — chegara ({thresh}%) dan YUQORI! "
                f"Hujjatlar deyarli bir xil. Tuzatish kiritilmagan."
                if sim >= thresh else
                f"⚠️ <b>O'xshashlik {sim:.1f}%</b> — shubhali daraja."
                if sim >= 78 else
                f"✅ <b>O'xshashlik {sim:.1f}%</b> — hujjatlar farqlanadi."
            )
            st.markdown(f'<div class="{clr_cls}">{msg}<br><small>Usul: {res["method"]}</small></div>', unsafe_allow_html=True)

            apps2 = load_data()
            for a2 in apps2:
                if a2["id"] == sel_id:
                    a2["_doc_sim"] = res["sim"]
            save_data(apps2)
            app["_doc_sim"] = res["sim"]

        if app.get("_doc_sim") is not None:
            doc_sim_pct = app["_doc_sim"] * 100

    st.markdown("---")

    # ════ QADAM 3 ════
    st.markdown('<span class="step">3</span> **Jamoat nazorati — aholi yulduzli baholari**', unsafe_allow_html=True)

    reviews = app.get("reviews", [])
    avg_rev = np.mean([r["baho"] for r in reviews]) if reviews else 0

    col1, col2, col3 = st.columns([2, 2, 3])
    with col1:
        if reviews:
            clr = "#dc2626" if avg_rev <= 2.5 else ("#d97706" if avg_rev <= 3.5 else "#16a34a")
            st.markdown(
                f'<div style="text-align:center;padding:16px;background:#f8fafc;border-radius:10px;border-top:4px solid {clr}">'
                f'<div style="font-size:40px;font-weight:800;color:{clr}">{avg_rev:.1f}</div>'
                f'<div style="font-size:20px">{"⭐"*round(avg_rev)}</div>'
                f'<div style="color:#64748b;font-size:12px">{len(reviews)} ta baho</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.info("Hali baho yo'q")
    with col2:
        if reviews:
            from collections import Counter
            dist = Counter(r["baho"] for r in reviews)
            for i in range(5, 0, -1):
                cnt = dist.get(i, 0)
                bar = int(cnt / len(reviews) * 20)
                st.write(f"{'⭐' * i} {'█' * bar}{'░' * (20 - bar)} {cnt}")
    with col3:
        if reviews:
            st.markdown("**Oxirgi sharhlar:**")
            for r in reviews[-4:]:
                st.markdown(
                    f'<div style="background:#f8fafc;border-radius:6px;padding:8px 12px;margin:4px 0">'
                    f'<b>{r["ism"]}</b> {"⭐" * r["baho"]}<br>'
                    f'<small style="color:#475569">{r["fikr"]}</small>'
                    f'<br><small style="color:#94a3b8">{r["sana"]}</small></div>',
                    unsafe_allow_html=True,
                )

    with st.expander("➕ Baho qo'shish"):
        with st.form("rev_f"):
            fc1, fc2 = st.columns([3, 1])
            with fc1:
                fikr = st.text_area("Fikringiz:", height=70, placeholder="Qurilish sifati, xavfsizlik...")
            with fc2:
                baho = st.select_slider("Baho:", options=[1, 2, 3, 4, 5], value=3)
                ism = st.text_input("Ism:", placeholder="Anonim")
            if st.form_submit_button("✈️ Yuborish", type="primary"):
                apps2 = load_data()
                for a2 in apps2:
                    if a2["id"] == sel_id:
                        a2.setdefault("reviews", []).append({
                            "ism": ism or "Anonim", "baho": baho,
                            "fikr": fikr, "sana": datetime.now().strftime("%Y-%m-%d"),
                        })
                save_data(apps2)
                st.success("✅ Fikringiz qo'shildi!")
                st.rerun()

    st.markdown("---")

    # ════ QADAM 4: AI XULOSA ════
    st.markdown('<span class="step">4</span> **AI Korrupsiya xulosasi**', unsafe_allow_html=True)

    organ_holat = ("Rad etildi → keyin tasdiqlandi" if rad_bor else
                   "Rad etildi" if app["holat"] == "rad" else "Tasdiqlandi")

    prev = app.get("ai_tahlil")
    if prev:
        st.markdown(
            f'<div class="card-blue">⏱️ Oxirgi tahlil: <b>{prev["sana"]}</b> | '
            f'Xavf: <b>{prev["daraja"]}</b> | Ball: {prev["ball"]}</div>',
            unsafe_allow_html=True,
        )

    if st.button("🤖 AI barcha ko'rsatkichlarni tahlil qilsin", type="primary", use_container_width=True):
        with st.spinner("AI tahlil qilmoqda..."):
            v = verdict(mezon_pct, doc_sim_pct, avg_rev, app["holat"], rad_bor, reviews)
            ai_text = ""
            if HF_TOKEN:
                ai_text = flan_analysis(
                    app["loyiha"], mezon_pct, organ_holat,
                    doc_sim_pct, avg_rev, len(reviews),
                )

        # ── Umumiy verdict ──
        st.markdown(
            f'<div class="verdict-box {v["cls"]}">'
            f'<h3 style="margin:0 0 8px 0">{v["level"]}</h3>'
            f'<div style="color:#374151">{v["umumiy"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # ── Ko'rsatkichlar jadvali ──
        st.markdown("#### 📊 3 ko'rsatkich xulosasi:")
        t1, t2, t3 = st.columns(3)
        with t1:
            c = "#dc2626" if mezon_pct < 60 else ("#d97706" if mezon_pct < 70 else "#16a34a")
            lbl = "❌ Juda past" if mezon_pct < 60 else ("⚠️ Chegaraviy" if mezon_pct < 70 else "✅ Normal")
            st.markdown(
                f'<div style="text-align:center;background:#f8fafc;border-radius:8px;padding:16px;border-top:4px solid {c}">'
                f'<b>🧮 Texnik mezon</b><br>'
                f'<span style="font-size:32px;font-weight:800;color:{c}">{mezon_pct:.0f}%</span><br>'
                f'<small>{lbl}</small></div>', unsafe_allow_html=True,
            )
        with t2:
            if rad_bor and doc_sim_pct > 0:
                c = "#dc2626" if doc_sim_pct >= 92 else ("#d97706" if doc_sim_pct >= 78 else "#16a34a")
                lbl = "❌ Xavfli (≥92%)" if doc_sim_pct >= 92 else ("⚠️ Shubhali" if doc_sim_pct >= 78 else "✅ Normal")
                val = f"{doc_sim_pct:.0f}%"
            else:
                c = "#94a3b8"; lbl = "Rad yo'q / Tekshirilmagan"; val = "—"
            st.markdown(
                f'<div style="text-align:center;background:#f8fafc;border-radius:8px;padding:16px;border-top:4px solid {c}">'
                f'<b>📄 Hujjat o\'xshashligi</b><br>'
                f'<span style="font-size:32px;font-weight:800;color:{c}">{val}</span><br>'
                f'<small>{lbl}</small></div>', unsafe_allow_html=True,
            )
        with t3:
            if reviews:
                c = "#dc2626" if avg_rev <= 2.5 else ("#d97706" if avg_rev <= 3.5 else "#16a34a")
                lbl = "❌ Qoniqarsiz" if avg_rev <= 2.5 else ("⚠️ O'rtacha" if avg_rev <= 3.5 else "✅ Yaxshi")
                val = f"{avg_rev:.1f}⭐"
            else:
                c = "#94a3b8"; lbl = "Baho yo'q"; val = "—"
            st.markdown(
                f'<div style="text-align:center;background:#f8fafc;border-radius:8px;padding:16px;border-top:4px solid {c}">'
                f'<b>⭐ Aholi bahosi</b><br>'
                f'<span style="font-size:32px;font-weight:800;color:{c}">{val}</span><br>'
                f'<small>{lbl}</small></div>', unsafe_allow_html=True,
            )

        # ── Xavf omillari (batafsil) ──
        if v["flags"]:
            st.markdown("#### ⚠️ Aniqlangan korrupsion alomatlar (batafsil):")
            for idx, fl in enumerate(v["flags"], 1):
                with st.expander(f"{fl['icon']} **{idx}. {fl['sarlavha']}**", expanded=True):
                    st.markdown(f'<div class="card-red"><b>Tavsif:</b><br>{fl["tavsif"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="card-blue"><b>💡 Tavsiya:</b><br>{fl["tavsiya"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card-green">✅ Aniqlanadigan korrupsion alomat topilmadi</div>', unsafe_allow_html=True)

        # ── AI model matni ──
        if ai_text:
            with st.expander("🤖 HuggingFace flan-t5 tahlil matni"):
                st.info(ai_text)
        elif HF_TOKEN:
            st.caption("flan-t5 modeli javob bermadi — qoida asosidagi tahlil ko'rsatildi")

        # Saqlash
        apps2 = load_data()
        for a2 in apps2:
            if a2["id"] == sel_id:
                a2["ai_tahlil"] = {
                    "sana": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "daraja": v["level"],
                    "ball": v["score"],
                    "alomatlar_soni": len(v["flags"]),
                }
        save_data(apps2)


# ════════════════════════════════════════════════════════════
#  PAGE: ARIZALAR
# ════════════════════════════════════════════════════════════
elif page == "📋 Arizalar ro'yxati":
    st.title("📋 Barcha arizalar")
    apps = load_data()

    filter_holat = st.selectbox("Filter:", ["Hammasi", "rad_keyin_tasdiq", "tasdiq", "rad"])
    filtered = apps if filter_holat == "Hammasi" else [a for a in apps if a["holat"] == filter_holat]

    for i, a in enumerate(filtered):
        pct = calc_score(a.get("mezon_ballari", {}))
        rad_bor = a["holat"] == "rad_keyin_tasdiq"
        w1 = set(a.get("rad_hujjat", "").lower().split())
        w2 = set(a.get("tasdiq_hujjat", "").lower().split())
        dsim = len(w1 & w2) / (len(w1 | w2) + 1e-9) * 100 if (w1 and w2) else 0
        revs = a.get("reviews", [])
        avg = np.mean([r["baho"] for r in revs]) if revs else 0
        v = verdict(pct, dsim, avg, a["holat"], rad_bor, revs)
        icon = "🔴" if v["score"] >= 50 else ("🟡" if v["score"] >= 20 else "🟢")

        hol_icons = {"tasdiq": "✅", "rad_keyin_tasdiq": "⚠️", "rad": "🚫"}
        with st.expander(f"{icon} **{a['id']}** | {a['loyiha']} {hol_icons.get(a['holat'],'?')}"):
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Mezon",    f"{pct:.0f}%")
            c2.metric("Hujjat",   f"{dsim:.0f}%" if rad_bor else "—")
            c3.metric("Baho",     f"{avg:.1f}⭐" if revs else "—")
            c4.metric("Xavf bali", v["score"])
            c5.metric("Holat",    v["level"].split()[0])
            if st.button("🔍 AI tahlil", key=f"list_{i}"):
                st.session_state["sel_id"] = a["id"]
                st.rerun()


# ════════════════════════════════════════════════════════════
#  PAGE: YANGI ARIZA
# ════════════════════════════════════════════════════════════
elif page == "➕ Yangi ariza":
    st.title("➕ Yangi ariza kiritish")

    with st.form("new_app"):
        c1, c2 = st.columns(2)
        with c1:
            nid = st.text_input("Ariza raqami", placeholder="QB-2024-004")
            loyiha = st.text_input("Loyiha nomi")
            tadbirkor = st.text_input("Tadbirkor")
            manzil = st.text_input("Manzil")
        with c2:
            tur = st.selectbox("Tur", [
                "Ko'p qavatli turar-joy (≥5 qavat)", "Ko'p qavatli turar-joy (<5 qavat)",
                "Tijorat binosi", "Ishlab chiqarish", "Ijtimoiy obyekt",
            ])
            qavatlar = st.number_input("Qavatlar", 1, 50, 10)
            bosqich = st.selectbox("Ruxsatnoma bosqichi", ["qurilish", "foydalanish"])
            holat = st.selectbox("Holat", ["rad_keyin_tasdiq", "tasdiq", "rad"])

        st.subheader("20 Mezon ballari (0=yo'q, 5=a'lo)")
        ballari = {}
        for dept_n in ["🧪 Sanitariya", "🔥 Yong'in", "🌿 Ekologiya", "🏗️ Qurilish"]:
            st.markdown(f"**{dept_n}**")
            dept_crit = [(k, n, w) for k, d, n, w in CRITERIA if d == dept_n]
            cols = st.columns(5)
            for i, (key, name, _) in enumerate(dept_crit):
                ballari[key] = cols[i].number_input(
                    name[:20], 0, 5, 3, key=f"nb_{key}"
                )

        rad_hujjat = st.text_area("Rad etilgan hujjat matni:", height=80)
        tasdiq_hujjat = st.text_area("Tasdiqlangan hujjat matni:", height=80)

        org_data = []
        st.subheader("Vakolatli organlar qarorlari")
        for org_nom in ["Sanitariya-Epidemiologiya", "Yong'in Xavfsizligi", "Ekologiya", "Qurilish Inspeksiyasi"]:
            with st.expander(org_nom):
                q1 = st.selectbox("1-qaror:", ["tasdiq", "rad"], key=f"q1_{org_nom}")
                s1 = st.text_area("Rad sababi (1):", key=f"s1_{org_nom}", height=60)
                q2 = st.selectbox("2-qaror:", ["tasdiq", "rad"], key=f"q2_{org_nom}")
                s2 = st.text_area("Rad sababi (2):", key=f"s2_{org_nom}", height=60)
                org_data.append({"nom": org_nom, "qaror_1": q1, "sabab_1": s1, "qaror_2": q2, "sabab_2": s2})

        if st.form_submit_button("💾 Saqlash", type="primary", use_container_width=True):
            if not nid or not loyiha:
                st.error("Ariza raqami va loyiha nomini kiriting!")
            else:
                apps2 = load_data()
                if any(a["id"] == nid for a in apps2):
                    st.error(f"{nid} ID allaqachon mavjud!")
                else:
                    apps2.append({
                        "id": nid, "loyiha": loyiha, "tadbirkor": tadbirkor,
                        "manzil": manzil, "tur": tur, "qavatlar": int(qavatlar),
                        "bosqich": bosqich, "sana": datetime.now().strftime("%Y-%m-%d"),
                        "holat": holat, "mezon_ballari": ballari,
                        "organlar": org_data, "rad_hujjat": rad_hujjat,
                        "tasdiq_hujjat": tasdiq_hujjat, "reviews": [],
                        "ai_tahlil": None, "_doc_sim": None,
                    })
                    save_data(apps2)
                    st.success(f"✅ Ariza {nid} saqlandi! AI tahlil uchun '🔍 AI Tahlil' bo'limiga o'ting.")


# ════════════════════════════════════════════════════════════
#  PAGE: STATISTIKA
# ════════════════════════════════════════════════════════════
elif page == "📊 Statistika":
    st.title("📊 Statistika va xavf xaritasi")
    apps = load_data()

    rows = []
    for a in apps:
        pct = calc_score(a.get("mezon_ballari", {}))
        rad_bor = a["holat"] == "rad_keyin_tasdiq"
        w1 = set(a.get("rad_hujjat", "").lower().split())
        w2 = set(a.get("tasdiq_hujjat", "").lower().split())
        dsim = len(w1 & w2) / (len(w1 | w2) + 1e-9) * 100 if (w1 and w2) else 0
        revs = a.get("reviews", [])
        avg = np.mean([r["baho"] for r in revs]) if revs else 0
        v = verdict(pct, dsim, avg, a["holat"], rad_bor, revs)
        rows.append({**a, "pct": pct, "dsim": dsim, "avg": avg, "vscore": v["score"], "vlevel": v["level"]})

    red_r = [r for r in rows if r["vscore"] >= 50]
    yel_r = [r for r in rows if 20 <= r["vscore"] < 50]
    grn_r = [r for r in rows if r["vscore"] < 20]

    cols = st.columns(5)
    for i, (lab, val, clr) in enumerate([
        ("Jami arizalar", len(rows), "#1e3a5f"),
        ("🔴 Yuqori xavf", len(red_r), "#dc2626"),
        ("🟡 O'rta xavf", len(yel_r), "#d97706"),
        ("🟢 Past xavf", len(grn_r), "#16a34a"),
        ("⚠️ Rad→Tasdiq", len([a for a in apps if a["holat"] == "rad_keyin_tasdiq"]), "#7c3aed"),
    ]):
        cols[i].markdown(
            f'<div class="kpi"><div class="kpi-val" style="color:{clr}">{val}</div>'
            f'<div class="kpi-lab">{lab}</div></div>', unsafe_allow_html=True,
        )

    st.divider()
    st.subheader("Arizalar xavf jadvali")
    header = st.columns([2, 3, 1, 1, 1, 1])
    for col, txt in zip(header, ["ID", "Loyiha", "Mezon%", "Hujjat%", "Baho", "Xavf"]):
        col.markdown(f"**{txt}**")

    for r in sorted(rows, key=lambda x: -x["vscore"]):
        icon = "🔴" if r["vscore"] >= 50 else ("🟡" if r["vscore"] >= 20 else "🟢")
        rc = st.columns([2, 3, 1, 1, 1, 1])
        rc[0].write(f"**{r['id']}**")
        rc[1].write(r["loyiha"][:28])
        rc[2].write(f"{r['pct']:.0f}%")
        rc[3].write(f"{r['dsim']:.0f}%" if r["holat"] == "rad_keyin_tasdiq" else "—")
        rc[4].write(f"{r['avg']:.1f}⭐" if r.get("reviews") else "—")
        rc[5].write(f"{icon} {r['vscore']}")

    st.divider()
    st.subheader("Bo'limlar bo'yicha o'rtacha muvofiqlik (barcha arizalar)")
    dept_avgs = {}
    for key, dept, _, w in CRITERIA:
        dept_avgs.setdefault(dept, [])
        for a in apps:
            dept_avgs[dept].append((a.get("mezon_ballari", {}).get(key, 0) / 5) * 100)

    dc = st.columns(4)
    for i, (dept, vals) in enumerate(dept_avgs.items()):
        avg_d = np.mean(vals)
        clr = "#dc2626" if avg_d < 60 else ("#d97706" if avg_d < 75 else "#16a34a")
        dc[i].markdown(
            f'<div style="text-align:center;padding:12px;background:#f8fafc;border-radius:8px;border-top:3px solid {clr}">'
            f'<b style="font-size:12px">{dept}</b><br>'
            f'<span style="font-size:26px;font-weight:800;color:{clr}">{avg_d:.0f}%</span></div>',
            unsafe_allow_html=True,
        )
        dc[i].progress(avg_d / 100)
