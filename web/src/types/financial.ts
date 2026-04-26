export interface FinancialProduct {
  id: string;
  product_type: 'input_financing' | 'crop_insurance' | 'market_linkage' | 'savings';
  name: string;
  description: string;
  provider: string;
  min_amount: number;
  max_amount: number;
  interest_rate_annual: number | null;
  commission_pct: number | null;
}

export interface FarmerRiskScore {
  farmer_id: string;
  score: number;
  components: Record<string, number> | null;
  last_computed_at: string | null;
}

export interface ProductEligibility {
  farmer_id: string;
  risk_score: number;
  eligible_products: FinancialProduct[];
  ineligible_reasons: Record<string, string> | null;
}

export interface AnalyticsSummary {
  total_queries: number;
  avg_cost_per_query_usd_cents: number;
  total_cost_usd_cents: number;
  avg_input_tokens: number;
  avg_output_tokens: number;
  avg_latency_ms: number;
  cache_hit_rate_pct: number;
}
