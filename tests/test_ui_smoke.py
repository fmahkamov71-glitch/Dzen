import os
from datetime import date

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication  # noqa: E402

from alloh_uchun.models import Confirmation, DayEntry, Status  # noqa: E402
from alloh_uchun.ui import theme  # noqa: E402
from alloh_uchun.ui.dialogs import EntryDialog  # noqa: E402
from alloh_uchun.ui.main_window import MainWindow  # noqa: E402


@pytest.fixture(scope="module")
def app():
    a = QApplication.instance() or QApplication([])
    a.setStyleSheet(theme.STYLESHEET)
    return a


def test_main_window_title_and_calendar(app, db):
    db.save_entry(DayEntry(date(2024, 2, 29), Status.SUCCESS))
    w = MainWindow(db, today=date(2024, 2, 29))
    assert w.windowTitle() == "ALLOH UCHUN"
    assert w.findChild(type(w.calendar.title), "title").text() == "ALLOH UCHUN"
    assert len(w.calendar.cells) == 29
    w.calendar.go_month(1)
    assert len(w.calendar.cells) == 31
    w.calendar.go_month(-2)
    assert len(w.calendar.cells) == 31 and w.calendar.month == 1
    assert w.stats._values["recorded"].text() == "0"


def test_entry_dialog_requires_confirmation_for_difficult(app, monkeypatch):
    from PySide6.QtWidgets import QMessageBox
    monkeypatch.setattr(QMessageBox, "information", lambda *a, **k: None)
    dlg = EntryDialog(date(2024, 5, 1), None)
    dlg.status_radios[Status.DIFFICULT].setChecked(True)
    dlg._save()
    assert dlg.result_entry is None  # tasdiq tanlanmagan — saqlanmaydi
    dlg.conf_radios[Confirmation.UNDECIDED].setChecked(True)
    dlg._save()
    assert dlg.result_entry.confirmation is Confirmation.UNDECIDED
