from datetime import date, timedelta

import pytest

from alloh_uchun import calendar_logic as cal
from alloh_uchun.database import Database, RestoreError
from alloh_uchun.models import Confirmation, DayEntry, Status
from alloh_uchun.stats import current_streak, longest_streak, month_stats

S, D, B = Status.SUCCESS, Status.DIFFICULT, Status.SETBACK


def e(day, status=S, conf=None, note=""):
    return DayEntry(day, status, conf, note)


# ---- kalendar --------------------------------------------------------------
@pytest.mark.parametrize("y,m,n", [
    (2023, 2, 28), (2024, 2, 29), (1900, 2, 28), (2000, 2, 29),
    (2024, 4, 30), (2024, 1, 31), (2024, 12, 31),
])
def test_days_in_month(y, m, n):
    assert cal.days_in_month(y, m) == n


def test_leap_years():
    assert cal.is_leap(2024) and cal.is_leap(2000)
    assert not cal.is_leap(1900) and not cal.is_leap(2023)


def test_month_grid_contains_every_day_once():
    for y, m in [(2024, 2), (2023, 2), (2024, 3), (2024, 4)]:
        days = [d for w in cal.month_grid(y, m) for d in w if d]
        assert days == [date(y, m, i) for i in range(1, cal.days_in_month(y, m) + 1)]
        assert all(len(w) == 7 for w in cal.month_grid(y, m))


def test_month_grid_weekday_alignment():
    # 1 Mart 2024 — juma (indeks 4)
    assert cal.month_grid(2024, 3)[0][4] == date(2024, 3, 1)


def test_shift_month_wraps_years():
    assert cal.shift_month(2024, 12, 1) == (2025, 1)
    assert cal.shift_month(2024, 1, -1) == (2023, 12)
    assert cal.shift_month(2024, 5, -17) == (2022, 12)


# ---- saqlash / tahrirlash --------------------------------------------------
def test_save_and_edit_entry(db):
    d = date(2024, 5, 10)
    db.save_entry(e(d, S, note="birinchi"))
    assert db.get_entry(d).note == "birinchi"
    db.save_entry(e(d, B, note="o‘zgardi"))
    got = db.get_entry(d)
    assert got.status is B and got.note == "o‘zgardi"
    assert len(db.all_entries()) == 1


def test_unrecorded_dates_stay_unrecorded(db):
    db.save_entry(e(date(2024, 5, 10)))
    assert db.get_entry(date(2024, 5, 9)) is None
    assert set(db.entries_for_month(2024, 5)) == {date(2024, 5, 10)}


def test_delete_entry(db):
    d = date(2024, 5, 10)
    db.save_entry(e(d))
    db.delete_entry(d)
    assert db.get_entry(d) is None


def test_confirmation_stored_separately_and_not_inferred(db):
    d = date(2024, 5, 10)
    db.save_entry(e(d, D, Confirmation.UNDECIDED))
    got = db.get_entry(d)
    assert got.status is D and got.confirmation is Confirmation.UNDECIDED
    assert not got.is_confirmed_success
    db.save_entry(e(d, D, Confirmation.NO))
    assert not db.get_entry(d).is_confirmed_success
    db.save_entry(e(d, D, Confirmation.YES))
    assert db.get_entry(d).is_confirmed_success


def test_confirmation_only_for_difficult():
    with pytest.raises(ValueError):
        DayEntry(date(2024, 1, 1), S, Confirmation.YES)


# ---- seriyalar ---------------------------------------------------------------
def test_longest_streak_consecutive_only():
    base = date(2024, 5, 1)
    entries = [e(base + timedelta(days=i)) for i in (0, 1, 2, 4, 5)]  # 3 kun, ttanaffus, 2 kun
    assert longest_streak(entries) == 3


def test_missing_date_breaks_streak():
    entries = [e(date(2024, 5, 1)), e(date(2024, 5, 3))]
    assert longest_streak(entries) == 1


def test_unconfirmed_difficult_breaks_streak():
    entries = [e(date(2024, 5, 1)), e(date(2024, 5, 2), D, Confirmation.UNDECIDED), e(date(2024, 5, 3))]
    assert longest_streak(entries) == 1
    entries[1] = e(date(2024, 5, 2), D, Confirmation.YES)
    assert longest_streak(entries) == 3
    entries[1] = e(date(2024, 5, 2), D, Confirmation.NO)
    assert longest_streak(entries) == 1


def test_streak_across_month_and_year_boundary():
    entries = [e(date(2023, 12, 30)), e(date(2023, 12, 31)), e(date(2024, 1, 1))]
    assert longest_streak(entries) == 3
    assert current_streak(entries, date(2024, 1, 1)) == 3


def test_streak_over_leap_day():
    entries = [e(date(2024, 2, 28)), e(date(2024, 2, 29)), e(date(2024, 3, 1))]
    assert longest_streak(entries) == 3


def test_current_streak_rules():
    today = date(2024, 5, 10)
    run = [e(today - timedelta(days=i)) for i in (1, 2, 3)]
    assert current_streak(run, today) == 3               # bugun yozilmagan: kechadan
    assert current_streak(run + [e(today)], today) == 4  # bugun muvaffaqiyat
    assert current_streak(run + [e(today, B)], today) == 0
    assert current_streak(run + [e(today, D, Confirmation.UNDECIDED)], today) == 0
    assert current_streak([e(today - timedelta(days=2))], today) == 0  # kecha yo'q
    assert current_streak([], today) == 0


# ---- oylik statistika ------------------------------------------------------
def test_month_stats():
    entries = [
        e(date(2024, 5, 1)), e(date(2024, 5, 2)),
        e(date(2024, 5, 3), D, Confirmation.YES),
        e(date(2024, 5, 4), D, Confirmation.UNDECIDED),
        e(date(2024, 5, 5), B),
        e(date(2024, 4, 30)),  # boshqa oy
    ]
    ms = month_stats(entries, 2024, 5)
    assert (ms.recorded, ms.successful, ms.difficult, ms.setback) == (5, 3, 2, 1)
    assert ms.success_percent == 60.0


def test_month_stats_empty_has_no_percent():
    ms = month_stats([], 2024, 5)
    assert ms.recorded == 0 and ms.success_percent is None


# ---- doimiylik (qayta ishga tushirish) ------------------------------------
def test_persistence_after_restart(tmp_path):
    path = tmp_path / "p.db"
    db1 = Database(path)
    db1.save_entry(e(date(2024, 5, 1), D, Confirmation.NO, "izoh"))
    db1.close()
    db2 = Database(path)
    got = db2.get_entry(date(2024, 5, 1))
    assert got == e(date(2024, 5, 1), D, Confirmation.NO, "izoh")
    db2.close()


# ---- zaxira / tiklash / o'chirish -----------------------------------------
def test_backup_and_restore(db, tmp_path):
    db.save_entry(e(date(2024, 5, 1), note="a"))
    db.save_entry(e(date(2024, 5, 2), B))
    backup = tmp_path / "b" / "backup.db"
    db.backup_to(backup)
    db.delete_all()
    assert db.all_entries() == []
    db.restore_from(backup)
    assert [x.day for x in db.all_entries()] == [date(2024, 5, 1), date(2024, 5, 2)]
    assert db.get_entry(date(2024, 5, 1)).note == "a"


def test_restore_invalid_file_keeps_data(db, tmp_path):
    db.save_entry(e(date(2024, 5, 1)))
    bad = tmp_path / "bad.db"
    bad.write_text("bu sqlite emas")
    with pytest.raises(RestoreError):
        db.restore_from(bad)
    with pytest.raises(RestoreError):
        db.restore_from(tmp_path / "yoq.db")
    assert len(db.all_entries()) == 1


def test_restore_foreign_sqlite_rejected(db, tmp_path):
    import sqlite3
    other = tmp_path / "other.db"
    c = sqlite3.connect(other)
    c.execute("CREATE TABLE x(a)")
    c.commit()
    c.close()
    db.save_entry(e(date(2024, 5, 1)))
    with pytest.raises(RestoreError):
        db.restore_from(other)
    assert len(db.all_entries()) == 1


def test_months_with_entries_history(db):
    db.save_entry(e(date(2024, 3, 1)))
    db.save_entry(e(date(2024, 5, 1)))
    assert db.months_with_entries() == [(2024, 5), (2024, 3)]


# ---- motivatsiya ----------------------------------------------------------
def test_motivation_content():
    from alloh_uchun.motivation import CHALLENGES, MESSAGES, URGE_PLAN, daily_challenge_id, pick_message
    for st in Status:
        assert len(MESSAGES[st.value]) >= 4
        text, _ = pick_message(st)
        assert text
    ids = [c[0] for c in CHALLENGES]
    assert len(ids) == len(set(ids))
    assert daily_challenge_id(date(2024, 5, 1)) == daily_challenge_id(date(2024, 5, 1))
    assert len(URGE_PLAN) == 5


def test_challenge_log(db):
    from alloh_uchun.models import ChallengeState
    d = date(2024, 5, 1)
    assert db.get_challenge(d) is None
    db.set_challenge(d, 3, ChallengeState.LATER)
    assert db.get_challenge(d) == (3, ChallengeState.LATER)
    db.set_challenge(d, 3, ChallengeState.DONE)
    assert db.get_challenge(d) == (3, ChallengeState.DONE)
