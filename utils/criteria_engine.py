"""
20 ta mezon - 4 ta bo'lim bo'yicha
"""

CRITERIA = {
    "sanitariya": {
        "nomi": "🧪 Sanitariya-Epidemiologiya",
        "rang": "#e91e63",
        "mezonlar": [
            {
                "id": "s1",
                "nomi": "Sanitariya muhofaza zonasi masofasi",
                "tavsif": "Loyiha sanitariya muhofaza zonasi talablariga mos kelishi",
                "max_ball": 20,
                "savol": "Qurilish joyi va yaqin atrof-muhit orasidagi sanitariya masofasi qanday?",
                "variantlar": {
                    "Barcha talablarga to'liq mos": 20,
                    "Asosan mos, kichik kamchiliklar": 14,
                    "Qisman mos": 8,
                    "Talablarga mos emas": 0
                }
            },
            {
                "id": "s2",
                "nomi": "Ichimlik suvi ta'minoti sifati",
                "tavsif": "Loyihada ichimlik suvi ta'minoti va sifat nazorati",
                "max_ball": 15,
                "savol": "Ichimlik suvi ta'minoti tizimi holati?",
                "variantlar": {
                    "Markazlashgan tizimga ulangan, sertifikatlangan": 15,
                    "Markazlashgan, lekin sertifikat yo'q": 10,
                    "Muqobil manba, tekshirilgan": 6,
                    "Noaniq yoki ko'rsatilmagan": 0
                }
            },
            {
                "id": "s3",
                "nomi": "Chiqindi oqava suv tizimi",
                "tavsif": "Kanalizatsiya va chiqindi suvlarni tozalash",
                "max_ball": 15,
                "savol": "Chiqindi oqava suv tizimi holati?",
                "variantlar": {
                    "Markazlashgan kanalizatsiya, loyihalashtirilgan": 15,
                    "Lokal tozalash qurilmasi bilan": 10,
                    "Qisman yechim": 5,
                    "Yechim ko'rsatilmagan": 0
                }
            },
            {
                "id": "s4",
                "nomi": "Shovqin va vibratsiya darajasi",
                "tavsif": "Qurilish va ekspluatatsiya davrida shovqin normalariga muvofiqlik",
                "max_ball": 10,
                "savol": "Shovqin darajasi baholash hujjatlari mavjudmi?",
                "variantlar": {
                    "To'liq baholash o'tkazilgan, normada": 10,
                    "Qisman baholash": 6,
                    "Faqat deklaratsiya": 2,
                    "Hujjat yo'q": 0
                }
            },
            {
                "id": "s5",
                "nomi": "Havo ifloslanishi nazorati",
                "tavsif": "Qurilish davrida havo sifatini nazorat qilish",
                "max_ball": 10,
                "savol": "Havo ifloslanishini nazorat qilish choralar?",
                "variantlar": {
                    "To'liq atrof-muhit ta'siri baholandi": 10,
                    "Standart chora-tadbirlar rejalashtirilgan": 6,
                    "Minimal choralar": 2,
                    "Hech qanday chora ko'rilmagan": 0
                }
            }
        ]
    },
    "yonghin": {
        "nomi": "🔥 Yong'in Xavfsizligi",
        "rang": "#ff5722",
        "mezonlar": [
            {
                "id": "y1",
                "nomi": "Yong'in chiqish yo'llari va evakuatsiya",
                "tavsif": "Bino evakuatsiya yo'llari loyiha talablariga muvofiqligi",
                "max_ball": 20,
                "savol": "Evakuatsiya yo'llari va zinapoyalar holati?",
                "variantlar": {
                    "Barcha normativlarga to'liq mos": 20,
                    "Asosiy talablar bajarilgan": 13,
                    "Kamchiliklar mavjud": 7,
                    "Jiddiy muammolar bor": 0
                }
            },
            {
                "id": "y2",
                "nomi": "Avtomatik yong'in o'chirish tizimi",
                "tavsif": "Sprinkler va boshqa avtomatik o'chirish tizimlari",
                "max_ball": 20,
                "savol": "Avtomatik yong'in o'chirish tizimi loyihalashtirilganmi?",
                "variantlar": {
                    "To'liq AYOT tizimi loyihalashtirilgan": 20,
                    "Qisman tizim": 12,
                    "Qo'l bilan o'chirish vositalarigina": 5,
                    "Hech qanday tizim ko'zda tutilmagan": 0
                }
            },
            {
                "id": "y3",
                "nomi": "Yong'inga chidamli konstruksiyalar",
                "tavsif": "Bino materiallarining yong'inga chidamliligi",
                "max_ball": 15,
                "savol": "Qurilish materiallarining yong'inga chidamliligi darajasi?",
                "variantlar": {
                    "I-II darajali yong'inga chidamlilik": 15,
                    "III daraja": 10,
                    "IV daraja": 4,
                    "V daraja yoki ko'rsatilmagan": 0
                }
            },
            {
                "id": "y4",
                "nomi": "Favqulodda yoritish va signalizatsiya",
                "tavsif": "Zaxira yoritish va yong'in ogohlantirish tizimi",
                "max_ball": 10,
                "savol": "Favqulodda yoritish va ogohlantirish tizimi?",
                "variantlar": {
                    "To'liq avtomatik tizim": 10,
                    "Qo'lda boshqariladigan": 6,
                    "Minimal vositalar": 2,
                    "Ko'zda tutilmagan": 0
                }
            },
            {
                "id": "y5",
                "nomi": "Yong'in xavfsizligi driveway va yondoshish",
                "tavsif": "Yong'in avtomobillari uchun kirishlar va suv olish manbalari",
                "max_ball": 15,
                "savol": "Yong'in mashinasi uchun kirish yo'li va gidrantlar?",
                "variantlar": {
                    "Barcha talablar bajarilgan": 15,
                    "Kirish yo'li bor, gidrant yo'q": 8,
                    "Qisman ta'minlangan": 4,
                    "Ko'zda tutilmagan": 0
                }
            }
        ]
    },
    "ekologiya": {
        "nomi": "🌿 Ekologiya",
        "rang": "#4caf50",
        "mezonlar": [
            {
                "id": "e1",
                "nomi": "Chiqindilarni boshqarish va utilizatsiya",
                "tavsif": "Qurilish va ekspluatatsiya chiqindilarini boshqarish rejasi",
                "max_ball": 15,
                "savol": "Chiqindilarni boshqarish rejasi mavjudmi?",
                "variantlar": {
                    "To'liq boshqarish rejasi bilan": 15,
                    "Qisman reja": 9,
                    "Umumiy deklaratsiya bor": 4,
                    "Reja yo'q": 0
                }
            },
            {
                "id": "e2",
                "nomi": "Yashil zonalar va ko'kalamzorlashtirish",
                "tavsif": "Loyihadagi yashil maydon foizi va daraxt saqlanishi",
                "max_ball": 10,
                "savol": "Yashil zona va ko'kalamzorlashtirish rejasi?",
                "variantlar": {
                    "Normadan yuqori yashil zona": 10,
                    "Normaga mos": 7,
                    "Qisman mos": 3,
                    "Normalarga mos emas": 0
                }
            },
            {
                "id": "e3",
                "nomi": "Tuproq va yer osti suvlari muhofazasi",
                "tavsif": "Qurilish davrida tuproq ifloslanishidan himoya",
                "max_ball": 15,
                "savol": "Tuproq muhofazasi choralari?",
                "variantlar": {
                    "Kompleks muhofaza choralari ko'rilgan": 15,
                    "Standart choralar": 9,
                    "Minimal choralar": 4,
                    "Choralar ko'rilmagan": 0
                }
            },
            {
                "id": "e4",
                "nomi": "Atmosfera emissiyalari nazorati",
                "tavsif": "Havo ifloslanishi normalariga muvofiqlik",
                "max_ball": 20,
                "savol": "Atmosfera emissiyalari baholash hujjatlari?",
                "variantlar": {
                    "Atrof-muhitga ta'sir baholandi (AMTB)": 20,
                    "Qisman baholash": 12,
                    "Faqat deklaratsiya": 5,
                    "Baholash yo'q": 0
                }
            },
            {
                "id": "e5",
                "nomi": "Suv havzalari va sug'orish kanallari muhofazasi",
                "tavsif": "Yaqin suv manbalari muhofaza zonasiga rioya qilish",
                "max_ball": 10,
                "savol": "Yaqin suv havzalarini muhofaza qilish choralari?",
                "variantlar": {
                    "Muhofaza zonalari to'liq hisobga olingan": 10,
                    "Qisman hisobga olingan": 6,
                    "Faqat eslatib o'tilgan": 2,
                    "Ko'rsatilmagan": 0
                }
            }
        ]
    },
    "qurilish": {
        "nomi": "🏗️ Qurilish Bo'limi",
        "rang": "#2196f3",
        "mezonlar": [
            {
                "id": "q1",
                "nomi": "Loyiha hujjatlari to'liqligi",
                "tavsif": "Barcha talab qilinadigan loyiha hujjatlarining mavjudligi",
                "max_ball": 25,
                "savol": "Loyiha hujjatlari to'plami holati?",
                "variantlar": {
                    "To'liq hujjatlar to'plami mavjud": 25,
                    "Asosiy hujjatlar bor, qo'shimchalar yetishmaydi": 16,
                    "Qisman hujjatlar": 8,
                    "Jiddiy kamchiliklar": 0
                }
            },
            {
                "id": "q2",
                "nomi": "Me'moriy va shaharsozlik talablari",
                "tavsif": "Bosh reja va shaharsozlik reglamentlariga muvofiqlik",
                "max_ball": 20,
                "savol": "Shaharsozlik me'yorlariga muvofiqlik?",
                "variantlar": {
                    "To'liq mos, barcha cheklovlar hisobga olingan": 20,
                    "Asosan mos": 13,
                    "Qisman mos": 6,
                    "Mos emas": 0
                }
            },
            {
                "id": "q3",
                "nomi": "Konstruktiv mustahkamlik va seysmoturgunlik",
                "tavsif": "Bino konstruksiyasining mustahkamligi va zilzilaga chidamliligi hisob-kitoblari",
                "max_ball": 25,
                "savol": "Konstruktiv hisob-kitoblar va seysmoturgunlik?",
                "variantlar": {
                    "To'liq hisob-kitoblar, sertifikatlangan": 25,
                    "Hisob-kitoblar bor, ekspertiza o'tilmagan": 16,
                    "Qisman hisob-kitoblar": 8,
                    "Hisob-kitoblar yo'q": 0
                }
            },
            {
                "id": "q4",
                "nomi": "Muhandislik kommunikatsiyalari loyihasi",
                "tavsif": "Elektr, suv, isitish, gaz kommunikatsiyalari loyihasi",
                "max_ball": 15,
                "savol": "Muhandislik kommunikatsiyalari loyihasi holati?",
                "variantlar": {
                    "Barcha kommunikatsiyalar to'liq loyihalashtirilgan": 15,
                    "Asosiy kommunikatsiyalar bor": 9,
                    "Qisman loyiha": 4,
                    "Loyiha yo'q": 0
                }
            },
            {
                "id": "q5",
                "nomi": "Yer uchastkasidan foydalanish huquqi hujjatlari",
                "tavsif": "Qurilish uchun yer uchastkasi huquqiy holati",
                "max_ball": 20,
                "savol": "Yer uchastkasi huquqiy hujjatlari?",
                "variantlar": {
                    "To'liq rasmiylashtrilgan, kadastr raqami bor": 20,
                    "Rasmiylashtirish jarayonida": 12,
                    "Vaqtincha hujjatlar": 5,
                    "Hujjatlar yo'q yoki nizoli": 0
                }
            }
        ]
    }
}

def get_max_total_score():
    """Jami maksimal ball"""
    total = 0
    for dept_data in CRITERIA.values():
        for mezon in dept_data["mezonlar"]:
            total += mezon["max_ball"]
    return total

def get_dept_max_score(dept_key):
    """Bo'lim bo'yicha maksimal ball"""
    return sum(m["max_ball"] for m in CRITERIA[dept_key]["mezonlar"])

def calculate_risk_level(score_percent):
    """Risk darajasini hisoblash"""
    if score_percent >= 80:
        return "PAST", "🟢", "#4caf50"
    elif score_percent >= 60:
        return "O'RTA", "🟡", "#ff9800"
    elif score_percent >= 40:
        return "YUQORI", "🟠", "#ff5722"
    else:
        return "JUDA YUQORI", "🔴", "#f44336"

def get_all_criteria_list():
    """Barcha mezonlar ro'yxati"""
    all_criteria = []
    for dept_key, dept_data in CRITERIA.items():
        for mezon in dept_data["mezonlar"]:
            mezon_copy = mezon.copy()
            mezon_copy["bo'lim"] = dept_key
            mezon_copy["bo'lim_nomi"] = dept_data["nomi"]
            mezon_copy["rang"] = dept_data["rang"]
            all_criteria.append(mezon_copy)
    return all_criteria
