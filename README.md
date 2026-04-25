# 🏗️ E-Construction — Korrupsiyaga qarshi AI tizimi

Qurilish sohasidagi korrupsiyani 3 usulda avtomatik aniqlaydi:
1. **Hujjat taqqoslash** — rad etilgan va tasdiqlangan hujjatlar bir xilmi?
2. **20 mezon baholash** — loyiha past ball olgan bo'lsa ham tasdiqlanganligi
3. **Foydalanuvchi fikrlari** — aholi bahosi rasmiy xulosaga zidmi?

---

## 🚀 Ishga tushirish

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🤗 HuggingFace Token ulash (MUHIM)

### Nima uchun token kerak?
Token bo'lmasa ham dastur ishlaydi (Jaccard fallback usuli bilan),
lekin token ulansa semantik AI tahlil aniqroq bo'ladi.

### Token olish — qadamba-qadam:

**1-qadam:** https://huggingface.co ga kiring (ro'yxatdan o'ting)

**2-qadam:** Yuqori o'ng burchakda profilingizga kiring:
```
Profile → Settings → Access Tokens
```

**3-qadam:** "New token" tugmasini bosing:
- **Name:** e-construction  
- **Role:** `Read` (yozish huquqi shart emas)
- "Generate token" bosing

**4-qadam:** Tokenni nusxalab oling:
```
hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
⚠️ Bu tokenni biror joyga saqlang — bir marta ko'rsatiladi!

---

## 🔐 Token ulash — 2 usul

### Usul A — Streamlit Cloud (deployment uchun)
Streamlit Cloud da:
```
App settings → Secrets → quyidagini qo'shing:
```
```toml
HF_TOKEN = "hf_sizning_tokeningiz"
```

### Usul B — Lokal ishlatish uchun
`.streamlit/secrets.toml` faylini yarating:
```toml
HF_TOKEN = "hf_sizning_tokeningiz"
```

Yoki terminal orqali:
```bash
export HF_TOKEN="hf_sizning_tokeningiz"
streamlit run app.py
```

---

## 🤖 Qaysi model — va nima uchun?

### Tanlangan model: `paraphrase-multilingual-MiniLM-L12-v2`

| Xususiyat | Qiymat |
|-----------|--------|
| Til qo'llovi | O'zbek, Rus, Ingliz (50+ til) |
| Hajmi | 118 MB — yengil |
| Aniqlik | Semantic o'xshashlikda juda aniq |
| Narxi | **Mutlaqo bepul** |
| API cheklovi | Kunda 30,000 so'rov (bepul hisob) |

### Nima uchun bu model optimal?
- Ko'p qavatli arxitektura (12 qavat transformer)
- Hujjat semantikasini tushunadi — nafaqat so'z sanoq
- O'zbek va Rus tilida yaxshi ishlaydi
- HuggingFace Inference API orqali token kerak emas ham (bepul tier)

### Bepul tier cheklovlari:
- Kunda ~30,000 so'rov
- Ba'zan 10-30 soniya kechikish (model "uxlab" qoladi)
- Birinchi so'rovda model yuklanadi (~10-20 soniya)

### Agar token bo'lmasa nima bo'ladi?
Dastur **Jaccard similarity** (so'z ustma-ustma kelishi) usulini ishlatadi.
Bu ham ishlaydi, lekin semantik tahlil kamroq aniq bo'ladi.

---

## 📊 20 Mezon tuzilmasi

| Bo'lim | Mezon soni | Maks ball |
|--------|-----------|-----------|
| Sanitariya-Epidemiologiya | 5 | 21 |
| Yong'in Xavfsizligi | 5 | 22 |
| Ekologiya | 5 | 18 |
| Qurilish Bo'limi | 5 | 23 |
| **Jami** | **20** | **84** |

---

## ⚠️ Xavf belgilari

| Signal | Shart | Natija |
|--------|-------|--------|
| 🔴 Hujjat | Rad vs tasdiq ≥ 92% o'xshash | Ariza qizilga kiradi |
| 🔴 Mezon | Ball < 60% + tasdiq berilgan | Ariza qizilga kiradi |
| 🔴 Fikr | Foydalanuvchi ≤ 2.5 ball + rasmiy tasdiq | Ariza qizilga kiradi |

---

## 📁 Fayl tuzilmasi

```
e_construction/
├── app.py                    ← Asosiy dastur
├── requirements.txt          ← Kutubxonalar
├── .gitignore
├── .streamlit/
│   └── secrets.toml          ← HF_TOKEN (GitHub ga yuklamang!)
└── data/
    └── applications.json     ← Saqlangan ma'lumotlar
```

---

## 🚀 Streamlit Cloud ga deploy qilish

```bash
# GitHub ga yuklang
git init
git add . 
git add -f .streamlit/  # secrets.toml yuklamang!
git commit -m "E-Construction AI"
git push origin main
```

Keyin:
1. https://share.streamlit.io ga kiring
2. "New app" → GitHub reponi tanlang
3. **Secrets bo'limiga HF_TOKEN kiriting**
4. Deploy!
