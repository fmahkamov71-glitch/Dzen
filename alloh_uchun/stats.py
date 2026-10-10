"""Statistika hisoblari. Qoidalar README.md da hujjatlashtirilgan."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable, Optional

from .models import DayEntry, Status


@dataclass(frozen=True)
class MonthStats:
    recorded: int
    successful: int
    difficult: int
    setback: int
    success_percent: Optional[float]  # yozuv yo'q bo'lsa None


def month_stats(entries: Iterable[DayEntry], year: int, month: int) -> MonthStats:
    month_entries = [e for e in entries if e.day.year == year and e.day.month == month]
    recorded = len(month_entries)
    successful = sum(1 for e in month_entries if e.is_confirmed_success)
    difficult = sum(1 for e in month_entries if e.status is Status.DIFFICULT)
    setback = sum(1 for e in month_entries if e.status is Status.SETBACK)
    percent = round(100.0 * successful / recorded, 1) if recorded else None
    return MonthStats(recorded, successful, difficult, setback, percent)


def _success_days(entries: Iterable[DayEntry]) -> set[date]:
    return {e.day for e in entries if e.is_confirmed_success}


def longest_streak(entries: Iterable[DayEntry]) -> int:
    days = sorted(_success_days(entries))
    best = run = 0
    prev: Optional[date] = None
    for d in days:
        run = run + 1 if prev is not None and d - prev == timedelta(days=1) else 1
        best = max(best, run)
        prev = d
    return best


def current_streak(entries: Iterable[DayEntry], today: date) -> int:
    """Bugundan orqaga ketma-ket tasdiqlangan muvaffaqiyatli kunlar soni.

    - Bugun tasdiqlangan muvaffaqiyat bo'lsa, hisob bugundan boshlanadi.
    - Bugun umuman yozilmagan bo'lsa, hisob kechadan boshlanadi (seriya uzilmaydi, lekin
      bugun muvaffaqiyat deb ham sanalmaydi).
    - Bugun yozilgan, ammo tasdiqlanmagan/buzilgan bo'lsa, joriy seriya 0.
    """
    entries = list(entries)
    days = _success_days(entries)
    recorded_today = any(e.day == today for e in entries)
    if today in days:
        cursor = today
    elif recorded_today:
        return 0
    else:
        cursor = today - timedelta(days=1)
    count = 0
    while cursor in days:
        count += 1
        cursor -= timedelta(days=1)
    return count
