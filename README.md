# 🏗️ E-Construction Anti-Korrupsiya Tizimi

Qurilish ruxsatnomalari jarayonidagi korrupsion holatlarni AI yordamida aniqlash tizimi.

## 📋 Loyiha haqida

Bu tizim qurilish ruxsatnomalari jarayonida:
1. **20 mezon** bo'yicha loyihani avtomatik baholaydi
2. **Vakolatli organlar** qarorlari bilan taqqoslaydi  
3. **Rad etish ~ O'zgartirishlar** nomutanosibligini aniqlaydi
4. **Foydalanuvchi baholari** bilan solishtirib korrupsiyani topadi

## 🚀 O'rnatish va Ishga Tushirish

### 1. Kerakli kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 2. Ishga tushirish
```bash
streamlit run app.py
```

### 3. HuggingFace Token (AI uchun)
1. [huggingface.co](https://huggingface.co) ga boring
2. Bepul ro'yxatdan o'ting
3. Settings → Access Tokens → New Token (Read) yarating
4. Tizimda ⚙️ Sozlamalar → AI Sozlamalari bo'limiga kiriting

## 📁 Fayl Strukturasi

```
e-construction/
├── app.py                    # Asosiy Streamlit ilovasi
├── requirements.txt          # Kutubxonalar
├── pages/
│   ├── home.py              # Bosh sahifa
│   ├── application.py       # Ariza kiritish
│   ├── ai_analysis.py       # AI tahlil
│   ├── corruption_detector.py # Korrupsiya detektori
│   ├── user_reviews.py      # Foydalanuvchi baholari
│   ├── dashboard.py         # Statistika
│   └── settings.py          # Sozlamalar
├── utils/
│   ├── criteria_engine.py   # 20 mezon logikasi
│   ├── ai_analyzer.py       # HuggingFace AI
│   └── data_store.py        # Ma'lumotlar saqlash
└── data/
    └── applications.json    # Ma'lumotlar bazasi (demo)
```

## 🤖 AI Texnologiyasi

### Bepul HuggingFace Modellari:
| Model | Tavsif |
|-------|--------|
| Mistral-7B-Instruct | Eng yaxshi sifat, ko'p tilli |
| Phi-3-mini | Tez, engil, samarali |
| Zephyr-7B | Yaxshi instruksiya bajaradi |

### Mahalliy Tahlil (Internet siz):
- Rule-based scoring (20 mezon)
- Kalit so'z tahlili (O'zbek tili)
- Pattern matching algoritmi

## 📊 Korrupsiya Aniqlash Algoritmi

Tizim **3 ta signal** ni taqqoslaydi:

```
Korrupsiya Bali = 
  (Mezon balli anomaliyasi × 0.5) +
  (Rad etish ~ O'zgartirishlar nomutanosibligi × 0.3) +
  (Foydalanuvchi bahosi anomaliyasi × 0.2)
```

### Signal qoidalari:
- 🔴 **70+** → Jiddiy korrupsion xavf (Darhol tekshiruv)
- 🟠 **40-70** → O'rta xavf (Qo'shimcha tekshiruv)
- 🟡 **20-40** → Past xavf (Kuzatib borish)
- 🟢 **0-20** → Xavf yo'q

## 🏗️ Ishlab chiqarish uchun

```python
# .env fayl yarating
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
HF_TOKEN=hf_your_token_here
MY_GOV_UZ_API=your_api_key
```

## 📞 Bog'lanish
E-Construction Jamoasi | O'zbekiston Respublikasi | 2025
