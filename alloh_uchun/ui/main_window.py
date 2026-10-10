"""Asosiy oyna."""
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

from PySide6.QtWidgets import (
    QComboBox, QFileDialog, QFrame, QHBoxLayout, QLabel, QMainWindow, QMessageBox,
    QPushButton, QVBoxLayout, QWidget,
)

from .. import APP_NAME, calendar_logic as cal
from ..database import Database, RestoreError
from ..models import ChallengeState
from ..motivation import daily_challenge_id, pick_message, random_challenge
from ..stats import current_streak, longest_streak, month_stats
from .calendar_widget import CalendarWidget
from .dialogs import ChallengeDialog, EntryDialog, MessageDialog, UrgePlanDialog
from .header import Header
from .stats_panel import StatsPanel


class MainWindow(QMainWindow):
    def __init__(self, db: Database, today: date | None = None) -> None:
        super().__init__()
        self.db = db
        self.today = today or date.today()
        self.setWindowTitle(APP_NAME)
        self.resize(980, 860)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 12)
        root.addWidget(Header())

        body = QVBoxLayout()
        body.setContentsMargins(20, 12, 20, 0)
        root.addLayout(body)

        self.stats = StatsPanel()
        body.addWidget(self.stats)

        card = QFrame()
        card.setObjectName("card")
        cl = QVBoxLayout(card)
        self.calendar = CalendarWidget(self.today)
        self.calendar.dateSelected.connect(self.edit_day)
        self.calendar.monthChanged.connect(lambda *_: self.refresh())
        cl.addWidget(self.calendar)
        legend = QLabel("🟩 Muvaffaqiyat   🟧 Qiyin kun   🟥 Maqsad buzildi   ▫ Yozilmagan (yozilmagan kun muvaffaqiyat hisoblanmaydi)")
        legend.setObjectName("statName")
        cl.addWidget(legend)
        body.addWidget(card, 1)

        hist = QHBoxLayout()
        hist.addWidget(QLabel("Oylar tarixi:"))
        self.history = QComboBox()
        self.history.activated.connect(self._history_picked)
        hist.addWidget(self.history, 1)
        body.addLayout(hist)

        row = QHBoxLayout()
        self.challenge_btn = QPushButton("Bugungi sinov")
        self.challenge_btn.clicked.connect(self.open_challenge)
        self.backup_btn = QPushButton("Zaxira nusxa")
        self.backup_btn.clicked.connect(self.backup)
        self.restore_btn = QPushButton("Tiklash")
        self.restore_btn.clicked.connect(self.restore)
        self.wipe_btn = QPushButton("Barcha yozuvlarni o‘chirish")
        self.wipe_btn.clicked.connect(self.wipe_all)
        for b in (self.challenge_btn, self.backup_btn, self.restore_btn, self.wipe_btn):
            row.addWidget(b)
        body.addLayout(row)

        self.urge_btn = QPushButton("HOZIR O‘ZIMNI NAZORAT QILISHIM KERAK")
        self.urge_btn.setObjectName("urge")
        self.urge_btn.clicked.connect(lambda: UrgePlanDialog(self).exec())
        body.addWidget(self.urge_btn)

        privacy = QLabel(f"🔒 Ma’lumotlar faqat shu kompyuterda saqlanadi: {db.path}")
        privacy.setObjectName("statName")
        privacy.setWordWrap(True)
        body.addWidget(privacy)

        self.refresh()

    # ---- yangilash -------------------------------------------------------
    def refresh(self) -> None:
        y, m = self.calendar.year, self.calendar.month
        entries = self.db.entries_for_month(y, m)
        self.calendar.set_entries(entries)
        all_entries = self.db.all_entries()
        self.stats.update_stats(
            month_stats(all_entries, y, m),
            current_streak(all_entries, self.today),
            longest_streak(all_entries),
        )
        self.history.clear()
        for yy, mm in self.db.months_with_entries():
            self.history.addItem(cal.month_title(yy, mm), (yy, mm))

    def _history_picked(self, idx: int) -> None:
        data = self.history.itemData(idx)
        if data:
            self.calendar.year, self.calendar.month = data
            self.refresh()

    # ---- kun yozuvi ------------------------------------------------------
    def edit_day(self, d: date) -> None:
        if d > self.today:
            QMessageBox.information(self, APP_NAME, "Kelajakdagi kunga yozuv kiritib bo‘lmaydi.")
            return
        existing = self.db.get_entry(d)
        dlg = EntryDialog(d, existing, self)
        if not dlg.exec():
            return
        if dlg.deleted:
            self.db.delete_entry(d)
            self.refresh()
            return
        entry = dlg.result_entry
        self.db.save_entry(entry)  # darhol saqlanadi
        self.refresh()
        text, source = pick_message(entry.status)
        _, challenge = random_challenge()
        MessageDialog(text, source, challenge, self).exec()

    # ---- sinov -----------------------------------------------------------
    def open_challenge(self) -> None:
        cid = daily_challenge_id(self.today)
        logged = self.db.get_challenge(self.today)
        dlg = ChallengeDialog(cid, logged[1] if logged else None, self)
        if dlg.exec() and dlg.state:
            self.db.set_challenge(self.today, cid, dlg.state)

    # ---- zaxira / tiklash / o'chirish -----------------------------------
    def backup(self) -> None:
        default = str(Path.home() / f"ALLOH_UCHUN_zaxira_{datetime.now():%Y%m%d_%H%M}.db")
        path, _ = QFileDialog.getSaveFileName(self, "Zaxira nusxa", default, "SQLite (*.db)")
        if path:
            try:
                self.db.backup_to(path)
                QMessageBox.information(self, APP_NAME, f"Zaxira nusxa saqlandi:\n{path}")
            except Exception as exc:  # noqa: BLE001
                QMessageBox.critical(self, APP_NAME, f"Zaxira yaratilmadi: {exc}")

    def restore(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Zaxiradan tiklash", str(Path.home()), "SQLite (*.db)")
        if not path:
            return
        if QMessageBox.question(
            self, APP_NAME, "Joriy yozuvlar zaxiradagi ma’lumotlar bilan almashtiriladi. Davom etasizmi?"
        ) != QMessageBox.Yes:
            return
        try:
            self.db.restore_from(path)
        except RestoreError as exc:
            QMessageBox.critical(self, APP_NAME, str(exc))
            return
        self.refresh()
        QMessageBox.information(self, APP_NAME, "Ma’lumotlar tiklandi.")

    def wipe_all(self) -> None:
        box = QMessageBox(QMessageBox.Warning, APP_NAME,
                          "Barcha yozuvlar va izohlar butunlay o‘chiriladi. Bu amalni qaytarib bo‘lmaydi.\n"
                          "Avval zaxira nusxa olishni tavsiya qilamiz. Davom etasizmi?",
                          QMessageBox.NoButton, self)
        yes = box.addButton("Ha, hammasini o‘chir", QMessageBox.DestructiveRole)
        box.addButton("Bekor qilish", QMessageBox.RejectRole)
        box.exec()
        if box.clickedButton() is yes:
            self.db.delete_all()
            self.refresh()
