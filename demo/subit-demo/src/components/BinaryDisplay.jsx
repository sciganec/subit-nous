export default function BinaryDisplay({ bits }) {
  const bitArray = bits.split('').map(Number);
  return (
    <div style={{ display: 'flex', gap: '8px', justifyContent: 'center', margin: '1rem 0' }}>
      {bitArray.map((bit, i) => (
        <div key={i} style={{
          width: '40px', height: '40px', borderRadius: '8px',
          backgroundColor: bit === 1 ? '#2ecc71' : '#95a5a6',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontWeight: 'bold', color: 'white'
        }}>
          {bit}
        </div>
      ))}
    </div>
  );
}