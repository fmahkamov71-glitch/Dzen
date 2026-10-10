"""Ma'lumot modellari."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


class Status(str, Enum):
    SUCCESS = "success"
    DIFFICULT = "difficult"
    SETBACK = "setback"

    @property
    def label(self) -> str:
        return STATUS_LABELS[self]


class Confirmation(str, Enum):
    YES = "yes"
    NO = "no"
    UNDECIDED = "undecided"

    @property
    def label(self) -> str:
        return CONFIRMATION_LABELS[self]


STATUS_LABELS = {
    Status.SUCCESS: "Muvaffaqiyat",
    Status.DIFFICULT: "Qiyin kun",
    Status.SETBACK: "Maqsad buzildi",
}

CONFIRMATION_LABELS = {
    Confirmation.YES: "Ha",
    Confirmation.NO: "Yo‘q",
    Confirmation.UNDECIDED: "Hali aniqlashtirmayman",
}


class ChallengeState(str, Enum):
    DONE = "done"
    SKIPPED = "skipped"
    LATER = "later"


@dataclass(frozen=True)
class DayEntry:
    day: date
    status: Status
    confirmation: Optional[Confirmation] = None  # faqat "Qiyin kun" uchun
    note: str = ""

    def __post_init__(self) -> None:
        if self.status is not Status.DIFFICULT and self.confirmation is not None:
            raise ValueError("Tasdiq faqat 'Qiyin kun' holati uchun saqlanadi.")

    @property
    def is_confirmed_success(self) -> bool:
        """Faqat aniq tasdiqlangan muvaffaqiyat (qoidalar README'da)."""
        return self.status is Status.SUCCESS or (
            self.status is Status.DIFFICULT and self.confirmation is Confirmation.YES
        )
