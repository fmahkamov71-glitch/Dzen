"""Motivatsion xabarlar, kunlik sinovlar va 10 daqiqalik nazorat rejasi.

Iqtiboslar faqat matni va manbasi ishonchli bo'lgan oyatlar/hadislardan olingan.
Ular "ma'nosi" sifatida beriladi (tarjima emas, mazmun).
"""
from __future__ import annotations

import random
from datetime import date
from typing import List, Optional

from .models import Status

# (matn, manba yoki None)
MESSAGES: dict[str, List[tuple[str, Optional[str]]]] = {
    "success": [
        ("Bugungi g‘alabang kichik ko‘rinishi mumkin, lekin intizom aynan shunday quriladi — kunma-kun.", None),
        ("Sen bugun o‘z so‘zingda turding. Bu tuyg‘uni eslab qol, ertaga u senga kuch beradi.", None),
        ("Niyatni to‘g‘ri qilish — yo‘lning yarmi. Bugun uni amalda ko‘rsatding.", None),
        ("Mukammallik shart emas. Muhimi — davom etish. Bugun davom etding.", None),
        ("Amallar niyatlarga qarab baholanadi.", "Hadis, Sahih al-Buxoriy 1; Sahih Muslim 1907 (ma’nosi)"),
    ],
    "difficult": [
        ("Qiyin kunda ham turib berish — bu ham kuch. O‘zingga mehribon bo‘l, lekin qat’iy qol.", None),
        ("Hissiyot to‘lqin kabi: ko‘tariladi, cho‘qqiga chiqadi va pasayadi. Sen uni kutib o‘tishing mumkin.", None),
        ("Bugun qiyin bo‘lgani — sen zaifsan degani emas. Sen kurashayotganingni bildiradi.", None),
        ("Albatta, qiyinchilik bilan birga yengillik bor.", "Qur’on, Inshirah surasi, 94:5–6 (ma’nosi)"),
        ("Sabr va namoz orqali (Allohdan) yordam so‘rang.", "Qur’on, Baqara surasi, 2:153 (ma’nosi)"),
    ],
    "setback": [
        ("Yiqilish — oxiri emas. Muhimi, bugun nima o‘rgangani va ertaga nima qilishing.", None),
        ("Bir kun butun yo‘lingni o‘chirib tashlamaydi. Ayb qilish o‘rniga, aniq reja qur.", None),
        ("O‘zingni ayblash kuch bermaydi; tushunish va qayta boshlash beradi. Bugun yangi boshlanish mumkin.", None),
        ("Allohning rahmatidan noumid bo‘lmanglar.", "Qur’on, Zumar surasi, 39:53 (ma’nosi)"),
        ("Nima bu holatga olib keldi? Vaqt, joy, his-tuyg‘u — yozib qo‘y va keyingi safar uni oldindan sezib ol.", None),
    ],
}

# Mavzu bo'yicha qo'shimcha (sabr, niyat, intizom, qayta tiklanish) — har holatda ko'rsatish mumkin
GENERAL: List[tuple[str, Optional[str]]] = [
    ("Sabr — kutish emas, kutayotganda to‘g‘ri tanlov qilishdir.", None),
    ("Intizom — hohlamasangiz ham, o‘zingiz uchun muhim ishni qilish odatidir.", None),
    ("Niyatni har ertalab yangila: nima uchun bu yo‘ldaman?", None),
    ("Kichik odatlar katta o‘zgarishlarni yaratadi. Bugun faqat bugunga e’tibor ber.", None),
]

# (id, matn) — ID barqaror bo'lishi kerak (bazada saqlanadi); mavjudlarini o'zgartirmang
CHALLENGES: List[tuple[int, str]] = [
    (1, "Bir stakan suv ich va 2 daqiqa nafasingga e’tibor ber (4 soniya olish, 6 soniya chiqarish)."),
    (2, "Telefondan bugun vasvasa qiladigan ilova yoki saytlarni vaqtincha yopib qo‘y."),
    (3, "10 daqiqa piyoda yur — iloji bo‘lsa, tashqarida."),
    (4, "Bugungi niyatingni bir jumla bilan yozib qo‘y."),
    (5, "Do‘st yoki oila a’zosiga qisqa xabar yoz yoki qo‘ng‘iroq qil."),
    (6, "Kechqurun telefonni yotoqdan uzoqroqqa qo‘y va kitob o‘qi."),
    (7, "5 daqiqa Qur’on tilovatini tingla yoki zikr qil."),
    (8, "Xonangni 10 daqiqa tartibga keltir — muhitni o‘zgartirish ham yordam beradi."),
    (9, "Bugun qaysi vaqt eng qiyin bo‘lishini aniqla va o‘sha vaqtga foydali ish rejalashtir."),
    (10, "Yengil jismoniy mashq qil: 20 ta o‘tirib-turish yoki cho‘zilish."),
    (11, "Bugun uchun uchta minnatdorchilik sababini yoz."),
    (12, "Yolg‘iz qolishdan qoch: eshik ochiq joyda, odamlar orasida ishla yoki o‘qi."),
]

URGE_PLAN: List[tuple[str, str]] = [
    ("1-2 daqiqa: To‘xta va nafas ol",
     "Hozir qilayotgan ishingni to‘xtat. 4 soniya nafas ol, 6 soniya chiqar — 6 marta takrorla. "
     "O‘zingga ayt: «Bu tuyg‘u o‘tadi. Men uni kutib o‘tishim mumkin.» Bu — kurash, uyat emas."),
    ("3-4 daqiqa: Muhitni o‘zgartir",
     "Turgan joyingdan turib, boshqa xonaga yoki tashqariga chiq. Eshik yopiq, yolg‘iz joyda qolma. "
     "Yuzingni sovuq suv bilan yuv, abdest ol — bu tanani ham, fikrni ham tiklaydi."),
    ("5-6 daqiqa: Vasvasa manbasini uzib qo‘y",
     "Telefon yoki kompyuterdagi vasvasali kontentni yop. Kerak bo‘lsa, qurilmani boshqa xonaga qo‘y "
     "yoki ishonchli odamga topshir. Kirish yo‘lini qiyinlashtirish — aqlli qaror."),
    ("7-9 daqiqa: Xavfsiz muqobil faoliyat",
     "Qo‘llaring va fikringni band qiladigan ish tanla: piyoda yurish, yengil mashq, idish yuvish, "
     "do‘stga qo‘ng‘iroq, Qur’on tinglash yoki zikr, kitob o‘qish."),
    ("10-daqiqa: Niyatni eslab, o‘zingni qo‘llab-quvvatla",
     "O‘zingdan so‘ra: «Nima uchun bu yo‘ldaman?» Niyatni qayta yangila va keyingi bir soatga kichik reja qil. "
     "Agar urg‘u hali ham kuchli bo‘lsa, yana 10 daqiqa takrorla yoki ishonchli odam bilan gaplash. "
     "Agar o‘zingga zarar yetkazish fikrlari bo‘lsa, darhol yaqin odamingdan yoki mutaxassisdan yordam so‘ra."),
]


def pick_message(status: Status, rng: Optional[random.Random] = None) -> tuple[str, Optional[str]]:
    rng = rng or random
    pool = MESSAGES[status.value] + (GENERAL if rng.random() < 0.3 else [])
    return rng.choice(pool)


def challenge_by_id(cid: int) -> Optional[str]:
    return dict(CHALLENGES).get(cid)


def daily_challenge_id(day: date) -> int:
    """Berilgan sana uchun barqaror (deterministik) sinov."""
    return CHALLENGES[day.toordinal() % len(CHALLENGES)][0]


def random_challenge(rng: Optional[random.Random] = None) -> tuple[int, str]:
    return (rng or random).choice(CHALLENGES)
