import { useState, useEffect } from 'react';
import { BarChart3, DollarSign, Zap, Target } from 'lucide-react';
import { fetchUnitEconomics, fetchIntentDistribution, fetchEscalationRate, fetchFunnel } from '../api/analytics';

export function AnalyticsDashboard() {
  const [economics, setEconomics] = useState<any>(null);
  const [intents, setIntents] = useState<any[]>([]);
  const [escalation, setEscalation] = useState<any>(null);
  const [funnel, setFunnel] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      fetchUnitEconomics().then((r) => r.data).catch(() => null),
      fetchIntentDistribution().then((r) => r.data ?? []).catch(() => []),
      fetchEscalationRate().then((r) => r.data).catch(() => null),
      fetchFunnel().then((r) => r.data).catch(() => null),
    ]).then(([econ, ints, esc, fun]) => {
      setEconomics(econ);
      setIntents(ints);
      setEscalation(esc);
      setFunnel(fun);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="text-sm text-earth-400">Loading analytics...</div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 p-6">
      <h2 className="font-display text-lg font-bold text-earth-800">Limi Analytics</h2>

      {/* KPI Cards */}
      <div className="grid grid-cols-4 gap-3">
        <KpiCard
          icon={<BarChart3 size={16} />}
          label="Total Queries"
          value={economics?.total_queries ?? 0}
        />
        <KpiCard
          icon={<DollarSign size={16} />}
          label="Avg Cost/Query"
          value={`${(economics?.avg_cost_per_query_usd_cents ?? 1.5).toFixed(2)}¢`}
        />
        <KpiCard
          icon={<Zap size={16} />}
          label="Cache Hit Rate"
          value={`${(economics?.cache_hit_rate_pct ?? 0).toFixed(1)}%`}
        />
        <KpiCard
          icon={<Target size={16} />}
          label="Escalation Rate"
          value={`${(escalation?.escalation_rate_pct ?? 0).toFixed(1)}%`}
        />
      </div>

      {/* Intent Distribution */}
      <div className="rounded-xl border border-earth-200 bg-white p-4">
        <h3 className="mb-3 text-sm font-semibold text-earth-700">Intent Distribution</h3>
        {intents.length > 0 ? (
          <div className="space-y-2">
            {intents.map((item: any) => {
              const maxCount = Math.max(...intents.map((i: any) => i.count));
              const pct = maxCount > 0 ? (item.count / maxCount) * 100 : 0;
              return (
                <div key={item.intent} className="flex items-center gap-2">
                  <span className="w-28 truncate text-xs text-earth-500">{item.intent}</span>
                  <div className="flex-1">
                    <div
                      className="h-4 rounded-r bg-green-200"
                      style={{ width: `${Math.max(pct, 2)}%` }}
                    />
                  </div>
                  <span className="w-8 text-right text-xs font-medium text-earth-600">{item.count}</span>
                </div>
              );
            })}
          </div>
        ) : (
          <p className="text-xs text-earth-300">No query data yet. Connect PostgreSQL and send queries to see analytics.</p>
        )}
      </div>

      {/* Financial Funnel */}
      <div className="rounded-xl border border-earth-200 bg-white p-4">
        <h3 className="mb-3 text-sm font-semibold text-earth-700">Financial Product Funnel</h3>
        {funnel?.financial_queries_total > 0 ? (
          <div className="space-y-1.5">
            {Object.entries(funnel.by_intent).map(([intent, count]) => (
              <div key={intent} className="flex items-center justify-between rounded-lg bg-earth-50 px-3 py-1.5 text-xs">
                <span className="text-earth-600">{intent.replace('_', ' ')}</span>
                <span className="font-semibold text-earth-800">{count as number}</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-earth-300">No financial queries yet. Ask about loans, insurance, or market linkage to populate the funnel.</p>
        )}
      </div>

      {/* Unit Economics */}
      <div className="rounded-xl border border-earth-200 bg-white p-4">
        <h3 className="mb-3 text-sm font-semibold text-earth-700">Unit Economics</h3>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-lg font-bold text-earth-800">
              {economics?.avg_input_tokens ?? '~3,000'}
            </div>
            <div className="text-[10px] text-earth-400">Avg Input Tokens</div>
          </div>
          <div>
            <div className="text-lg font-bold text-earth-800">
              {economics?.avg_output_tokens ?? '~800'}
            </div>
            <div className="text-[10px] text-earth-400">Avg Output Tokens</div>
          </div>
          <div>
            <div className="text-lg font-bold text-earth-800">
              {economics?.avg_latency_ms ? `${Math.round(economics.avg_latency_ms)}ms` : '~2s'}
            </div>
            <div className="text-[10px] text-earth-400">Avg Latency</div>
          </div>
        </div>
      </div>
    </div>
  );
}

function KpiCard({ icon, label, value }: { icon: React.ReactNode; label: string; value: string | number }) {
  return (
    <div className="rounded-xl border border-earth-200 bg-white p-3 text-center">
      <div className="mx-auto mb-1 flex h-8 w-8 items-center justify-center rounded-lg bg-green-50 text-green-600">
        {icon}
      </div>
      <div className="text-lg font-bold text-earth-800">{value}</div>
      <div className="text-[10px] text-earth-400">{label}</div>
    </div>
  );
}
