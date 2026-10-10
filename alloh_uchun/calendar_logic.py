"""Kalendar mantig'i (Gregorian, kabisa yillari bilan)."""
from __future__ import annotations

import calendar
from datetime import date
from typing import List

MONTH_NAMES = [
    "Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
    "Iyul", "Avgust", "Sentyabr", "Oktyabr", "Noyabr", "Dekabr",
]
WEEKDAY_NAMES = ["Du", "Se", "Chor", "Pay", "Ju", "Sha", "Yak"]  # dushanba birinchi


def is_leap(year: int) -> bool:
    return calendar.isleap(year)


def days_in_month(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]


def month_grid(year: int, month: int) -> List[List[date | None]]:
    """Haftalar ro'yxati (dushanbadan boshlab); oy tashqarisidagi kataklar None."""
    weeks = calendar.Calendar(firstweekday=0).monthdatescalendar(year, month)
    return [[d if d.month == month else None for d in week] for week in weeks]


def shift_month(year: int, month: int, delta: int) -> tuple[int, int]:
    idx = year * 12 + (month - 1) + delta
    return idx // 12, idx % 12 + 1


def month_title(year: int, month: int) -> str:
    return f"{MONTH_NAMES[month - 1]} {year}"
