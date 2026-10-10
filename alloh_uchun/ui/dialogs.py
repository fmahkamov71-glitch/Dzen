"""Dialoglar: kunlik yozuv, motivatsiya, sinov, nazorat rejasi."""
from __future__ import annotations

from datetime import date
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup, QDialog, QFrame, QHBoxLayout, QLabel, QMessageBox, QPushButton,
    QRadioButton, QScrollArea, QTextEdit, QVBoxLayout, QWidget,
)

from .. import calendar_logic as cal
from ..models import ChallengeState, Confirmation, DayEntry, Status
from ..motivation import URGE_PLAN, challenge_by_id


def _fmt(d: date) -> str:
    return f"{d.day} {cal.MONTH_NAMES[d.month - 1]} {d.year}"


class EntryDialog(QDialog):
    """Kunlik holat, tasdiq va shaxsiy izoh."""

    def __init__(self, day: date, existing: Optional[DayEntry], parent=None) -> None:
        super().__init__(parent)
        self.day = day
        self.deleted = False
        self.result_entry: Optional[DayEntry] = None
        self.setWindowTitle(f"Kun: {_fmt(day)}")
        self.setMinimumWidth(460)
        lay = QVBoxLayout(self)
        head = QLabel(_fmt(day))
        head.setObjectName("monthTitle")
        lay.addWidget(head)

        self.status_group = QButtonGroup(self)
        self.status_radios: dict[Status, QRadioButton] = {}
        for st in Status:
            rb = QRadioButton(st.label)
            self.status_group.addButton(rb)
            self.status_radios[st] = rb
            lay.addWidget(rb)
            rb.toggled.connect(self._refresh_confirm)

        self.confirm_box = QFrame()
        self.confirm_box.setObjectName("card")
        cl = QVBoxLayout(self.confirm_box)
        cl.addWidget(QLabel("Majburiyatingizni saqlab qoldingizmi?"))
        self.conf_group = QButtonGroup(self)
        self.conf_radios: dict[Confirmation, QRadioButton] = {}
        for c in Confirmation:
            rb = QRadioButton(c.label)
            self.conf_group.addButton(rb)
            self.conf_radios[c] = rb
            cl.addWidget(rb)
        lay.addWidget(self.confirm_box)

        lay.addWidget(QLabel("Shaxsiy izoh (ixtiyoriy, faqat shu qurilmada saqlanadi):"))
        self.note = QTextEdit()
        self.note.setMinimumHeight(110)
        lay.addWidget(self.note)

        btns = QHBoxLayout()
        if existing:
            d = QPushButton("Yozuvni o‘chirish")
            d.clicked.connect(self._delete)
            btns.addWidget(d)
        btns.addStretch(1)
        cancel = QPushButton("Bekor qilish")
        cancel.clicked.connect(self.reject)
        self.save_btn = QPushButton("Saqlash")
        self.save_btn.setObjectName("primary")
        self.save_btn.clicked.connect(self._save)
        btns.addWidget(cancel)
        btns.addWidget(self.save_btn)
        lay.addLayout(btns)

        if existing:
            self.status_radios[existing.status].setChecked(True)
            if existing.confirmation:
                self.conf_radios[existing.confirmation].setChecked(True)
            self.note.setPlainText(existing.note)
        self._refresh_confirm()

    def _selected_status(self) -> Optional[Status]:
        return next((s for s, r in self.status_radios.items() if r.isChecked()), None)

    def _selected_confirmation(self) -> Optional[Confirmation]:
        return next((c for c, r in self.conf_radios.items() if r.isChecked()), None)

    def _refresh_confirm(self) -> None:
        self.confirm_box.setVisible(self._selected_status() is Status.DIFFICULT)

    def _save(self) -> None:
        st = self._selected_status()
        if st is None:
            QMessageBox.information(self, "ALLOH UCHUN", "Iltimos, kun holatini tanlang.")
            return
        conf = None
        if st is Status.DIFFICULT:
            conf = self._selected_confirmation()
            if conf is None:
                QMessageBox.information(
                    self, "ALLOH UCHUN",
                    "Iltimos, majburiyat saqlanganmi yoki yo‘qligini tanlang "
                    "(yoki «Hali aniqlashtirmayman»).",
                )
                return
        self.result_entry = DayEntry(self.day, st, conf, self.note.toPlainText().strip())
        self.accept()

    def _delete(self) -> None:
        if QMessageBox.question(self, "ALLOH UCHUN", "Bu kunning yozuvi o‘chirilsinmi?") == QMessageBox.Yes:
            self.deleted = True
            self.accept()


class MessageDialog(QDialog):
    """Saqlangandan keyin: motivatsion xabar va amaliy sinov."""

    def __init__(self, text: str, source: Optional[str], challenge_text: str, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("ALLOH UCHUN")
        self.setMinimumWidth(480)
        lay = QVBoxLayout(self)
        m = QLabel(f"“{text}”" if source else text)
        m.setWordWrap(True)
        m.setStyleSheet("font-size: 17px; font-style: italic;")
        lay.addWidget(m)
        if source:
            s = QLabel(f"— {source}")
            s.setWordWrap(True)
            s.setObjectName("subtitle")
            lay.addWidget(s)
        lay.addWidget(QLabel("Amaliy sinov:"))
        c = QLabel(challenge_text)
        c.setWordWrap(True)
        c.setStyleSheet("color: #d4af37; font-size: 15px;")
        lay.addWidget(c)
        ok = QPushButton("Yaxshi")
        ok.setObjectName("primary")
        ok.clicked.connect(self.accept)
        lay.addWidget(ok)


class ChallengeDialog(QDialog):
    """Bugungi sinov: bajarish / o'tkazib yuborish / keyinroqqa."""

    def __init__(self, challenge_id: int, current: Optional[ChallengeState], parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Bugungi sinov")
        self.setMinimumWidth(460)
        self.state: Optional[ChallengeState] = None
        lay = QVBoxLayout(self)
        t = QLabel(challenge_by_id(challenge_id) or "")
        t.setWordWrap(True)
        t.setStyleSheet("font-size: 17px; color: #d4af37;")
        lay.addWidget(t)
        if current:
            names = {ChallengeState.DONE: "bajarilgan", ChallengeState.SKIPPED: "o‘tkazib yuborilgan",
                     ChallengeState.LATER: "keyinroqqa saqlangan"}
            lay.addWidget(QLabel(f"Joriy holat: {names[current]}"))
        row = QHBoxLayout()
        for label, st, prim in (("Bajardim", ChallengeState.DONE, True),
                                ("O‘tkazib yuborish", ChallengeState.SKIPPED, False),
                                ("Keyinroqqa saqlash", ChallengeState.LATER, False)):
            b = QPushButton(label)
            if prim:
                b.setObjectName("primary")
            b.clicked.connect(lambda _=False, s=st: self._pick(s))
            row.addWidget(b)
        lay.addLayout(row)
        lay.addWidget(QLabel("Hech qanday jazo yo‘q — sinov faqat yordam uchun."))

    def _pick(self, st: ChallengeState) -> None:
        self.state = st
        self.accept()


class UrgePlanDialog(QDialog):
    """10 daqiqalik qo'llab-quvvatlovchi reja."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("10 daqiqalik reja")
        self.setMinimumSize(540, 560)
        lay = QVBoxLayout(self)
        intro = QLabel("Sen yolg‘iz emassan va bu lahza o‘tadi. Keling, 10 daqiqani birga o‘tkazamiz.")
        intro.setWordWrap(True)
        intro.setStyleSheet("font-size: 16px; color: #d4af37;")
        lay.addWidget(intro)
        area = QScrollArea()
        area.setWidgetResizable(True)
        inner = QWidget()
        il = QVBoxLayout(inner)
        for title, body in URGE_PLAN:
            card = QFrame()
            card.setObjectName("card")
            cl = QVBoxLayout(card)
            h = QLabel(title)
            h.setStyleSheet("color: #d4af37; font-weight: bold;")
            b = QLabel(body)
            b.setWordWrap(True)
            cl.addWidget(h)
            cl.addWidget(b)
            il.addWidget(card)
        il.addStretch(1)
        area.setWidget(inner)
        lay.addWidget(area)
        close = QPushButton("Yopish")
        close.setObjectName("primary")
        close.clicked.connect(self.accept)
        lay.addWidget(close)
