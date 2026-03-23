import type { ConfidenceLevel } from '../types';
import { ShieldCheck, ShieldAlert, ShieldQuestion } from 'lucide-react';

const STYLES: Record<ConfidenceLevel, { bg: string; text: string; icon: typeof ShieldCheck }> = {
  HIGH: { bg: 'bg-green-100', text: 'text-green-700', icon: ShieldCheck },
  MEDIUM: { bg: 'bg-amber-100', text: 'text-amber-700', icon: ShieldAlert },
  LOW: { bg: 'bg-red-100', text: 'text-red-700', icon: ShieldQuestion },
};

export function ConfidenceBadge({ level }: { level: ConfidenceLevel }) {
  const style = STYLES[level];
  const Icon = style.icon;

  return (
    <span className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-semibold ${style.bg} ${style.text}`}>
      <Icon size={12} />
      {level}
    </span>
  );
}
