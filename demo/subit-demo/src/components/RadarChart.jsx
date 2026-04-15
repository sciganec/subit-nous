import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';

export default function SubitRadar({ vector }) {
  const data = [
    { axis: 'WHO₁', value: vector[0] },
    { axis: 'WHO₂', value: vector[1] },
    { axis: 'WHERE₁', value: vector[2] },
    { axis: 'WHERE₂', value: vector[3] },
    { axis: 'WHEN₁', value: vector[4] },
    { axis: 'WHEN₂', value: vector[5] },
    { axis: 'WHY₁', value: vector[6] },
    { axis: 'WHY₂', value: vector[7] },
  ];
  return (
    <ResponsiveContainer width="100%" height={300}>
      <RadarChart data={data}>
        <PolarGrid />
        <PolarAngleAxis dataKey="axis" tick={{ fontSize: 10 }} />
        <PolarRadiusAxis domain={[-1, 1]} />
        <Radar dataKey="value" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
      </RadarChart>
    </ResponsiveContainer>
  );
}