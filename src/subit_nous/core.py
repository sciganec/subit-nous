"""SUBIT-NOUS core: 4 dimensions, 4 transversal modes, 256 archetypes"""

__version__ = "2.0.0"

from enum import Enum
from typing import Dict, Tuple, Optional

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