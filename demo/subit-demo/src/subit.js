// subit.js — SUBIT-NOUS core engine (browser-compatible)
// v5.0 enhanced: tokenization, presets, interpolation, Hamming

// ─── Dimension markers ────────────────────────────────────────────────────────
export const MARKERS = {
  WHO: {
    ME:   ['i', 'me', 'my', 'mine', 'myself'],
    WE:   ['we', 'us', 'our', 'ours', 'ourselves'],
    YOU:  ['you', 'your', 'yours', 'yourself'],
    THEY: ['they', 'them', 'their', 'theirs', 'he', 'she', 'it'],
  },
  WHERE: {
    EAST:  ['east', 'eastern', 'right', 'forward', 'future', 'advance'],
    SOUTH: ['south', 'southern', 'down', 'downward', 'growth', 'expand'],
    WEST:  ['west', 'western', 'left', 'back', 'past', 'retreat'],
    NORTH: ['north', 'northern', 'up', 'center', 'stable', 'core'],
  },
  WHEN: {
    SPRING: ['spring', 'start', 'begin', 'birth', 'dawn', 'new', 'initiate'],
    SUMMER: ['summer', 'peak', 'mid', 'height', 'flourish', 'mature'],
    AUTUMN: ['autumn', 'fall', 'decay', 'decline', 'evening', 'late', 'reflect'],
    WINTER: ['winter', 'end', 'death', 'night', 'final', 'still'],
  },
  WHY: {
    LOGOS:  ['logic', 'logical', 'reason', 'code', 'data', 'proof', 'science', 'math', 'algorithm', 'system', 'structure', 'analyze', 'analysis', 'think'],
    ETHOS:  ['ethics', 'ethos', 'moral', 'trust', 'community', 'tradition', 'virtue', 'justice', 'harmony', 'honest', 'fair'],
    PATHOS: ['pathos', 'emotion', 'beauty', 'art', 'love', 'joy', 'sorrow', 'passion', 'aesthetic', 'feeling', 'dream', 'heart', 'soul'],
    THYMOS: ['thymos', 'spirit', 'will', 'courage', 'power', 'control', 'ambition', 'fight', 'dominate', 'strength', 'force', 'victory', 'bold'],
  },
};

// ─── Visual config ────────────────────────────────────────────────────────────
export const AXIS_CONFIG = {
  WHO:   { color: '#60a5fa', bg: 'rgba(96,165,250,0.18)',  label: 'WHO',   icon: '👤' },
  WHERE: { color: '#34d399', bg: 'rgba(52,211,153,0.18)',  label: 'WHERE', icon: '🧭' },
  WHEN:  { color: '#fbbf24', bg: 'rgba(251,191,36,0.18)',  label: 'WHEN',  icon: '⏳' },
  WHY:   { color: '#f87171', bg: 'rgba(248,113,113,0.18)', label: 'WHY',   icon: '💡' },
};

export const ARCHETYPE_CONFIG = {
  MICRO: { id: 170, color: '#818cf8', emoji: '⚡', tagline: 'Individual · Logical · Forward · New' },
  MACRO: { id: 255, color: '#34d399', emoji: '🌍', tagline: 'Collective · Ethical · Growth · Peak' },
  MESO:  { id: 85,  color: '#fbbf24', emoji: '🌙', tagline: 'Dialogical · Aesthetic · Backward · Declining' },
  META:  { id: 0,   color: '#f87171', emoji: '🌑', tagline: 'Systemic · Willful · Stable · Final' },
};

// ─── Preset texts ─────────────────────────────────────────────────────────────
export const PRESET_TEXTS = [
  {
    label: 'MICRO',
    emoji: '⚡',
    color: '#818cf8',
    text: 'I think logically about the east in spring. My data proves that science advances forward with each new beginning. I reason precisely from first principles.',
    description: 'Individual · Logical · Forward · New',
  },
  {
    label: 'MACRO',
    emoji: '🌍',
    color: '#34d399',
    text: 'We trust our community in the south during summer. Our ethics bind us together through tradition. We flourish in harmony, growing together toward shared virtue and justice.',
    description: 'Collective · Ethical · Growth · Peak',
  },
  {
    label: 'MESO',
    emoji: '🌙',
    color: '#fbbf24',
    text: 'You feel the beauty of art in the autumn decline. Your love and sorrow flow west, back toward the past. The aesthetic moment fades like a poem into the evening.',
    description: 'Dialogical · Aesthetic · Backward · Declining',
  },
  {
    label: 'META',
    emoji: '🌑',
    color: '#f87171',
    text: 'They control power in the north during winter. Their will dominates through ambition and courage. The final night reigns at the stable center of authority.',
    description: 'Systemic · Willful · Stable · Final',
  },
  {
    label: 'Science',
    emoji: '🔬',
    color: '#60a5fa',
    text: 'I analyzed the data structure using a new algorithm. My proof relies on mathematical logic and systematic reasoning. The science advances our understanding of the code.',
    description: 'LOGOS — analytical text',
  },
  {
    label: 'Manifesto',
    emoji: '✊',
    color: '#f87171',
    text: 'We must fight for our community with courage and strength. Our spirit will dominate through ambition. Together we control our destiny with bold determination and power.',
    description: 'THYMOS/WE — collective call to action',
  },
  {
    label: 'Poem',
    emoji: '🌸',
    color: '#fbbf24',
    text: 'You dream of beauty in the art of evening. Your heart carries sorrow and love into the past. The soul reflects on aesthetic feeling as autumn fades.',
    description: 'PATHOS/YOU — lyrical text',
  },
  {
    label: 'Hamlet',
    emoji: '💀',
    color: '#a78bfa',
    text: 'To be or not to be — that is the question. Whether it is nobler in the mind to suffer the slings and arrows of outrageous fortune, or to take arms against a sea of troubles.',
    description: 'Classic — mixed archetype',
  },
];

// ─── Tokenization with axis highlighting ──────────────────────────────────────
const WORD_LOOKUP = (() => {
  const map = {};
  for (const [axis, cats] of Object.entries(MARKERS)) {
    for (const [cat, words] of Object.entries(cats)) {
      for (const w of words) {
        if (!map[w]) map[w] = { axis, category: cat };
      }
    }
  }
  return map;
})();

export function tokenizeWithHighlights(text) {
  const tokens = [];
  const regex = /(\b[a-zA-Z']+\b|[^a-zA-Z']+)/g;
  let match;
  while ((match = regex.exec(text)) !== null) {
    const raw = match[0];
    const lower = raw.toLowerCase().replace(/'/g, '');
    const info = WORD_LOOKUP[lower];
    tokens.push({ text: raw, axis: info?.axis || null, category: info?.category || null });
  }
  return tokens;
}

// ─── Core analysis ────────────────────────────────────────────────────────────
const CATEGORY_TO_BITS = {
  ME: [1,-1], WE: [1,1], YOU: [-1,1], THEY: [-1,-1],
  EAST: [1,-1], SOUTH: [1,1], WEST: [-1,1], NORTH: [-1,-1],
  SPRING: [1,-1], SUMMER: [1,1], AUTUMN: [-1,1], WINTER: [-1,-1],
  LOGOS: [1,-1], ETHOS: [1,1], PATHOS: [-1,1], THYMOS: [-1,-1],
};

function countWord(text, word) {
  const re = new RegExp(`\\b${word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'gi');
  return (text.match(re) || []).length;
}

export function heuristicTextToSubit(text) {
  const lower = text.toLowerCase();
  const scores = {};
  for (const [axis, cats] of Object.entries(MARKERS)) {
    for (const [cat, words] of Object.entries(cats)) {
      let cnt = 0;
      for (const w of words) cnt += countWord(lower, w);
      if (cnt > 0) scores[`${axis}|${cat}`] = cnt;
    }
  }
  const vec = new Array(8).fill(0);
  const axisOrder = ['WHO', 'WHERE', 'WHEN', 'WHY'];
  for (let i = 0; i < axisOrder.length; i++) {
    const axis = axisOrder[i];
    const cats = Object.keys(MARKERS[axis]);
    const catScores = {};
    for (const cat of cats) catScores[cat] = scores[`${axis}|${cat}`] || 0;
    const total = Object.values(catScores).reduce((a, b) => a + b, 0);
    if (total === 0) continue;
    let b1 = 0, b2 = 0;
    for (const [cat, score] of Object.entries(catScores)) {
      const prob = score / total;
      const [bit1, bit2] = CATEGORY_TO_BITS[cat];
      b1 += prob * bit1;
      b2 += prob * bit2;
    }
    vec[2 * i] = Math.min(1, Math.max(-1, b1));
    vec[2 * i + 1] = Math.min(1, Math.max(-1, b2));
  }
  return vec;
}

export function computeEnergy(vec) {
  let minDist2 = Infinity;
  for (let mask = 0; mask < 256; mask++) {
    let dist2 = 0;
    for (let i = 0; i < 8; i++) {
      const bit = (mask >> (7 - i)) & 1 ? 1 : -1;
      dist2 += (vec[i] - bit) ** 2;
    }
    if (dist2 < minDist2) minDist2 = dist2;
  }
  return minDist2;
}

export function subitToAxes(vec) {
  const bits = vec.map(v => v > 0 ? 1 : 0);
  const b = s => `${bits[s]}${bits[s+1]}`;
  const whoMap   = { '10':'ME','11':'WE','01':'YOU','00':'THEY' };
  const whereMap = { '10':'EAST','11':'SOUTH','01':'WEST','00':'NORTH' };
  const whenMap  = { '10':'SPRING','11':'SUMMER','01':'AUTUMN','00':'WINTER' };
  const whyMap   = { '10':'LOGOS','11':'ETHOS','01':'PATHOS','00':'THYMOS' };
  return {
    WHO:   whoMap[b(0)]   || 'ME',
    WHERE: whereMap[b(2)] || 'EAST',
    WHEN:  whenMap[b(4)]  || 'SPRING',
    WHY:   whyMap[b(6)]   || 'LOGOS',
  };
}

export function vecToId(vec) {
  const bits = vec.map(v => v > 0 ? '1' : '0').join('');
  return parseInt(bits, 2);
}

export function idToName(id) {
  const special = { 170:'MICRO', 255:'MACRO', 85:'MESO', 0:'META' };
  if (special[id] !== undefined) return `${special[id]} mode`;
  return `Archetype ${id}`;
}

export function idToColor(id) {
  const special = { 170:'#818cf8', 255:'#34d399', 85:'#fbbf24', 0:'#f87171' };
  if (special[id] !== undefined) return special[id];
  // Color by WHY (bits 0-1)
  const why = id & 0b11;
  return ['#f87171','#fbbf24','#60a5fa','#34d399'][why];
}

export function cosineSimilarity(v1, v2) {
  let dot = 0, n1 = 0, n2 = 0;
  for (let i = 0; i < 8; i++) {
    dot += v1[i] * v2[i];
    n1 += v1[i] ** 2;
    n2 += v2[i] ** 2;
  }
  if (n1 === 0 || n2 === 0) return 0;
  return dot / (Math.sqrt(n1) * Math.sqrt(n2));
}

export function hammingDistance(id1, id2) {
  let xor = id1 ^ id2;
  let count = 0;
  while (xor) { count += xor & 1; xor >>= 1; }
  return count;
}

export function interpolateVectors(v1, v2, alpha) {
  return v1.map((v, i) => v * (1 - alpha) + v2[i] * alpha);
}

// ─── Full text analysis ───────────────────────────────────────────────────────
export function analyzeText(text) {
  const vector = heuristicTextToSubit(text);
  const axes   = subitToAxes(vector);
  const id     = vecToId(vector);
  const name   = idToName(id);
  const energy = computeEnergy(vector);
  const tokens = tokenizeWithHighlights(text);
  const bits   = vector.map(v => v > 0 ? 1 : 0);
  const color  = idToColor(id);
  return { vector, axes, id, name, energy, tokens, bits, color };
}

// ─── Axis score breakdown ─────────────────────────────────────────────────────
export function getAxisScores(text) {
  const lower = text.toLowerCase();
  const result = {};
  for (const [axis, cats] of Object.entries(MARKERS)) {
    result[axis] = {};
    let axisTotal = 0;
    for (const [cat, words] of Object.entries(cats)) {
      let cnt = 0;
      for (const w of words) cnt += countWord(lower, w);
      result[axis][cat] = cnt;
      axisTotal += cnt;
    }
    result[axis]._total = axisTotal;
  }
  return result;
}
