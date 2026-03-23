import { Bug, TrendingUp, Stethoscope, Calendar, Sprout, Droplets, HelpCircle, Leaf } from 'lucide-react';

const INTENT_META: Record<string, { label: string; icon: typeof Bug; color: string }> = {
  crop_disease_id: { label: 'Disease ID', icon: Bug, color: 'text-red-600 bg-red-50' },
  market_price: { label: 'Price Check', icon: TrendingUp, color: 'text-blue-600 bg-blue-50' },
  livestock_health: { label: 'Livestock', icon: Stethoscope, color: 'text-purple-600 bg-purple-50' },
  planting_calendar: { label: 'Planting', icon: Calendar, color: 'text-green-600 bg-green-50' },
  pest_management: { label: 'Pest Mgmt', icon: Bug, color: 'text-orange-600 bg-orange-50' },
  soil_fertility: { label: 'Soil', icon: Leaf, color: 'text-amber-700 bg-amber-50' },
  irrigation_advice: { label: 'Irrigation', icon: Droplets, color: 'text-cyan-600 bg-cyan-50' },
  general_agri: { label: 'General', icon: Sprout, color: 'text-green-600 bg-green-50' },
  human_escalation: { label: 'Escalated', icon: HelpCircle, color: 'text-red-600 bg-red-50' },
};

export function IntentBadge({ intent }: { intent: string }) {
  const meta = INTENT_META[intent] ?? { label: intent, icon: Sprout, color: 'text-gray-600 bg-gray-50' };
  const Icon = meta.icon;

  return (
    <span className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium ${meta.color}`}>
      <Icon size={12} />
      {meta.label}
    </span>
  );
}
