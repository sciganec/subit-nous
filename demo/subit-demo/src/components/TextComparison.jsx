import { useState } from 'react';
import { heuristicTextToSubit, cosineSimilarity } from '../subit';

export default function TextComparison() {
  const [textA, setTextA] = useState('');
  const [textB, setTextB] = useState('');
  const [similarity, setSimilarity] = useState(null);

  const handleCompare = () => {
    if (!textA.trim() || !textB.trim()) {
      setSimilarity(null);
      return;
    }
    const vA = heuristicTextToSubit(textA);
    const vB = heuristicTextToSubit(textB);
    const sim = cosineSimilarity(vA, vB);
    setSimilarity(sim);
  };

  return (
    <div style={{ border: '1px solid #ccc', borderRadius: '12px', padding: '1rem', margin: '1rem 0' }}>
      <h3>📊 Text Comparison</h3>
      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        <textarea
          rows={3}
          cols={40}
          placeholder="Text A"
          value={textA}
          onChange={e => setTextA(e.target.value)}
        />
        <textarea
          rows={3}
          cols={40}
          placeholder="Text B"
          value={textB}
          onChange={e => setTextB(e.target.value)}
        />
      </div>
      <button onClick={handleCompare} style={{ marginTop: '0.5rem' }}>Compare</button>
      {similarity !== null && (
        <p><strong>Cosine similarity:</strong> {similarity.toFixed(4)}</p>
      )}
    </div>
  );
}