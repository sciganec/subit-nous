"""SUBIT-NOUS core: 4 dimensions, 4 transversal modes, 256 archetypes"""

__version__ = "2.0.0"

from enum import Enum
from typing import Dict, Tuple, Optional
import numpy as np

from .subit_algebra import Subit

def text_to_subit_object(text: str) -> Subit:
    return Subit(text_to_subit(text))

# ============ ВИМІРИ (ENUM) ============

class Who(Enum):
    ME = 0b10
    WE = 0b11
    YOU = 0b01
    THEY = 0b00

class Where(Enum):
    EAST = 0b10
    SOUTH = 0b11
    WEST = 0b01
    NORTH = 0b00

class When(Enum):
    SPRING = 0b10
    SUMMER = 0b11
    AUTUMN = 0b01
    WINTER = 0b00

class Why(Enum):
    LOGOS = 0b10
    ETHOS = 0b11
    PATHOS = 0b01
    THYMOS = 0b00

# ============ МАПІНГИ ============

WHO_MAP = {0b10: "ME", 0b11: "WE", 0b01: "YOU", 0b00: "THEY"}
WHERE_MAP = {0b10: "EAST", 0b11: "SOUTH", 0b01: "WEST", 0b00: "NORTH"}
WHEN_MAP = {0b10: "SPRING", 0b11: "SUMMER", 0b01: "AUTUMN", 0b00: "WINTER"}
WHY_MAP = {0b10: "LOGOS", 0b11: "ETHOS", 0b01: "PATHOS", 0b00: "THYMOS"}

# transversal modes for the four corner archetypes
MODE_FOR_ARCHETYPE = {
    0b10101010: "MICRO",   # 170
    0b11111111: "MACRO",   # 255
    0b01010101: "MESO",    # 85
    0b00000000: "META",    # 0
}

# Мапінг назв модусів до бітових значень (MODE axis)
MODE_VALUES = {
    "STATE": 0b10,   # LOGOS
    "VALUE": 0b11,   # ETHOS
    "FORM": 0b01,    # PATHOS
    "FORCE": 0b00,   # THYMOS
}

MODE_NAMES = {v: k for k, v in MODE_VALUES.items()}

# ============ МАРКЕРИ ============

MARKERS = {
    'WHO': {
        0b10: ['i', 'me', 'my', 'mine', 'myself'],
        0b11: ['we', 'us', 'our', 'ours', 'ourselves'],
        0b01: ['you', 'your', 'yours', 'yourself'],
        0b00: ['they', 'them', 'their', 'theirs', 'he', 'she', 'it', 'its'],
    },
    'WHERE': {
        0b10: ['east', 'eastern', 'right', 'forward', 'future', 'advance'],
        0b11: ['south', 'southern', 'down', 'downward', 'growth', 'expand'],
        0b01: ['west', 'western', 'left', 'back', 'past', 'retreat'],
        0b00: ['north', 'northern', 'up', 'center', 'stable', 'core'],
    },
    'WHEN': {
        0b10: ['spring', 'start', 'begin', 'birth', 'dawn', 'new', 'initiate'],
        0b11: ['summer', 'peak', 'mid', 'height', 'flourish', 'mature'],
        0b01: ['autumn', 'fall', 'decay', 'decline', 'evening', 'late', 'reflect'],
        0b00: ['winter', 'end', 'death', 'night', 'final', 'still'],
    },
    'WHY': {
        0b10: ['logic', 'logical', 'reason', 'code', 'data', 'proof', 'science', 'math', 'algorithm', 'system', 'structure'],
        0b11: ['ethics', 'ethos', 'moral', 'trust', 'community', 'tradition', 'virtue', 'justice', 'harmony'],
        0b01: ['pathos', 'emotion', 'beauty', 'art', 'love', 'joy', 'sorrow', 'passion', 'aesthetic', 'feeling'],
        0b00: ['thymos', 'spirit', 'will', 'courage', 'power', 'control', 'ambition', 'fight', 'dominate'],
    }
}

def _detect_dimension(text: str, dim_markers: Dict[int, list], dim_name: str = None) -> int:
    """Повертає 2-бітне значення для одного виміру з підвищеною вагою для займенників."""
    text_lower = text.lower()
    scores = {bits: 0 for bits in dim_markers}
    for bits, words in dim_markers.items():
        for w in words:
            if w in text_lower:
                weight = len(w)
                # Підвищена вага для ключових займенників WHO
                if dim_name == 'WHO':
                    if bits == 0b10 and w in ('i', 'me', 'my', 'mine'):
                        weight *= 5
                    elif bits == 0b11 and w in ('we', 'us', 'our', 'ours'):
                        weight *= 5
                    elif bits == 0b01 and w in ('you', 'your', 'yours'):
                        weight *= 5
                    elif bits == 0b00 and w in ('they', 'them', 'their', 'theirs'):
                        weight *= 5
                scores[bits] += weight
    if max(scores.values()) == 0:
        return 0b10  # default MICRO
    return max(scores, key=scores.get)

def text_to_subit(text: str, chunk_size: int = 1000) -> int:
    """Текст → 8-бітний архетип (0-255)."""
    sample = text[:chunk_size].lower()
    who_bits = _detect_dimension(sample, MARKERS['WHO'], 'WHO')
    where_bits = _detect_dimension(sample, MARKERS['WHERE'], 'WHERE')
    when_bits = _detect_dimension(sample, MARKERS['WHEN'], 'WHEN')
    why_bits = _detect_dimension(sample, MARKERS['WHY'], 'WHY')
    return (who_bits << 6) | (where_bits << 4) | (when_bits << 2) | why_bits

def subit_to_name(archetype: int) -> str:
    """Архетип → людинозрозуміла назва."""
    if archetype in MODE_FOR_ARCHETYPE:
        return f"{MODE_FOR_ARCHETYPE[archetype]} mode"
    who = WHO_MAP[(archetype >> 6) & 0b11]
    where = WHERE_MAP[(archetype >> 4) & 0b11]
    when = WHEN_MAP[(archetype >> 2) & 0b11]
    why = WHY_MAP[archetype & 0b11]
    return f"{why}_{who}_{where}_{when}"

def archetype_color(archetype: int) -> str:
    """Колір архетипу на основі WHY."""
    why = archetype & 0b11
    return {0b10: '#3498db', 0b11: '#2ecc71', 0b01: '#f1c40f', 0b00: '#9b59b6'}[why]

def get_mode(archetype: int) -> Optional[str]:
    """Повертає модус (MICRO/MACRO/MESO/META) для крайових архетипів, інакше None."""
    return MODE_FOR_ARCHETYPE.get(archetype)

def subit_to_coords(archetype: int) -> Tuple[int, int, int, int]:
    """Розкладає архетип на координати (who, where, when, why)."""
    return (
        (archetype >> 6) & 0b11,
        (archetype >> 4) & 0b11,
        (archetype >> 2) & 0b11,
        archetype & 0b11,
    )

def _dimension_soft(text: str, dim_markers: Dict[int, list]) -> tuple:
    """
    Повертає два soft-біти для одного виміру (наприклад, WHO).
    Значення в [-1,1]: позитивне → біт тяжіє до 1, негативне → до 0.
    """
    text_lower = text.lower()
    scores = {bits: 0 for bits in dim_markers}
    for bits, words in dim_markers.items():
        for w in words:
            if w in text_lower:
                scores[bits] += len(w)
    total = sum(scores.values())
    if total == 0:
        return (0.0, 0.0)
    # Нормалізуємо до [0,1]
    probs = {bits: scores[bits] / total for bits in dim_markers}
    # Для двох бітів (b1, b2) де:
    # bits = (b1<<1) | b2 ? Ні. У нас bits: 10,11,01,00.
    # Нехай b1 – старший біт (2¹), b2 – молодший (2⁰).
    # Тоді:
    # 10: b1=1, b2=0
    # 11: b1=1, b2=1
    # 01: b1=0, b2=1
    # 00: b1=0, b2=0
    # Ймовірність b1=1 = P(10)+P(11)
    # Ймовірність b2=1 = P(11)+P(01)
    p_b1 = probs.get(0b10, 0) + probs.get(0b11, 0)
    p_b2 = probs.get(0b11, 0) + probs.get(0b01, 0)
    # Перетворюємо [0,1] → [-1,1] через 2*p-1
    soft_b1 = 2 * p_b1 - 1
    soft_b2 = 2 * p_b2 - 1
    return (soft_b1, soft_b2)

def text_to_soft(text: str, chunk_size: int = 1000) -> np.ndarray:
    """
    Перетворює текст у 8-вимірний soft-вектор (значення в [-1,1]).
    Порядок бітів: [WHO_b1, WHO_b2, WHERE_b1, WHERE_b2, WHEN_b1, WHEN_b2, WHY_b1, WHY_b2]
    """
    sample = text[:chunk_size].lower()
    soft_parts = []
    for dim in ['WHO', 'WHERE', 'WHEN', 'WHY']:
        b1, b2 = _dimension_soft(sample, MARKERS[dim])
        soft_parts.extend([b1, b2])
    return np.array(soft_parts, dtype=np.float32)

def soft_to_hard(soft_vec: np.ndarray) -> int:
    """
    Перетворює soft-вектор у жорсткий архетип (поріг 0).
    """
    bits = 0
    for i, val in enumerate(soft_vec):
        if val > 0:
            bits |= (1 << (7 - i))   # старший біт – індекс 0
    return bits

from .subit_algebra import Subit

def text_to_subit_object(text: str, chunk_size: int = 1000) -> Subit:
    """Повертає об'єкт Subit для заданого тексту."""
    return Subit(text_to_subit(text, chunk_size))

def soft_to_subit_object(soft_vec: np.ndarray) -> Subit:
    """Перетворює soft-вектор у Subit (поріг 0)."""
    bits = soft_to_hard(soft_vec)
    return Subit(bits)