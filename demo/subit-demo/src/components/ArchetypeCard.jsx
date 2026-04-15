export default function ArchetypeCard({ subitId, name, energy, axes }) {
  return (
    <div style={{ border: '1px solid #ccc', borderRadius: '12px', padding: '1rem', margin: '1rem 0' }}>
      <h3>🧠 Archetype</h3>
      <p><strong>ID:</strong> {subitId}</p>
      <p><strong>Name:</strong> {name}</p>
      <p><strong>Energy:</strong> {energy.toFixed(3)}</p>
      <p><strong>Axes:</strong> WHO={axes.WHO}, WHERE={axes.WHERE}, WHEN={axes.WHEN}, WHY={axes.WHY}</p>
    </div>
  );
}