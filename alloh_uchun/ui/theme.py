"""Qora–oltin–to'q zumrad rang sxemasi va stillar."""
BLACK = "#0b0d0c"
PANEL = "#121815"
EMERALD_DARK = "#0d3b2e"
EMERALD = "#14624a"
GOLD = "#d4af37"
GOLD_SOFT = "#a98a2a"
TEXT = "#efe6cc"
MUTED = "#9fb0a6"

COL_SUCCESS = "#1e8f5f"
COL_DIFFICULT = "#c9922b"
COL_SETBACK = "#a13b3b"

STYLESHEET = f"""
QWidget {{ background: {BLACK}; color: {TEXT}; font-family: 'Segoe UI', 'Georgia', sans-serif; font-size: 14px; }}
QLabel#title {{ color: {GOLD}; font-family: 'Georgia', serif; font-size: 34px; font-weight: bold; letter-spacing: 8px; }}
QLabel#subtitle {{ color: {MUTED}; font-style: italic; font-size: 14px; }}
QLabel#monthTitle {{ color: {GOLD}; font-family: 'Georgia', serif; font-size: 22px; }}
QLabel#statValue {{ color: {GOLD}; font-size: 24px; font-weight: bold; }}
QLabel#statName {{ color: {MUTED}; font-size: 12px; }}
QFrame#card {{ background: {PANEL}; border: 1px solid {EMERALD}; border-radius: 10px; }}
QFrame#card QLabel {{ background: transparent; }}
QPushButton {{ background: {EMERALD_DARK}; color: {TEXT}; border: 1px solid {GOLD_SOFT}; border-radius: 8px; padding: 8px 14px; }}
QPushButton:hover {{ background: {EMERALD}; border-color: {GOLD}; }}
QPushButton#primary {{ background: {GOLD}; color: {BLACK}; font-weight: bold; border: none; }}
QPushButton#primary:hover {{ background: #e6c34f; }}
QPushButton#urge {{ background: {EMERALD}; color: {TEXT}; font-weight: bold; border: 2px solid {GOLD}; padding: 12px; }}
QPushButton#urge:hover {{ background: #1b7a5c; }}
QPushButton#dayCell {{ border-radius: 6px; padding: 6px; font-size: 15px; background: {PANEL}; border: 1px solid #23302a; }}
QPushButton#dayCell:hover {{ border-color: {GOLD}; }}
QTextEdit, QPlainTextEdit, QComboBox {{ background: {PANEL}; border: 1px solid {EMERALD}; border-radius: 6px; padding: 6px; }}
QRadioButton {{ spacing: 8px; padding: 4px; background: transparent; }}
QDialog {{ background: {BLACK}; }}
QMessageBox {{ background: {BLACK}; }}
QScrollArea {{ border: none; }}
"""
