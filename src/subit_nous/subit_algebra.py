"""SUBIT Algebra Core – формальна алгебра над (ℤ₂)⁸"""

from dataclasses import dataclass
from typing import Tuple, Literal

Axis = Literal["WHO", "WHERE", "WHEN", "MODE"]

# Мапінг осей до зсуву бітів
AXIS_SHIFT = {"WHO": 6, "WHERE": 4, "WHEN": 2, "MODE": 0}


@dataclass
class Subit:
    bits: int  # 0..255

    def __post_init__(self):
        if not (0 <= self.bits < 256):
            raise ValueError(f"Subit bits must be 0..255, got {self.bits}")

    # ------------------------------------------------------------------
    # Конструктори
    # ------------------------------------------------------------------
    @classmethod
    def from_coords(cls, who: int, where: int, when: int, mode: int) -> "Subit":
        """Створює Subit з 4-х координат (кожна 0..3)."""
        return cls((who << 6) | (where << 4) | (when << 2) | mode)

    @classmethod
    def from_byte(cls, byte: int) -> "Subit":
        return cls(byte)

    # ------------------------------------------------------------------
    # Операції
    # ------------------------------------------------------------------
    def xor(self, other: "Subit") -> "Subit":
        """Побітове XOR – перехід між станами."""
        return Subit(self.bits ^ other.bits)

    def distance(self, other: "Subit") -> int:
        """Відстань Геммінга – кількість різних бітів."""
        return (self.bits ^ other.bits).bit_count()

    def project(self, axis: Axis) -> int:
        """Проекція на вісь (повертає 0..3)."""
        shift = AXIS_SHIFT[axis]
        return (self.bits >> shift) & 0b11

    def replace(self, axis: Axis, value: int) -> "Subit":
        """Заміна значення на заданій осі."""
        shift = AXIS_SHIFT[axis]
        mask = 0b11 << shift
        new_bits = (self.bits & ~mask) | ((value & 0b11) << shift)
        return Subit(new_bits)

    def invert(self) -> "Subit":
        """Повна бітова інверсія (протилежний архетип)."""
        return Subit(self.bits ^ 0xFF)

    # ------------------------------------------------------------------
    # Перетворення
    # ------------------------------------------------------------------
    def to_tuple(self) -> Tuple[int, int, int, int]:
        """Повертає (who, where, when, mode)."""
        return (
            (self.bits >> 6) & 0b11,
            (self.bits >> 4) & 0b11,
            (self.bits >> 2) & 0b11,
            self.bits & 0b11,
        )

    def to_human(self) -> str:
        """Людинозрозуміла назва (використовує core.subit_to_name)."""
        from .core import subit_to_name  # уникнення циркулярного імпорту

        return subit_to_name(self.bits)

    def __repr__(self) -> str:
        return f"Subit(bits={self.bits:08b}, human='{self.to_human()}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Subit):
            return False
        return self.bits == other.bits