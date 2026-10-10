"""Interaktiv oylik kalendar."""
from __future__ import annotations

from datetime import date
from typing import Dict

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from .. import calendar_logic as cal
from ..models import DayEntry, Status
from . import theme

_STATUS_COLORS = {
    Status.SUCCESS: theme.COL_SUCCESS,
    Status.DIFFICULT: theme.COL_DIFFICULT,
    Status.SETBACK: theme.COL_SETBACK,
}


class CalendarWidget(QWidget):
    dateSelected = Signal(date)
    monthChanged = Signal(int, int)

    def __init__(self, today: date | None = None) -> None:
        super().__init__()
        self._today = today or date.today()
        self.year, self.month = self._today.year, self._today.month
        self.selected: date | None = None
        self._entries: Dict[date, DayEntry] = {}

        root = QVBoxLayout(self)
        nav = QHBoxLayout()
        self.prev_btn = QPushButton("◀")
        self.next_btn = QPushButton("▶")
        self.today_btn = QPushButton("Bugun")
        self.title = QLabel()
        self.title.setObjectName("monthTitle")
        self.title.setAlignment(Qt.AlignCenter)
        for b in (self.prev_btn, self.next_btn):
            b.setFixedWidth(48)
        self.prev_btn.clicked.connect(lambda: self.go_month(-1))
        self.next_btn.clicked.connect(lambda: self.go_month(1))
        self.today_btn.clicked.connect(self.go_today)
        nav.addWidget(self.prev_btn)
        nav.addWidget(self.title, 1)
        nav.addWidget(self.today_btn)
        nav.addWidget(self.next_btn)
        root.addLayout(nav)

        self.grid = QGridLayout()
        self.grid.setSpacing(6)
        root.addLayout(self.grid)
        self.cells: Dict[date, QPushButton] = {}
        self._rebuild()

    def set_entries(self, entries: Dict[date, DayEntry]) -> None:
        self._entries = entries
        self._rebuild()

    def go_month(self, delta: int) -> None:
        self.year, self.month = cal.shift_month(self.year, self.month, delta)
        self.monthChanged.emit(self.year, self.month)

    def go_today(self) -> None:
        self.year, self.month = self._today.year, self._today.month
        self.monthChanged.emit(self.year, self.month)

    def _rebuild(self) -> None:
        while self.grid.count():
            w = self.grid.takeAt(0).widget()
            if w:
                w.hide()
                w.setParent(None)
                w.deleteLater()
        self.cells.clear()
        self.title.setText(cal.month_title(self.year, self.month))
        for col, name in enumerate(cal.WEEKDAY_NAMES):
            lbl = QLabel(name)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f"color: {theme.GOLD}; font-weight: bold;")
            self.grid.addWidget(lbl, 0, col)
        for r, week in enumerate(cal.month_grid(self.year, self.month), start=1):
            for c, d in enumerate(week):
                if d is None:
                    continue
                btn = QPushButton(str(d.day))
                btn.setObjectName("dayCell")
                btn.setMinimumSize(56, 52)
                entry = self._entries.get(d)
                border = theme.GOLD if d == self._today else "#23302a"
                if d == self.selected:
                    border = "#ffffff"
                bg = theme.PANEL
                text = ""
                if entry:
                    bg = _STATUS_COLORS[entry.status]
                    if entry.status is Status.DIFFICULT and entry.confirmation is not None:
                        text = {"yes": "✓", "no": "✗", "undecided": "?"}[entry.confirmation.value]
                    elif entry.status is Status.SUCCESS:
                        text = "✓"
                    if text:
                        btn.setText(f"{d.day}\n{text}")
                    btn.setToolTip(entry.status.label)
                btn.setStyleSheet(
                    f"QPushButton#dayCell {{ background: {bg}; border: 2px solid {border}; color: {theme.TEXT}; }}"
                )
                btn.clicked.connect(lambda _=False, dd=d: self._select(dd))
                self.grid.addWidget(btn, r, c)
                self.cells[d] = btn

    def _select(self, d: date) -> None:
        self.selected = d
        self._rebuild()
        self.dateSelected.emit(d)
