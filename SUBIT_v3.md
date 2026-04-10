# SUBIT v3.0 — Formal Specification

**Status:** Stable  
**Version:** 3.0  
**Type:** Algebraic Semantic Coordinate System  
**Date:** 2026-04-10  

---

## 1. Overview

SUBIT defines a **discrete coordinate space of meaning** consisting of four orthogonal axes:

```
SUBIT = WHO × WHERE × WHEN × MODE
```

Each axis has 4 values encoded with 2 bits.

---

## 2. Algebraic Structure

### 2.1 Base Space

```
SUBIT = (ℤ₂)⁸
```

where ℤ₂ = {0,1}

### 2.2 Element

```
S = (b₁, b₂, b₃, b₄, b₅, b₆, b₇, b₈)
```

### 2.3 Axis Decomposition

```
WHO   = (b₁, b₂)
WHERE = (b₃, b₄)
WHEN  = (b₅, b₆)
MODE  = (b₇, b₈)
```

---

## 3. Axis Definitions

### 3.1 WHO (Subject)

| Value | Binary | Interpretation |
|-------|--------|----------------|
| ME    | 10     | individual, self |
| WE    | 11     | collective, group |
| YOU   | 01     | dialogical, other |
| THEY  | 00     | systemic, external |

### 3.2 WHERE (Space)

| Value | Binary | Interpretation |
|-------|--------|----------------|
| EAST  | 10     | future, progress, right |
| SOUTH | 11     | growth, action, down |
| WEST  | 01     | past, reflection, left |
| NORTH | 00     | center, stability, up |

### 3.3 WHEN (Time)

| Value  | Binary | Interpretation |
|--------|--------|----------------|
| SPRING | 10     | beginning, birth, initiation |
| SUMMER | 11     | peak, growth, flourishing |
| AUTUMN | 01     | decline, reflection, transformation |
| WINTER | 00     | end, death, stillness |

### 3.4 MODE (Core)

| Value | Binary | Technical Name | Interface Name |
|-------|--------|----------------|----------------|
| STATE | 10     | LOGOS          | logical, factual, structured |
| VALUE | 11     | ETHOS          | ethical, trustworthy, communal |
| FORM  | 01     | PATHOS         | aesthetic, emotional, artistic |
| FORCE | 00     | THYMOS         | willful, powerful, ambitious |

---

## 4. Algebra

### 4.1 Operation: XOR

```
S₁ ⊕ S₂ = bitwise XOR
```

**Properties:**
- Commutative: `S₁ ⊕ S₂ = S₂ ⊕ S₁`
- Associative: `(S₁ ⊕ S₂) ⊕ S₃ = S₁ ⊕ (S₂ ⊕ S₃)`
- Identity: `S ⊕ 00000000 = S`
- Inverse: `S ⊕ S = 00000000`

### 4.2 Metric: Hamming Distance

```
d(S₁, S₂) = Σ |bᵢ¹ - bᵢ²|
```

Number of differing bits between two states.

### 4.3 Projection

```
π_axis(S) → 2-bit value
```

Extracts the value of a specific axis.

### 4.4 Replacement

```
replace(S, axis, value) → S'
```

Creates a new state by replacing one axis value.

### 4.5 Complement (Inversion)

```
¬S = S ⊕ 11111111
```

Bitwise NOT – the semantic opposite.

### 4.6 Axis Flip

```
flip_axis(S, axis) → S'
```

Mirror reflection of an axis (10↔00, 11↔01).

### 4.7 Bit Flip

```
flip_bit(S, i) → S'
```

Inverts a single bit at position i (0..7).

### 4.8 Axis Permutation

```
permute_axes(S, σ) → S' where σ ∈ S₄
```

Reorders the four axes according to permutation σ.

---

## 5. Geometry

### 5.1 Embedding in ℝ⁸

Map binary values to real numbers:

```
0 → -1
1 → +1
```

```
S ∈ {-1, +1}⁸ ⊂ ℝ⁸
```

### 5.2 Euclidean Distance

```
||S₁ - S₂|| = √(Σ (vᵢ¹ - vᵢ²)²)
```

### 5.3 Cosine Similarity

```
sim(S₁, S₂) = (S₁ · S₂) / 8
```

Range: -1 (opposite) to +1 (identical).

### 5.4 Continuous Extension (Soft SUBIT)

```
S ∈ ℝ⁸
S ∈ [0,1]⁸  (probability interpretation)
axis ∈ Δ⁴   (simplex for each axis)
```

---

## 6. Canonical States (Diagonal Elements)

### 6.1 Definition

| Name  | Binary          | Value |
|-------|-----------------|-------|
| MICRO | (10,10,10,10)   | 170   |
| MACRO | (11,11,11,11)   | 255   |
| MESO  | (01,01,01,01)   | 85    |
| META  | (00,00,00,00)   | 0     |

### 6.2 Interpretation

| State | Meaning |
|-------|---------|
| MICRO | local, generative, individual |
| MACRO | collective, stabilizing, synchronous |
| MESO  | relational, expressive, dialogical |
| META  | structural, abstract, foundational |

---

## 7. Invariants

### 7.1 Bit Parity

```
parity(S) = (Σ bᵢ) mod 2
```

### 7.2 Axis Balance

```
balance(S) = distance between axes
```

Measures how different the four axis values are.

---

## 8. Operations Summary

| Operation | Input | Output | Category |
|-----------|-------|--------|----------|
| XOR | S₁, S₂ | S₃ | Algebraic |
| distance | S₁, S₂ | ℕ | Metric |
| project | S, axis | {0,1,2,3} | Projection |
| replace | S, axis, value | S' | Transformation |
| invert | S | S' | Transformation |
| flip_axis | S, axis | S' | Symmetry |
| flip_bit | S, i | S' | Symmetry |
| permute_axes | S, σ | S' | Symmetry |
| embed | S | ℝ⁸ | Geometric |
| cosine_similarity | S₁, S₂ | [-1,1] | Geometric |

---

## 9. Applications

### 9.1 Classification

Map any text to its closest SUBIT state using marker-based detection or trained models.

### 9.2 Control

Use SUBIT state as a constraint for LLM generation (style, tone, perspective).

### 9.3 Routing

Route tasks to specialized agents based on MODE value:
- STATE → reasoning agent
- VALUE → alignment agent
- FORM → creative agent
- FORCE → execution agent

### 9.4 Retrieval

Hybrid search combining SUBIT filtering with embedding similarity.

### 9.5 Interpolation

Create smooth transitions between archetypes using continuous SUBIT vectors.

---

## 10. Reference Implementation

The canonical implementation is available in the `subit-nous` Python package:

```python
from subit_nous.subit_algebra import Subit

# Create states
micro = Subit(0b10101010)  # 170
macro = Subit(0b11111111)  # 255

# Operations
xor_result = micro.xor(macro)  # 0b01010101 = MESO
distance = micro.distance(macro)  # 4
projected = micro.project("MODE")  # 2 (STATE)
flipped = micro.flip_axis("WHO")   # 0b00101010
```

---

## 11. Summary

```
SUBIT v3 = {
  Space: (ℤ₂)⁸
  Axes: 4 × (ℤ₂)²
  Operation: XOR
  Metric: Hamming
  Geometry: ℝ⁸ embedding
  Transformations: flips, permutations
  Invariants: parity, balance
  Canonical States: MICRO, MACRO, MESO, META
}
```

---

## 12. References

1. Plato – *Republic* (division of the soul: LOGOS, THYMOS, PATHOS)
2. Aristotle – *Rhetoric* (LOGOS, ETHOS, PATHOS)
3. Shannon, C. E. – *A Mathematical Theory of Communication* (binary information theory)
4. SUBIT‑NOUS Implementation – [github.com/sciganec/subit-nous](https://github.com/sciganec/subit-nous)

---

**Document Version:** 3.0  
**Last Updated:** 2026-04-10  
**Maintainer:** SUBIT Ecosystem