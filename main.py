"""ALLOH UCHUN — ilovaning kirish nuqtasi."""
import sys

from PySide6.QtWidgets import QApplication

from alloh_uchun import APP_NAME
from alloh_uchun.database import Database
from alloh_uchun.paths import default_db_path
from alloh_uchun.ui import theme
from alloh_uchun.ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyleSheet(theme.STYLESHEET)
    db = Database(default_db_path())
    win = MainWindow(db)
    win.show()
    code = app.exec()
    db.close()
    return code


if __name__ == "__main__":
    sys.exit(main())
