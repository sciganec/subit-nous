import pytest
from subit_nous.core import (
    text_to_subit,
    subit_to_name,
    archetype_color,
    get_mode,
    subit_to_coords,
    MODE_FOR_ARCHETYPE,
    WHO_MAP,
    WHERE_MAP,
    WHEN_MAP,
    WHY_MAP,
)

# ----------------------------------------------------------------------
# Tests for mappings
# ----------------------------------------------------------------------

def test_who_mapping():
    assert WHO_MAP[0b10] == "ME"
    assert WHO_MAP[0b11] == "WE"
    assert WHO_MAP[0b01] == "YOU"
    assert WHO_MAP[0b00] == "THEY"

def test_where_mapping():
    assert WHERE_MAP[0b10] == "EAST"
    assert WHERE_MAP[0b11] == "SOUTH"
    assert WHERE_MAP[0b01] == "WEST"
    assert WHERE_MAP[0b00] == "NORTH"

def test_when_mapping():
    assert WHEN_MAP[0b10] == "SPRING"
    assert WHEN_MAP[0b11] == "SUMMER"
    assert WHEN_MAP[0b01] == "AUTUMN"
    assert WHEN_MAP[0b00] == "WINTER"

def test_why_mapping():
    assert WHY_MAP[0b10] == "LOGOS"
    assert WHY_MAP[0b11] == "ETHOS"
    assert WHY_MAP[0b01] == "PATHOS"
    assert WHY_MAP[0b00] == "THYMOS"

def test_modes_mapping():
    assert MODE_FOR_ARCHETYPE[0b10101010] == "MICRO"
    assert MODE_FOR_ARCHETYPE[0b11111111] == "MACRO"
    assert MODE_FOR_ARCHETYPE[0b01010101] == "MESO"
    assert MODE_FOR_ARCHETYPE[0b00000000] == "META"

# ----------------------------------------------------------------------
# Tests for text_to_subit
# ----------------------------------------------------------------------

def test_text_to_subit_micro():
    text = "I believe the truth is in the east, like a spring morning. Logic proves it."
    subit = text_to_subit(text)
    assert subit == 0b10101010  # 170
    assert get_mode(subit) == "MICRO"

def test_text_to_subit_macro():
    text = "We together build our community in the south during summer. Our ethics guide us."
    subit = text_to_subit(text)
    assert subit == 0b11111111  # 255
    assert get_mode(subit) == "MACRO"

def test_text_to_subit_meso():
    text = "You look to the west in autumn and feel the beauty of change."
    subit = text_to_subit(text)
    assert subit == 0b01010101  # 85
    assert get_mode(subit) == "MESO"

def test_text_to_subit_meta():
    text = "They gather in the north during winter, with strong will and spirit."
    subit = text_to_subit(text)
    assert subit == 0b00000000  # 0
    assert get_mode(subit) == "META"

def test_subit_to_coords():
    assert subit_to_coords(0b10101010) == (0b10, 0b10, 0b10, 0b10)
    assert subit_to_coords(0b11111111) == (0b11, 0b11, 0b11, 0b11)
    assert subit_to_coords(0b01010101) == (0b01, 0b01, 0b01, 0b01)
    assert subit_to_coords(0b00000000) == (0b00, 0b00, 0b00, 0b00)
    assert subit_to_coords(0b10110001) == (0b10, 0b11, 0b00, 0b01)  # ME, SOUTH, WINTER, PATHOS

def test_subit_to_name():
    assert subit_to_name(0b10101010) == "MICRO mode"
    assert subit_to_name(0b11111111) == "MACRO mode"
    assert subit_to_name(0b01010101) == "MESO mode"
    assert subit_to_name(0b00000000) == "META mode"

    # 0b10110001 = ME (10), SOUTH (11), WINTER (00), PATHOS (01)
    subit = 0b10110001
    assert subit_to_name(subit) == "PATHOS_ME_SOUTH_WINTER"

def test_archetype_color():
    assert archetype_color(0b10101010) == '#3498db'  # LOGOS
    assert archetype_color(0b11111111) == '#2ecc71'  # ETHOS
    assert archetype_color(0b01010101) == '#f1c40f'  # PATHOS
    assert archetype_color(0b00000000) == '#9b59b6'  # THYMOS

def test_get_mode():
    assert get_mode(0b10101010) == "MICRO"
    assert get_mode(0b11111111) == "MACRO"
    assert get_mode(0b01010101) == "MESO"
    assert get_mode(0b00000000) == "META"
    assert get_mode(0b10110001) is None