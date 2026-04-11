"""SUBIT Algebra Core – формальна алгебра над (ℤ₂)⁸ згідно SUBIT v3.0"""

from dataclasses import dataclass
from typing import Tuple, Literal, Dict, Optional

Axis = Literal["WHO", "WHERE", "WHEN", "MODE"]
AXIS_SHIFT = {"WHO": 6, "WHERE": 4, "WHEN": 2, "MODE": 0}
AXIS_ORDER = ["WHO", "WHERE", "WHEN", "MODE"]

# Дзеркальна симетрія для 2-бітних значень (ME↔THEY, WE↔YOU, ...)
_FLIP_MAP = {0b10: 0b00, 0b00: 0b10, 0b11: 0b01, 0b01: 0b11}


@dataclass
class Subit:
    bits: int  # 0..255

    def __post_init__(self):
        if not (0 <= self.bits < 256):
            raise ValueError(f"Subit bits must be 0..255, got {self.bits}")

    # ------------------------------------------------------------------
    # Магічні методи
    # ------------------------------------------------------------------
    def __xor__(self, other: "Subit") -> "Subit":
        """Bitwise XOR operator."""
        return Subit(self.bits ^ other.bits)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Subit):
            return False
        return self.bits == other.bits

    def __repr__(self) -> str:
        return f"Subit(bits={self.bits:08b}, human='{self.to_human()}')"

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

    @classmethod
    def from_text(cls, text: str, chunk_size: int = 1000) -> "Subit":
        """Encode text into Subit state using marker-based detection."""
        from .core import text_to_subit
        return cls(text_to_subit(text, chunk_size))

    # ------------------------------------------------------------------
    # Базові операції
    # ------------------------------------------------------------------
    def xor(self, other: "Subit") -> "Subit":
        """Alias for ^ operator."""
        return self ^ other

    def distance(self, other: "Subit") -> int:
        """Hamming distance – кількість різних бітів."""
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
    # Нові операції v3.0
    # ------------------------------------------------------------------
    def flip_axis(self, axis: Axis) -> "Subit":
        """Дзеркальне відображення осі (10↔00, 11↔01)."""
        shift = AXIS_SHIFT[axis]
        val = (self.bits >> shift) & 0b11
        flipped = _FLIP_MAP[val]
        return self.replace(axis, flipped)

    def flip_bit(self, pos: int) -> "Subit":
        """Інвертує один біт (0 – наймолодший)."""
        if not 0 <= pos < 8:
            raise ValueError(f"Bit position must be 0..7, got {pos}")
        return Subit(self.bits ^ (1 << pos))

    def permute_axes(self, perm: Tuple[int, int, int, int]) -> "Subit":
        """
        Перестановка осей. perm – кортеж (new_index_for_WHO, ...)
        Наприклад, (1,0,2,3) поміняє WHO і WHERE.
        """
        if len(perm) != 4 or not all(0 <= p < 4 for p in perm):
            raise ValueError("perm must be a tuple of 4 integers in 0..3")
        vals = [self.project(ax) for ax in AXIS_ORDER]
        new_vals = [vals[perm[i]] for i in range(4)]
        bits = 0
        for i, ax in enumerate(AXIS_ORDER):
            bits |= (new_vals[i] << AXIS_SHIFT[ax])
        return Subit(bits)

    # ------------------------------------------------------------------
    # LLM Control (PHASE 2)
    # ------------------------------------------------------------------
    def apply_to_prompt(self, prompt: str, model: str = "llama3.2:3b") -> str:
        """
        Apply Subit state to control LLM generation.
        Requires Ollama running.
        """
        import ollama
        
        mode = self.project("MODE")
        mode_names = {2: "STATE", 3: "VALUE", 1: "FORM", 0: "FORCE"}
        mode_name = mode_names[mode]
        
        who = self.project("WHO")
        who_names = {2: "ME", 3: "WE", 1: "YOU", 0: "THEY"}
        who_name = who_names[who]
        
        system = f"""You are an AI assistant that responds in a specific style:
- MODE = {mode_name}: {self._get_mode_description(mode_name)}
- WHO = {who_name}: {self._get_who_description(who_name)}
Respond naturally but follow these style guidelines."""
        
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            options={"temperature": 0.7}
        )
        return response['message']['content']

    def _get_mode_description(self, mode: str) -> str:
        descriptions = {
            "STATE": "logical, factual, structured, analytical",
            "VALUE": "ethical, trustworthy, communal, harmonious",
            "FORM": "aesthetic, emotional, artistic, beautiful",
            "FORCE": "willful, powerful, controlling, ambitious",
        }
        return descriptions.get(mode, "")

    def _get_who_description(self, who: str) -> str:
        descriptions = {
            "ME": "first-person individual perspective",
            "WE": "collective group perspective",
            "YOU": "second-person dialogical perspective",
            "THEY": "third-person systemic perspective",
        }
        return descriptions.get(who, "")

    # ------------------------------------------------------------------
    # Інваріанти
    # ------------------------------------------------------------------
    def parity(self) -> int:
        """Сума бітів mod 2."""
        return bin(self.bits).count('1') % 2

    def axis_balance(self) -> Dict[str, float]:
        """Відстані між усіма парами осей (від 0 до 4)."""
        vals = [self.project(ax) for ax in AXIS_ORDER]
        balance = {}
        for i, ax1 in enumerate(AXIS_ORDER):
            for j, ax2 in enumerate(AXIS_ORDER):
                if i < j:
                    v1 = (vals[i] >> 1, vals[i] & 1)
                    v2 = (vals[j] >> 1, vals[j] & 1)
                    dist = abs(v1[0] - v2[0]) + abs(v1[1] - v2[1])
                    balance[f"{ax1}-{ax2}"] = dist
        return balance

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
        """Людинозрозуміла назва."""
        # Canonical states
        if self.bits == 0b10101010:
            return "MICRO mode"
        if self.bits == 0b11111111:
            return "MACRO mode"
        if self.bits == 0b01010101:
            return "MESO mode"
        if self.bits == 0b00000000:
            return "META mode"
        # Mixed states
        who = ["ME", "WE", "YOU", "THEY"][(self.bits >> 6) & 0b11]
        where = ["EAST", "SOUTH", "WEST", "NORTH"][(self.bits >> 4) & 0b11]
        when = ["SPRING", "SUMMER", "AUTUMN", "WINTER"][(self.bits >> 2) & 0b11]
        why = ["LOGOS", "ETHOS", "PATHOS", "THYMOS"][self.bits & 0b11]
        return f"{why}_{who}_{where}_{when}"