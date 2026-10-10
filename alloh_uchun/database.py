"""SQLite saqlash qatlami."""
from __future__ import annotations

import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional

from .models import ChallengeState, Confirmation, DayEntry, Status

SCHEMA = """
CREATE TABLE IF NOT EXISTS entries (
    day TEXT PRIMARY KEY,
    status TEXT NOT NULL CHECK (status IN ('success','difficult','setback')),
    confirmation TEXT CHECK (confirmation IN ('yes','no','undecided')),
    note TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS challenge_log (
    day TEXT PRIMARY KEY,
    challenge_id INTEGER NOT NULL,
    state TEXT NOT NULL CHECK (state IN ('done','skipped','later'))
);
"""


class RestoreError(Exception):
    pass


class Database:
    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.path))
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(SCHEMA)
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    # ---- kunlik yozuvlar -------------------------------------------------
    def save_entry(self, entry: DayEntry) -> None:
        """Yozuvni darhol saqlaydi (avtomatik saqlash)."""
        with self._conn:
            self._conn.execute(
                "INSERT INTO entries(day,status,confirmation,note,updated_at) VALUES(?,?,?,?,?) "
                "ON CONFLICT(day) DO UPDATE SET status=excluded.status, "
                "confirmation=excluded.confirmation, note=excluded.note, updated_at=excluded.updated_at",
                (
                    entry.day.isoformat(),
                    entry.status.value,
                    entry.confirmation.value if entry.confirmation else None,
                    entry.note,
                    datetime.now().isoformat(timespec="seconds"),
                ),
            )

    @staticmethod
    def _row_to_entry(row: sqlite3.Row) -> DayEntry:
        return DayEntry(
            day=date.fromisoformat(row["day"]),
            status=Status(row["status"]),
            confirmation=Confirmation(row["confirmation"]) if row["confirmation"] else None,
            note=row["note"],
        )

    def get_entry(self, day: date) -> Optional[DayEntry]:
        row = self._conn.execute("SELECT * FROM entries WHERE day=?", (day.isoformat(),)).fetchone()
        return self._row_to_entry(row) if row else None

    def delete_entry(self, day: date) -> None:
        with self._conn:
            self._conn.execute("DELETE FROM entries WHERE day=?", (day.isoformat(),))

    def entries_for_month(self, year: int, month: int) -> Dict[date, DayEntry]:
        prefix = f"{year:04d}-{month:02d}-"
        rows = self._conn.execute("SELECT * FROM entries WHERE day LIKE ?", (prefix + "%",)).fetchall()
        return {e.day: e for e in map(self._row_to_entry, rows)}

    def all_entries(self) -> List[DayEntry]:
        rows = self._conn.execute("SELECT * FROM entries ORDER BY day").fetchall()
        return [self._row_to_entry(r) for r in rows]

    def months_with_entries(self) -> List[tuple[int, int]]:
        rows = self._conn.execute(
            "SELECT DISTINCT substr(day,1,7) AS ym FROM entries ORDER BY ym DESC"
        ).fetchall()
        return [(int(r["ym"][:4]), int(r["ym"][5:7])) for r in rows]

    def delete_all(self) -> None:
        with self._conn:
            self._conn.execute("DELETE FROM entries")
            self._conn.execute("DELETE FROM challenge_log")

    # ---- sinovlar --------------------------------------------------------
    def set_challenge(self, day: date, challenge_id: int, state: ChallengeState) -> None:
        with self._conn:
            self._conn.execute(
                "INSERT INTO challenge_log(day,challenge_id,state) VALUES(?,?,?) "
                "ON CONFLICT(day) DO UPDATE SET challenge_id=excluded.challenge_id, state=excluded.state",
                (day.isoformat(), challenge_id, state.value),
            )

    def get_challenge(self, day: date) -> Optional[tuple[int, ChallengeState]]:
        row = self._conn.execute(
            "SELECT challenge_id,state FROM challenge_log WHERE day=?", (day.isoformat(),)
        ).fetchone()
        return (row["challenge_id"], ChallengeState(row["state"])) if row else None

    def challenges_by_state(self, state: ChallengeState) -> List[tuple[date, int]]:
        rows = self._conn.execute(
            "SELECT day,challenge_id FROM challenge_log WHERE state=? ORDER BY day DESC", (state.value,)
        ).fetchall()
        return [(date.fromisoformat(r["day"]), r["challenge_id"]) for r in rows]

    # ---- zaxira nusxa / tiklash -----------------------------------------
    def backup_to(self, target: Path | str) -> None:
        target = Path(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            target.unlink()
        dest = sqlite3.connect(str(target))
        try:
            self._conn.backup(dest)
        finally:
            dest.close()

    def restore_from(self, source: Path | str) -> None:
        """Zaxira fayldan tiklaydi. Fayl yaroqsiz bo'lsa, joriy ma'lumotlar o'zgarmaydi."""
        source = Path(source)
        if not source.is_file():
            raise RestoreError("Fayl topilmadi.")
        try:
            src = sqlite3.connect(f"file:{source.as_posix()}?mode=ro", uri=True)
        except sqlite3.Error as exc:
            raise RestoreError(f"Faylni ochib bo‘lmadi: {exc}") from exc
        try:
            try:
                names = {r[0] for r in src.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                if "entries" not in names:
                    raise RestoreError("Bu ALLOH UCHUN zaxira fayli emas.")
                cols = {r[1] for r in src.execute("PRAGMA table_info(entries)")}
                if not {"day", "status", "confirmation", "note"} <= cols:
                    raise RestoreError("Zaxira fayl tuzilmasi mos emas.")
            except sqlite3.DatabaseError as exc:
                raise RestoreError("Bu yaroqli SQLite fayli emas.") from exc
            src.backup(self._conn)
        finally:
            src.close()
        self._conn.executescript(SCHEMA)  # eski zaxiradagi yo'q jadvallar uchun
        self._conn.commit()
