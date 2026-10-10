"""Sarlavha: ALLOH UCHUN + kichik islomiy geometrik naqsh."""
from __future__ import annotations

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from .. import APP_NAME, SUBTITLE
from . import theme


def draw_star(p: QPainter, cx: float, cy: float, r: float) -> None:
    """Sakkiz qirrali yulduz (ikki burilgan kvadrat)."""
    import math
    for rot in (0, math.pi / 4):
        pts = [QPointF(cx + r * math.cos(rot + math.pi / 4 + k * math.pi / 2),
                       cy + r * math.sin(rot + math.pi / 4 + k * math.pi / 2)) for k in range(4)]
        for i in range(4):
            p.drawLine(pts[i], pts[(i + 1) % 4])


class Header(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumHeight(130)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 18, 20, 14)
        self.title = QLabel(APP_NAME)
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        self.subtitle = QLabel(SUBTITLE)
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.title)
        lay.addWidget(self.subtitle)
        for w in (self.title, self.subtitle):
            w.setStyleSheet("background: transparent;")

    def paintEvent(self, _event) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), QColor(theme.BLACK))
        gold = QColor(theme.GOLD)
        gold.setAlpha(60)
        p.setPen(QPen(gold, 1.2))
        step = 44
        for ix in range(-1, self.width() // step + 2):
            for iy in range(0, self.height() // step + 2):
                draw_star(p, ix * step + (step / 2 if iy % 2 else 0), iy * step, 16)
        line = QColor(theme.GOLD)
        p.setPen(QPen(line, 2))
        p.drawLine(0, self.height() - 1, self.width(), self.height() - 1)
        p.end()
