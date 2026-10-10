"""Ilova ma'lumotlari uchun yozish mumkin bo'lgan papka."""
from __future__ import annotations

import os
import sys
from pathlib import Path

DB_FILENAME = "alloh_uchun.db"


def data_dir() -> Path:
    """Windows: %APPDATA%\\ALLOH_UCHUN. ALLOH_UCHUN_DATA_DIR bilan almashtirish mumkin."""
    override = os.environ.get("ALLOH_UCHUN_DATA_DIR")
    if override:
        base = Path(override)
    elif sys.platform == "win32":
        base = Path(os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming") / "ALLOH_UCHUN"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share") / "ALLOH_UCHUN"
    base.mkdir(parents=True, exist_ok=True)
    return base


def default_db_path() -> Path:
    return data_dir() / DB_FILENAME
