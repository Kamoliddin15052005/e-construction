"""
Ma'lumotlar saqlash - JSON fayl asosida (ishlab chiqarishda PostgreSQL/Supabase)
"""

import json
import os
import uuid
from datetime import datetime
from typing import Optional, List, Dict

DATA_FILE = "data/applications.json"


def ensure_data_file():
    """Ma'lumotlar faylini yaratish"""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        # Demo ma'lumotlar
        demo_data = {
            "applications": [
                {
                    "id": "APP-2025-001",
                    "tadbirkor": "Abdullayev Jamshid",
                    "loyiha_nomi": "15 qavatli turar-joy",
                    "manzil": "Toshkent sh., Yunusobod t.",
                    "tur": "Ko'p qavatli turar-joy",
                    "maydon": 2500,
                    "qavatlar": 15,
                    "sana": "2025-01-15",
                    "holat": "qaytarilgan",
                    "criteria_scores": {
                        "s1": 8, "s2": 10, "s3": 5, "s4": 2, "s5": 2,
                        "y1": 7, "y2": 12, "y3": 4, "y4": 2, "y5": 4,
                        "e1": 4, "e2": 3, "e3": 4, "e4": 5, "e4": 5, "e5": 2,
                        "q1": 8, "q2": 6, "q3": 8, "q4": 4, "q5": 5
                    },
                    "dept_approvals": {"sanitariya": True, "yonghin": True, "ekologiya": False, "qurilish": True},
                    "rad_sabab": "Loyiha seysmoturgunlik talablariga to'liq javob bermaydi. Konstruktiv hisob-kitoblarda xatolar mavjud. Yong'in o'chirish tizimi loyihasi to'liq emas.",
                    "ozgartirishlar": "Seysmoturgunlik bo'yicha qo'shimcha hujjat taqdim etildi.",
                    "user_rating": 2.1,
                    "risk_score": 78,
                    "flag": "red"
                },
                {
                    "id": "APP-2025-002",
                    "tadbirkor": "Rahimov Saidakbar",
                    "loyiha_nomi": "Savdo markazi 'Premium'",
                    "manzil": "Samarqand sh., Registon yaqini",
                    "tur": "Tijorat bino",
                    "maydon": 5000,
                    "qavatlar": 4,
                    "sana": "2025-01-20",
                    "holat": "tasdiqlangan",
                    "criteria_scores": {
                        "s1": 18, "s2": 13, "s3": 12, "s4": 8, "s5": 8,
                        "y1": 18, "y2": 17, "y3": 13, "y4": 9, "y5": 13,
                        "e1": 13, "e2": 9, "e3": 13, "e4": 17, "e5": 9,
                        "q1": 22, "q2": 18, "q3": 22, "q4": 13, "q5": 18
                    },
                    "dept_approvals": {"sanitariya": True, "yonghin": True, "ekologiya": True, "qurilish": True},
                    "rad_sabab": "",
                    "ozgartirishlar": "",
                    "user_rating": 4.2,
                    "risk_score": 12,
                    "flag": "green"
                },
                {
                    "id": "APP-2025-003",
                    "tadbirkor": "Xolmatov Dilshod",
                    "loyiha_nomi": "Industrial ombor kompleksi",
                    "manzil": "Andijon sh., sanoat zonasi",
                    "tur": "Sanoat binosi",
                    "maydon": 8000,
                    "qavatlar": 2,
                    "sana": "2025-02-01",
                    "holat": "tekshiruvda",
                    "criteria_scores": {
                        "s1": 14, "s2": 10, "s3": 10, "s4": 6, "s5": 6,
                        "y1": 13, "y2": 12, "y3": 10, "y4": 6, "y5": 8,
                        "e1": 9, "e2": 7, "e3": 9, "e4": 12, "e5": 6,
                        "q1": 16, "q2": 13, "q3": 16, "q4": 9, "q5": 12
                    },
                    "dept_approvals": {"sanitariya": True, "yonghin": False, "ekologiya": True, "qurilish": False},
                    "rad_sabab": "Yong'in xavfsizligi tizimi talablarga mos emas. Qurilish hujjatlari to'liq emas.",
                    "ozgartirishlar": "Yong'in xavfsizligi bo'yicha qo'shimcha loyiha taqdim etildi. Hujjatlar to'ldirildi.",
                    "user_rating": None,
                    "risk_score": 35,
                    "flag": "yellow"
                }
            ]
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(demo_data, f, ensure_ascii=False, indent=2)


def load_applications() -> List[Dict]:
    """Barcha arizalarni yuklash"""
    ensure_data_file()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("applications", [])
    except:
        return []


def save_application(app_data: Dict) -> bool:
    """Yangi ariza saqlash"""
    ensure_data_file()
    try:
        applications = load_applications()
        
        # ID yaratish
        if "id" not in app_data:
            app_data["id"] = f"APP-{datetime.now().year}-{str(uuid.uuid4())[:6].upper()}"
        
        app_data["sana"] = datetime.now().strftime("%Y-%m-%d")
        
        applications.append(app_data)
        
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"applications": applications}, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Saqlash xatosi: {e}")
        return False


def get_application(app_id: str) -> Optional[Dict]:
    """ID bo'yicha ariza olish"""
    applications = load_applications()
    for app in applications:
        if app.get("id") == app_id:
            return app
    return None


def update_application(app_id: str, updates: Dict) -> bool:
    """Arizani yangilash"""
    ensure_data_file()
    try:
        applications = load_applications()
        for i, app in enumerate(applications):
            if app.get("id") == app_id:
                applications[i].update(updates)
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump({"applications": applications}, f, ensure_ascii=False, indent=2)
                return True
        return False
    except:
        return False


def get_statistics() -> Dict:
    """Statistika hisoblash"""
    applications = load_applications()
    
    total = len(applications)
    red_flags = sum(1 for a in applications if a.get("flag") == "red")
    green = sum(1 for a in applications if a.get("flag") == "green")
    yellow = sum(1 for a in applications if a.get("flag") == "yellow")
    
    avg_risk = 0
    if total > 0:
        avg_risk = sum(a.get("risk_score", 0) for a in applications) / total
    
    return {
        "total": total,
        "red": red_flags,
        "green": green,
        "yellow": yellow,
        "avg_risk": avg_risk,
        "rejection_rate": sum(1 for a in applications if a.get("holat") == "qaytarilgan") / max(total, 1)
    }
