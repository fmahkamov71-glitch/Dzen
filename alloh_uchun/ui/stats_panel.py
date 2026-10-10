"""Statistika paneli."""
from __future__ import annotations

from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QWidget

from ..stats import MonthStats


class StatsPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("card")
        grid = QGridLayout(self)
        grid.setContentsMargins(14, 12, 14, 12)
        self._values: dict[str, QLabel] = {}
        items = [
            ("recorded", "Yozilgan kunlar"),
            ("successful", "Tasdiqlangan muvaffaqiyatli kunlar"),
            ("difficult", "Qiyin kunlar"),
            ("setback", "Maqsad buzilgan kunlar"),
            ("percent", "Oylik muvaffaqiyat foizi"),
            ("current", "Joriy seriya"),
            ("longest", "Eng uzun seriya"),
        ]
        for i, (key, name) in enumerate(items):
            cell = QWidget()
            cell.setStyleSheet("background: transparent;")
            lay = QGridLayout(cell)
            lay.setContentsMargins(0, 0, 0, 0)
            val = QLabel("0")
            val.setObjectName("statValue")
            nm = QLabel(name)
            nm.setObjectName("statName")
            nm.setWordWrap(True)
            lay.addWidget(val, 0, 0)
            lay.addWidget(nm, 1, 0)
            grid.addWidget(cell, i // 4, i % 4)
            self._values[key] = val

    def update_stats(self, ms: MonthStats, current: int, longest: int) -> None:
        v = self._values
        v["recorded"].setText(str(ms.recorded))
        v["successful"].setText(str(ms.successful))
        v["difficult"].setText(str(ms.difficult))
        v["setback"].setText(str(ms.setback))
        v["percent"].setText("—" if ms.success_percent is None else f"{ms.success_percent:g}%")
        v["current"].setText(f"{current} kun")
        v["longest"].setText(f"{longest} kun")
