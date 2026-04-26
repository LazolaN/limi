interface RiskScoreBadgeProps {
  score: number;
  size?: 'sm' | 'md';
}

export function RiskScoreBadge({ score, size = 'md' }: RiskScoreBadgeProps) {
  const color =
    score >= 70
      ? 'text-green-700 bg-green-50 border-green-200'
      : score >= 40
        ? 'text-amber-700 bg-amber-50 border-amber-200'
        : 'text-red-700 bg-red-50 border-red-200';

  const label = score >= 70 ? 'Good' : score >= 40 ? 'Fair' : 'Low';

  if (size === 'sm') {
    return (
      <span className={`inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-[10px] font-semibold ${color}`}>
        {score} {label}
      </span>
    );
  }

  return (
    <div className={`flex items-center gap-3 rounded-xl border p-3 ${color}`}>
      <div className="text-2xl font-bold">{score}</div>
      <div>
        <div className="text-xs font-semibold">{label} Risk Score</div>
        <div className="text-[10px] opacity-70">0-100 scale</div>
      </div>
    </div>
  );
}
