import { useState, useEffect } from 'react';
import { heuristicTextToSubit, cosineSimilarity } from '../subit';

const MICRO_VEC = heuristicTextToSubit('I think logically about the east in spring.');
const MACRO_VEC = heuristicTextToSubit('We trust our community in the south during summer.');

export default function LiveSlider({ text }) {
  const [alpha, setAlpha] = useState(0.5);
  const [similarity, setSimilarity] = useState(0);
  useEffect(() => {
    const currentVec = MICRO_VEC.map((v, i) => v * (1 - alpha) + MACRO_VEC[i] * alpha);
    const sim = cosineSimilarity(heuristicTextToSubit(text), currentVec);
    setSimilarity(sim);
  }, [alpha, text]);
  return (
    <div style={{ border: '1px solid #ccc', borderRadius: '12px', padding: '1rem', margin: '1rem 0' }}>
      <h3>🎛️ Live Interpolation (MICRO ↔ MACRO)</h3>
      <input type="range" min={0} max={1} step={0.01} value={alpha} onChange={e => setAlpha(parseFloat(e.target.value))} />
      <p>Alpha: {alpha.toFixed(2)} | Similarity to target vector: {similarity.toFixed(4)}</p>
    </div>
  );
}