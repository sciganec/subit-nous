import { useState } from 'react';
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer, Tooltip,
} from 'recharts';
import {
  analyzeText, cosineSimilarity, hammingDistance,
  interpolateVectors, subitToAxes, vecToId, idToName,
  AXIS_CONFIG, PRESET_TEXTS, ARCHETYPE_CONFIG,
} from './subit';
import './App.css';

// ─── Design tokens ─────────────────────────────────────────────────────────────
const C = {
  bg:       '#0f172a',
  surface:  '#1e293b',
  surface2: '#162032',
  border:   '#334155',
  text:     '#e2e8f0',
  muted:    '#94a3b8',
  accent:   '#818cf8',
};

// ─── Mini components ───────────────────────────────────────────────────────────

function Card({ children, style }) {
  return (
    <div style={{
      background: C.surface, border: `1px solid ${C.border}`,
      borderRadius: 12, padding: '1rem', ...style,
    }}>
      {children}
    </div>
  );
}

function Tag({ children, color, bg }) {
  return (
    <span style={{
      display: 'inline-block', borderRadius: 6,
      padding: '2px 8px', fontSize: 12, fontWeight: 700,
      color, background: bg, letterSpacing: '0.04em',
    }}>
      {children}
    </span>
  );
}

function SectionTitle({ children }) {
  return (
    <h3 style={{
      color: C.muted, fontSize: 11, fontWeight: 700,
      letterSpacing: '0.1em', textTransform: 'uppercase',
      margin: '0 0 0.75rem 0',
    }}>
      {children}
    </h3>
  );
}

// ─── Word-highlighted text ─────────────────────────────────────────────────────
function HighlightedText({ tokens }) {
  return (
    <div style={{
      lineHeight: 1.9, fontSize: 15, color: C.text,
      background: C.surface2, borderRadius: 8,
      padding: '0.75rem 1rem', minHeight: 80,
      fontFamily: 'Georgia, serif',
    }}>
      {tokens.map((tok, i) =>
        tok.axis ? (
          <span key={i} title={`${tok.axis}: ${tok.category}`} style={{
            color: AXIS_CONFIG[tok.axis].color,
            background: AXIS_CONFIG[tok.axis].bg,
            borderRadius: 4, padding: '0 2px',
            cursor: 'default', fontWeight: 600,
          }}>{tok.text}</span>
        ) : (
          <span key={i}>{tok.text}</span>
        )
      )}
    </div>
  );
}

// ─── 8-bit binary grid ─────────────────────────────────────────────────────────
function BitGrid({ bits }) {
  const axLabels = ['WHO','WHO','WHERE','WHERE','WHEN','WHEN','WHY','WHY'];
  return (
    <div>
      <div style={{ display: 'flex', gap: 4, justifyContent: 'center' }}>
        {bits.map((bit, i) => {
          const col = AXIS_CONFIG[axLabels[i]].color;
          return (
            <div key={i} style={{
              width: 44, height: 44, borderRadius: 8,
              background: bit === 1 ? col : C.surface2,
              border: `2px solid ${bit === 1 ? col : C.border}`,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontWeight: 900, fontSize: 18,
              color: bit === 1 ? '#fff' : C.muted,
              transition: 'all 0.2s ease',
              boxShadow: bit === 1 ? `0 0 12px ${col}66` : 'none',
            }}>{bit}</div>
          );
        })}
      </div>
      <div style={{ display: 'flex', gap: 4, justifyContent: 'center', marginTop: 4 }}>
        {axLabels.map((ax, i) => (
          <div key={i} style={{
            width: 44, textAlign: 'center',
            fontSize: 9, color: AXIS_CONFIG[ax].color,
            fontWeight: 700, letterSpacing: '0.05em',
          }}>
            {ax.slice(0, 3)}
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Axes badges grid ──────────────────────────────────────────────────────────
function AxesBadges({ axes }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
      {['WHO','WHERE','WHEN','WHY'].map(ax => {
        const cfg = AXIS_CONFIG[ax];
        return (
          <div key={ax} style={{
            background: cfg.bg, border: `1px solid ${cfg.color}44`,
            borderRadius: 8, padding: '8px 12px',
            display: 'flex', alignItems: 'center', gap: 8,
          }}>
            <span style={{ fontSize: 18 }}>{cfg.icon}</span>
            <div>
              <div style={{ fontSize: 10, color: cfg.color, fontWeight: 700, letterSpacing: '0.08em' }}>{ax}</div>
              <div style={{ fontSize: 14, color: C.text, fontWeight: 700 }}>{axes[ax] || '—'}</div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

// ─── Radar chart ───────────────────────────────────────────────────────────────
const RADAR_LABELS = ['WHO₁','WHO₂','WHERE₁','WHERE₂','WHEN₁','WHEN₂','WHY₁','WHY₂'];

function SubitRadar({ vector, color = '#818cf8', height = 260 }) {
  const data = RADAR_LABELS.map((axis, i) => ({ axis, value: +(vector[i] || 0).toFixed(3) }));
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RadarChart data={data} margin={{ top: 10, right: 24, bottom: 10, left: 24 }}>
        <PolarGrid stroke={C.border} />
        <PolarAngleAxis dataKey="axis" tick={{ fill: C.muted, fontSize: 11 }} />
        <PolarRadiusAxis domain={[-1, 1]} tick={false} axisLine={false} />
        <Radar dataKey="value" stroke={color} fill={color} fillOpacity={0.3} strokeWidth={2} />
        <Tooltip
          contentStyle={{ background: C.surface, border: `1px solid ${C.border}`, borderRadius: 8, color: C.text }}
          formatter={v => [Number(v).toFixed(3), 'value']}
        />
      </RadarChart>
    </ResponsiveContainer>
  );
}

// ─── Archetype ID badge ────────────────────────────────────────────────────────
function ArchetypeBadge({ result }) {
  const { id, name, color, energy, bits } = result;
  const purity = Math.max(0, 100 - Math.round(energy * 20)).toFixed(0);
  return (
    <div style={{
      textAlign: 'center', padding: '1rem',
      background: `${color}18`, border: `1px solid ${color}55`,
      borderRadius: 12,
    }}>
      <div style={{ fontSize: 38, fontWeight: 900, color, fontFamily: 'monospace', lineHeight: 1 }}>{id}</div>
      <div style={{ fontSize: 12, color: C.muted, marginTop: 2 }}>0b{bits.join('')}</div>
      <div style={{ fontSize: 16, fontWeight: 700, color: C.text, marginTop: 6 }}>{name}</div>
      <div style={{ marginTop: 8, display: 'flex', justifyContent: 'center', gap: 8, flexWrap: 'wrap' }}>
        <Tag color={color} bg={`${color}22`}>energy {energy.toFixed(3)}</Tag>
        <Tag color={color} bg={`${color}22`}>purity {purity}%</Tag>
      </div>
    </div>
  );
}

// ─── Word legend ────────────────────────────────────────────────────────────────
function WordLegend({ tokens }) {
  const found = {};
  for (const t of tokens) {
    if (t.axis && t.text.trim()) {
      const key = `${t.axis}:${t.category}`;
      if (!found[key]) found[key] = { axis: t.axis, category: t.category, words: new Set() };
      found[key].words.add(t.text.trim().toLowerCase());
    }
  }
  const entries = Object.values(found);
  if (!entries.length) return <div style={{ fontSize: 12, color: C.muted, marginTop: 8 }}>No marker words detected yet.</div>;
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 8 }}>
      {entries.map(({ axis, category, words }) => (
        <span key={`${axis}:${category}`} style={{
          fontSize: 11, borderRadius: 20, padding: '2px 10px',
          color: AXIS_CONFIG[axis].color, background: AXIS_CONFIG[axis].bg,
          border: `1px solid ${AXIS_CONFIG[axis].color}44`,
        }}>
          {axis}:{category} — {[...words].join(', ')}
        </span>
      ))}
    </div>
  );
}

// ─── Similarity bar ────────────────────────────────────────────────────────────
function SimilarityBar({ value }) {
  const pct = ((value + 1) / 2 * 100).toFixed(1);
  const color = value > 0.5 ? '#34d399' : value > 0 ? '#fbbf24' : '#f87171';
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
        <span style={{ fontSize: 12, color: C.muted }}>Cosine similarity</span>
        <span style={{ fontSize: 14, fontWeight: 700, color }}>{value.toFixed(4)}</span>
      </div>
      <div style={{ height: 8, background: C.surface2, borderRadius: 4, overflow: 'hidden' }}>
        <div style={{
          height: '100%', width: `${pct}%`, background: color,
          borderRadius: 4, transition: 'width 0.3s ease',
        }} />
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
// TAB: ANALYZE
// ════════════════════════════════════════════════════════════════════════════════
function AnalyzeTab() {
  const [text, setText] = useState(PRESET_TEXTS[0].text);
  const result = analyzeText(text);

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>

      {/* LEFT */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <Card>
          <SectionTitle>✍️ Input text</SectionTitle>
          <textarea
            value={text}
            onChange={e => setText(e.target.value)}
            rows={6}
            style={{
              width: '100%', boxSizing: 'border-box',
              background: C.surface2, color: C.text,
              border: `1px solid ${C.border}`, borderRadius: 8,
              padding: '0.6rem 0.8rem', fontSize: 14,
              fontFamily: 'Georgia, serif', lineHeight: 1.7,
              resize: 'vertical', outline: 'none',
            }}
          />
        </Card>

        <Card>
          <SectionTitle>🎨 Semantic highlight</SectionTitle>
          <HighlightedText tokens={result.tokens} />
          <WordLegend tokens={result.tokens} />
        </Card>

        <Card>
          <SectionTitle>📚 Presets</SectionTitle>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 6 }}>
            {PRESET_TEXTS.map(p => (
              <button key={p.label} onClick={() => setText(p.text)} style={{
                background: text === p.text ? `${p.color}30` : C.surface2,
                border: `1px solid ${text === p.text ? p.color : C.border}`,
                borderRadius: 8, padding: '6px 4px', cursor: 'pointer',
                color: p.color, fontSize: 12, fontWeight: 700, transition: 'all 0.15s',
              }}>
                <div style={{ fontSize: 18 }}>{p.emoji}</div>
                <div>{p.label}</div>
              </button>
            ))}
          </div>
        </Card>
      </div>

      {/* RIGHT */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <ArchetypeBadge result={result} />
        <Card>
          <SectionTitle>📡 Soft vector (radar)</SectionTitle>
          <SubitRadar vector={result.vector} color={result.color} />
        </Card>
        <Card>
          <SectionTitle>🧭 Dimension breakdown</SectionTitle>
          <AxesBadges axes={result.axes} />
        </Card>
        <Card>
          <SectionTitle>🔢 8-bit SUBIT code</SectionTitle>
          <BitGrid bits={result.bits} />
        </Card>
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
// TAB: COMPARE
// ════════════════════════════════════════════════════════════════════════════════
function CompareTab() {
  const [textA, setTextA] = useState(PRESET_TEXTS[0].text);
  const [textB, setTextB] = useState(PRESET_TEXTS[1].text);
  const rA = analyzeText(textA);
  const rB = analyzeText(textB);
  const sim = cosineSimilarity(rA.vector, rB.vector);
  const hdist = hammingDistance(rA.id, rB.id);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        {[[textA, setTextA, rA, '#818cf8', '🟣 Text A'], [textB, setTextB, rB, '#34d399', '🟢 Text B']].map(
          ([text, setTxt, r, col, label]) => (
            <div key={label} style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              <Card>
                <SectionTitle>{label}</SectionTitle>
                <textarea
                  value={text}
                  onChange={e => setTxt(e.target.value)}
                  rows={5}
                  style={{
                    width: '100%', boxSizing: 'border-box',
                    background: C.surface2, color: C.text,
                    border: `1px solid ${C.border}`, borderRadius: 8,
                    padding: '0.6rem 0.8rem', fontSize: 13,
                    fontFamily: 'Georgia, serif', lineHeight: 1.7,
                    resize: 'vertical', outline: 'none',
                  }}
                />
              </Card>
              <ArchetypeBadge result={r} />
              <Card>
                <SectionTitle>📡 Radar</SectionTitle>
                <SubitRadar vector={r.vector} color={col} height={220} />
              </Card>
              <Card>
                <SectionTitle>🔢 Bits</SectionTitle>
                <BitGrid bits={r.bits} />
              </Card>
            </div>
          )
        )}
      </div>

      {/* Metrics */}
      <Card>
        <SectionTitle>📊 Semantic distance</SectionTitle>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr auto', gap: 24, alignItems: 'center' }}>
          <SimilarityBar value={sim} />
          <div style={{ textAlign: 'center', minWidth: 120 }}>
            <div style={{ fontSize: 11, color: C.muted, marginBottom: 4 }}>Hamming distance</div>
            <div style={{ fontSize: 28, fontWeight: 900, color: hdist <= 2 ? '#34d399' : hdist <= 4 ? '#fbbf24' : '#f87171' }}>
              {hdist} / 8
            </div>
            <div style={{ fontSize: 11, color: C.muted }}>bits differ</div>
          </div>
        </div>

        {/* Bit comparison */}
        <div style={{ marginTop: 12 }}>
          <SectionTitle>Bit-by-bit comparison</SectionTitle>
          <div style={{ display: 'flex', gap: 4, justifyContent: 'center' }}>
            {rA.bits.map((bA, i) => {
              const bB = rB.bits[i];
              const match = bA === bB;
              return (
                <div key={i} style={{ width: 44, borderRadius: 8, overflow: 'hidden', border: `2px solid ${match ? C.border : '#f87171'}` }}>
                  <div style={{
                    height: 22, background: bA ? '#818cf8' : C.surface2,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    color: bA ? '#fff' : C.muted, fontSize: 13, fontWeight: 700,
                  }}>{bA}</div>
                  <div style={{
                    height: 22, background: bB ? '#34d399' : C.surface2,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    color: bB ? '#fff' : C.muted, fontSize: 13, fontWeight: 700,
                  }}>{bB}</div>
                </div>
              );
            })}
          </div>
          <div style={{ display: 'flex', justifyContent: 'center', gap: 16, marginTop: 8 }}>
            <Tag color='#818cf8' bg='#818cf822'>🟣 Text A</Tag>
            <Tag color='#34d399' bg='#34d39922'>🟢 Text B</Tag>
            <Tag color='#f87171' bg='#f8717122'>🔴 different bit</Tag>
          </div>
        </div>
      </Card>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
// TAB: SPACE
// ════════════════════════════════════════════════════════════════════════════════
const CARDINAL = Object.entries(ARCHETYPE_CONFIG).map(([name, cfg]) => ({
  name, ...cfg,
  vec: Array.from({ length: 8 }, (_, i) => ((cfg.id >> (7 - i)) & 1) ? 1 : -1),
}));

function SpaceTab() {
  const [activeFrom, setActiveFrom] = useState('MICRO');
  const [activeTo,   setActiveTo]   = useState('META');
  const [alpha, setAlpha]           = useState(0.5);

  const fromCfg  = ARCHETYPE_CONFIG[activeFrom];
  const toCfg    = ARCHETYPE_CONFIG[activeTo];
  const fromVec  = CARDINAL.find(c => c.name === activeFrom).vec;
  const toVec    = CARDINAL.find(c => c.name === activeTo).vec;
  const interpVec  = interpolateVectors(fromVec, toVec, alpha);
  const interpAxes = subitToAxes(interpVec);
  const interpId   = vecToId(interpVec);
  const interpName = idToName(interpId);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>

      {/* 4 cardinal cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
        {CARDINAL.map(c => (
          <Card key={c.name} style={{ textAlign: 'center', border: `1px solid ${c.color}55` }}>
            <div style={{ fontSize: 32 }}>{c.emoji}</div>
            <div style={{ fontSize: 18, fontWeight: 900, color: c.color, marginTop: 4 }}>{c.name}</div>
            <div style={{ fontSize: 22, fontWeight: 700, color: C.muted, fontFamily: 'monospace' }}>{c.id}</div>
            <div style={{ fontSize: 11, color: C.muted, marginTop: 6, lineHeight: 1.5 }}>{c.tagline}</div>
            <SubitRadar vector={c.vec} color={c.color} height={160} />
          </Card>
        ))}
      </div>

      {/* Interpolation */}
      <Card>
        <SectionTitle>🎛️ Semantic interpolation</SectionTitle>
        <div style={{ display: 'grid', gridTemplateColumns: '160px 1fr 120px 1fr 160px', gap: 12, alignItems: 'center' }}>

          {/* From */}
          <div>
            <div style={{ fontSize: 11, color: C.muted, marginBottom: 6 }}>FROM</div>
            {CARDINAL.map(c => (
              <button key={c.name} onClick={() => setActiveFrom(c.name)} style={{
                display: 'block', width: '100%', marginBottom: 4,
                background: activeFrom === c.name ? `${c.color}30` : C.surface2,
                border: `1px solid ${activeFrom === c.name ? c.color : C.border}`,
                borderRadius: 8, padding: '6px 12px', cursor: 'pointer',
                color: c.color, fontSize: 13, fontWeight: 700, textAlign: 'left',
              }}>{c.emoji} {c.name}</button>
            ))}
          </div>

          {/* Slider */}
          <div style={{ textAlign: 'center' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
              <span style={{ fontSize: 11, color: fromCfg.color, fontWeight: 700 }}>{Math.round((1 - alpha) * 100)}%</span>
              <span style={{ fontSize: 11, color: toCfg.color, fontWeight: 700 }}>{Math.round(alpha * 100)}%</span>
            </div>
            <input
              type="range" min={0} max={1} step={0.01} value={alpha}
              onChange={e => setAlpha(parseFloat(e.target.value))}
              style={{ width: '100%', accentColor: C.accent }}
            />
            <div style={{ marginTop: 8 }}>
              <AxesBadges axes={interpAxes} />
            </div>
          </div>

          {/* Result */}
          <div style={{
            textAlign: 'center',
            background: `${fromCfg.color}18`,
            border: `1px solid ${fromCfg.color}44`,
            borderRadius: 12, padding: '1rem',
          }}>
            <div style={{ fontSize: 30, fontWeight: 900, color: fromCfg.color, fontFamily: 'monospace' }}>{interpId}</div>
            <div style={{ fontSize: 11, color: C.muted, marginTop: 4 }}>α = {alpha.toFixed(2)}</div>
            <div style={{ fontSize: 12, fontWeight: 700, color: C.text, marginTop: 4 }}>{interpName}</div>
          </div>

          {/* Radar */}
          <SubitRadar vector={interpVec} color={fromCfg.color} height={200} />

          {/* To */}
          <div>
            <div style={{ fontSize: 11, color: C.muted, marginBottom: 6 }}>TO</div>
            {CARDINAL.map(c => (
              <button key={c.name} onClick={() => setActiveTo(c.name)} style={{
                display: 'block', width: '100%', marginBottom: 4,
                background: activeTo === c.name ? `${c.color}30` : C.surface2,
                border: `1px solid ${activeTo === c.name ? c.color : C.border}`,
                borderRadius: 8, padding: '6px 12px', cursor: 'pointer',
                color: c.color, fontSize: 13, fontWeight: 700, textAlign: 'right',
              }}>{c.emoji} {c.name}</button>
            ))}
          </div>
        </div>
      </Card>

      {/* 256 grid */}
      <Card>
        <SectionTitle>🗺️ All 256 archetypes — colored by WHY axis</SectionTitle>
        <div style={{ fontSize: 11, color: C.muted, marginBottom: 8 }}>
          Hover a cell to see its coordinates. Bright borders = MICRO/MACRO/MESO/META.
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(16, 1fr)', gap: 2 }}>
          {Array.from({ length: 256 }, (_, id) => {
            const why = id & 0b11;
            const colors = ['#f87171','#fbbf24','#60a5fa','#34d399'];
            const col = colors[why];
            const isSpecial = [0,85,170,255].includes(id);
            const axVec = Array.from({ length: 8 }, (_, i) => ((id >> (7 - i)) & 1) ? 1 : -1);
            const ax = subitToAxes(axVec);
            return (
              <div
                key={id}
                title={`${id}: ${ax.WHO}·${ax.WHERE}·${ax.WHEN}·${ax.WHY}`}
                style={{
                  aspectRatio: 1, borderRadius: 3, cursor: 'default',
                  background: isSpecial ? col : `${col}40`,
                  border: isSpecial ? `2px solid ${col}` : `1px solid ${col}22`,
                  transition: 'transform 0.1s, background 0.1s',
                  position: 'relative',
                }}
                onMouseEnter={e => {
                  e.currentTarget.style.transform = 'scale(2.2)';
                  e.currentTarget.style.zIndex = 20;
                  e.currentTarget.style.background = col;
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.transform = '';
                  e.currentTarget.style.zIndex = '';
                  e.currentTarget.style.background = isSpecial ? col : `${col}40`;
                }}
              />
            );
          })}
        </div>
        <div style={{ display: 'flex', gap: 12, marginTop: 10, flexWrap: 'wrap' }}>
          {[['THYMOS','#f87171'],['PATHOS','#fbbf24'],['LOGOS','#60a5fa'],['ETHOS','#34d399']].map(([name, color]) => (
            <Tag key={name} color={color} bg={`${color}22`}>■ WHY={name}</Tag>
          ))}
          <Tag color={C.muted} bg={C.surface2}>■ bright border = cardinal</Tag>
        </div>
      </Card>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════════════════
// ROOT APP
// ════════════════════════════════════════════════════════════════════════════════
const TABS = [
  { id: 'analyze', label: '🔍 Analyze' },
  { id: 'compare', label: '⚖️ Compare' },
  { id: 'space',   label: '🌌 Space'   },
];

export default function App() {
  const [tab, setTab] = useState('analyze');

  return (
    <div style={{ minHeight: '100vh', background: C.bg, color: C.text, fontFamily: 'system-ui, sans-serif' }}>

      {/* Sticky header */}
      <header style={{
        borderBottom: `1px solid ${C.border}`,
        background: `${C.surface}ee`,
        backdropFilter: 'blur(12px)',
        position: 'sticky', top: 0, zIndex: 100,
        padding: '0 2rem',
      }}>
        <div style={{ maxWidth: 1200, margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: 60 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <span style={{ fontSize: 24 }}>🧠</span>
            <div>
              <span style={{ fontWeight: 900, fontSize: 18, color: C.text }}>SUBIT‑NOUS</span>
              <span style={{ fontSize: 12, color: C.muted, marginLeft: 10 }}>
                Operating System for Meaning · (ℤ₂)⁸ · 256 archetypes
              </span>
            </div>
          </div>
          <nav style={{ display: 'flex', gap: 4 }}>
            {TABS.map(t => (
              <button key={t.id} onClick={() => setTab(t.id)} style={{
                background: tab === t.id ? `${C.accent}22` : 'transparent',
                border: `1px solid ${tab === t.id ? C.accent : 'transparent'}`,
                borderRadius: 8, padding: '6px 16px', cursor: 'pointer',
                color: tab === t.id ? C.accent : C.muted,
                fontSize: 14, fontWeight: tab === t.id ? 700 : 400,
                transition: 'all 0.15s',
              }}>{t.label}</button>
            ))}
          </nav>
        </div>
      </header>

      {/* Axis legend bar */}
      <div style={{ background: C.surface2, borderBottom: `1px solid ${C.border}`, padding: '6px 2rem' }}>
        <div style={{ maxWidth: 1200, margin: '0 auto', display: 'flex', gap: 20, alignItems: 'center', flexWrap: 'wrap' }}>
          <span style={{ fontSize: 11, color: C.muted, fontWeight: 700, letterSpacing: '0.08em' }}>
            SUBIT = WHO × WHERE × WHEN × WHY
          </span>
          {Object.entries(AXIS_CONFIG).map(([ax, cfg]) => (
            <span key={ax} style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <span style={{ width: 8, height: 8, borderRadius: 2, background: cfg.color, display: 'inline-block' }} />
              <span style={{ fontSize: 11, color: cfg.color, fontWeight: 600 }}>{ax}</span>
            </span>
          ))}
          <span style={{ fontSize: 11, color: C.muted, marginLeft: 'auto' }}>
            ⚡170 · 🌍255 · 🌙85 · 🌑0
          </span>
        </div>
      </div>

      {/* Main content */}
      <main style={{ maxWidth: 1200, margin: '0 auto', padding: '1.5rem 2rem 4rem' }}>
        {tab === 'analyze' && <AnalyzeTab />}
        {tab === 'compare' && <CompareTab />}
        {tab === 'space'   && <SpaceTab />}
      </main>

      <footer style={{
        borderTop: `1px solid ${C.border}`, padding: '1rem 2rem',
        textAlign: 'center', color: C.muted, fontSize: 12,
      }}>
        SUBIT‑NOUS v5.0 · SUBIT = (ℤ₂)⁸ = WHO × WHERE × WHEN × MODE · MIT License
      </footer>
    </div>
  );
}
