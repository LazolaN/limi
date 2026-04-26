import { useState, useEffect } from 'react';
import { Wallet, Shield, TrendingUp, PiggyBank } from 'lucide-react';
import { RiskScoreBadge } from './RiskScoreBadge';
import { fetchEligibleProducts, fetchRiskScore } from '../api/financial';
import type { FinancialProduct, FarmerRiskScore } from '../types/financial';

interface FinancialPanelProps {
  farmerId: string;
}

const PRODUCT_ICONS: Record<string, React.ReactNode> = {
  input_financing: <Wallet size={14} />,
  crop_insurance: <Shield size={14} />,
  market_linkage: <TrendingUp size={14} />,
  savings: <PiggyBank size={14} />,
};

const PRODUCT_COLORS: Record<string, string> = {
  input_financing: 'border-blue-200 bg-blue-50',
  crop_insurance: 'border-green-200 bg-green-50',
  market_linkage: 'border-purple-200 bg-purple-50',
  savings: 'border-amber-200 bg-amber-50',
};

export function FinancialPanel({ farmerId }: FinancialPanelProps) {
  const [riskScore, setRiskScore] = useState<FarmerRiskScore | null>(null);
  const [products, setProducts] = useState<FinancialProduct[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      fetchRiskScore(farmerId).catch(() => null),
      fetchEligibleProducts(farmerId).catch(() => null),
    ]).then(([score, eligibility]) => {
      setRiskScore(score);
      setProducts(eligibility?.eligible_products ?? []);
      setLoading(false);
    });
  }, [farmerId]);

  if (loading) {
    return (
      <div className="space-y-2">
        <div className="h-16 animate-pulse rounded-xl bg-earth-100" />
        <div className="h-12 animate-pulse rounded-lg bg-earth-100" />
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {riskScore && <RiskScoreBadge score={riskScore.score} />}

      {products.length > 0 ? (
        <div className="space-y-1.5">
          {products.map((product) => (
            <div
              key={product.id}
              className={`rounded-lg border p-2 text-xs ${PRODUCT_COLORS[product.product_type] ?? 'border-earth-200 bg-earth-50'}`}
            >
              <div className="flex items-center gap-1.5">
                {PRODUCT_ICONS[product.product_type]}
                <span className="font-semibold">{product.name}</span>
              </div>
              <div className="mt-0.5 text-[10px] opacity-70">
                {product.interest_rate_annual != null
                  ? `From ${product.interest_rate_annual}% p.a.`
                  : product.commission_pct != null
                    ? `${product.commission_pct}% commission`
                    : product.provider}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-[10px] text-earth-300">No eligible products</p>
      )}
    </div>
  );
}
