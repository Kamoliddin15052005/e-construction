"""
AI Tahlil moduli - HuggingFace bepul modellari orqali
Qo'llaniladigan modellar:
  1. sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (mahalliy, bepul)
  2. HuggingFace Inference API - mistralai/Mixtral-8x7B-Instruct-v0.1 (API, bepul tier)
"""

import requests
import json
import re
import streamlit as st
from typing import Optional

# HuggingFace Inference API endpoint
HF_API_URL = "https://api-inference.huggingface.co/models/"

REJECTION_KEYWORDS_UZ = [
    "talablarga javob bermaydi", "hujjat yetishmaydi", "loyiha noto'liq",
    "normativlarga mos emas", "qayta ko'rib chiqish", "to'ldirish zarur",
    "xato hisob-kitob", "sanitariya me'yorlari buzilgan", "yong'in xavfsizligi",
    "ekologik talablar", "yer hujjati", "ruxsat berilmaydi"
]

CORRUPTION_KEYWORDS = [
    "to'liq loyiha", "barcha talablar bajarilgan", "muvofiq",
    "tasdiqlansin", "ruxsat berilsin"
]


def analyze_with_hf_api(text: str, hf_token: str, task: str = "text-generation") -> Optional[str]:
    """
    HuggingFace Inference API orqali tahlil
    Bepul: Mistral, Zephyr, Phi-2 modellari
    """
    # Bepul modellar: mistralai/Mistral-7B-Instruct-v0.2, HuggingFaceH4/zephyr-7b-beta
    model = "mistralai/Mistral-7B-Instruct-v0.2"
    
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    prompt = f"""[INST] Sen O'zbekiston qurilish ruxsatnomalari bo'yicha korrupsiya analizatorisin.
    
Quyidagi matnni o'qi va qisqa xulosa ber (o'zbek tilida, 3-5 gap):
1. Asosiy muammolar nima?
2. Noto'g'ri rad etish sabablari bormi?
3. Korrupsion xavf darajasi qanday?

Matn: {text[:1000]}

Xulosa: [/INST]"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.3,
            "do_sample": True,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(
            f"{HF_API_URL}{model}",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "")
        elif response.status_code == 503:
            return "⏳ Model yuklanmoqda, bir daqiqa kuting va qayta urining..."
        else:
            return f"API xatosi: {response.status_code}"
    except Exception as e:
        return f"Ulanish xatosi: {str(e)}"


def analyze_rejection_reasons(rejection_text: str, changes_text: str) -> dict:
    """
    Qaytarish sabablari va amalga oshirilgan o'zgarishlarni taqqoslash
    Rule-based + semantic analysis
    """
    results = {
        "inconsistencies": [],
        "risk_score": 0,
        "details": []
    }
    
    if not rejection_text or not changes_text:
        return results
    
    # Kalit so'zlar orqali tahlil
    rejection_lower = rejection_text.lower()
    changes_lower = changes_text.lower()
    
    # Rad etish sabablarini ajratib olish
    rejection_issues = []
    for keyword in REJECTION_KEYWORDS_UZ:
        if keyword in rejection_lower:
            rejection_issues.append(keyword)
    
    # O'zgartirishlar rad etish sabablariga mos keladimi?
    addressed = 0
    for issue in rejection_issues:
        # Kalimani o'zgartirishlar matnida qidirish
        issue_words = issue.split()
        for word in issue_words:
            if word in changes_lower and len(word) > 4:
                addressed += 1
                break
    
    if rejection_issues:
        address_rate = addressed / len(rejection_issues)
    else:
        address_rate = 1.0
    
    # Noto'g'ri mos kelishlar
    if address_rate < 0.3 and rejection_issues:
        results["inconsistencies"].append(
            f"⚠️ Rad etish sabablarining {(1-address_rate)*100:.0f}% o'zgartirishlar bilan hal qilinmagan"
        )
        results["risk_score"] += 40
    elif address_rate < 0.6 and rejection_issues:
        results["inconsistencies"].append(
            f"⚠️ Qisman hal qilingan: {(1-address_rate)*100:.0f}% sabablar qolmoqda"
        )
        results["risk_score"] += 20
    
    # O'zgartirishlar hajmi tekshirish
    if len(changes_text) < 50 and len(rejection_text) > 100:
        results["inconsistencies"].append(
            "⚠️ O'zgartirishlar juda qisqa - rad etish sabablariga nisbatan"
        )
        results["risk_score"] += 25
    
    results["address_rate"] = address_rate
    results["rejection_issues_count"] = len(rejection_issues)
    
    return results


def calculate_corruption_score(
    criteria_scores: dict,
    dept_approvals: dict,
    rejection_analysis: dict,
    user_rating: Optional[float] = None
) -> dict:
    """
    Asosiy korrupsiya ball hisoblash algoritmi
    3 komponent: mezonlar, rad etish tahlili, foydalanuvchi bahosi
    """
    
    corruption_indicators = []
    total_risk_score = 0
    
    # 1. MEZONLAR TAHLILI
    total_score = sum(criteria_scores.values()) if criteria_scores else 0
    max_possible = 350  # 20 mezon jami maksimal
    
    if max_possible > 0:
        score_percent = (total_score / max_possible) * 100
    else:
        score_percent = 0
    
    # Qancha bo'limlar tasdiqlagan?
    approved_depts = sum(1 for approved in dept_approvals.values() if approved)
    
    # Past ball, lekin ko'p tasdiqlash - korrupsiya belgisi!
    if score_percent < 50 and approved_depts >= 3:
        risk = 50 + (50 - score_percent)
        corruption_indicators.append({
            "tur": "JIDDIY",
            "rang": "#f44336",
            "matn": f"🚨 ASOSIY SIGNAL: Ball {score_percent:.0f}% lekin {approved_depts} bo'lim tasdiqlagan!",
            "ball": risk
        })
        total_risk_score += risk
    
    elif score_percent < 65 and approved_depts >= 2:
        risk = 30
        corruption_indicators.append({
            "tur": "O'RTA",
            "rang": "#ff9800",
            "matn": f"⚠️ Ball {score_percent:.0f}% lekin {approved_depts} bo'lim tasdiqlagan",
            "ball": risk
        })
        total_risk_score += risk
    
    # 2. RAD ETISH TAHLILI
    if rejection_analysis:
        rej_risk = rejection_analysis.get("risk_score", 0)
        if rej_risk > 0:
            total_risk_score += rej_risk
            for inconsistency in rejection_analysis.get("inconsistencies", []):
                corruption_indicators.append({
                    "tur": "TAQQOSLASH",
                    "rang": "#ff5722",
                    "matn": inconsistency,
                    "ball": rej_risk // 2
                })
    
    # 3. FOYDALANUVCHI BAHOSI
    if user_rating is not None:
        # Rasmiy tasdiqlash lekin past foydalanuvchi bahosi
        if user_rating < 2.5 and approved_depts >= 2:
            risk = 25
            corruption_indicators.append({
                "tur": "FOYDALANUVCHI",
                "rang": "#9c27b0",
                "matn": f"⚠️ Rasmiy tasdiqlangan, lekin foydalanuvchi bahosi: {user_rating:.1f}/5.0",
                "ball": risk
            })
            total_risk_score += risk
        elif user_rating < 3.5 and approved_depts >= 3:
            risk = 15
            corruption_indicators.append({
                "tur": "FOYDALANUVCHI",
                "rang": "#9c27b0",
                "matn": f"ℹ️ Past foydalanuvchi bahosi: {user_rating:.1f}/5.0 ({approved_depts} ta tasdiqlash bilan)",
                "ball": risk
            })
            total_risk_score += risk
    
    # Umumiy xulosa
    total_risk_score = min(100, total_risk_score)
    
    if total_risk_score >= 70:
        verdict = "🔴 JIDDIY KORRUPSION XAVF"
        flag_color = "red"
        recommendation = "Darhol tekshiruv uchun yuborish tavsiya etiladi!"
    elif total_risk_score >= 40:
        verdict = "🟠 O'RTA KORRUPSION XAVF"
        flag_color = "orange"
        recommendation = "Qo'shimcha tekshiruv o'tkazish kerak"
    elif total_risk_score >= 20:
        verdict = "🟡 PAST KORRUPSION XAVF"
        flag_color = "yellow"
        recommendation = "Kuzatib borish tavsiya etiladi"
    else:
        verdict = "🟢 XAVF ANIQLANMADI"
        flag_color = "green"
        recommendation = "Ariza me'yorlarga muvofiq"
    
    return {
        "total_risk_score": total_risk_score,
        "verdict": verdict,
        "flag_color": flag_color,
        "recommendation": recommendation,
        "indicators": corruption_indicators,
        "score_percent": score_percent,
        "approved_depts": approved_depts
    }


def local_text_analysis(text: str) -> dict:
    """
    Mahalliy (internet siz) matn tahlili - rule-based
    """
    if not text:
        return {"risk_words": [], "positive_words": [], "risk_count": 0}
    
    text_lower = text.lower()
    
    found_risk = [kw for kw in REJECTION_KEYWORDS_UZ if kw in text_lower]
    found_positive = [kw for kw in CORRUPTION_KEYWORDS if kw in text_lower]
    
    return {
        "risk_words": found_risk,
        "positive_words": found_positive,
        "risk_count": len(found_risk),
        "suspicious": len(found_positive) > 3 and len(found_risk) == 0
    }
