import type { FinancialProduct, FarmerRiskScore, ProductEligibility } from '../types/financial';

export async function fetchAllProducts(): Promise<FinancialProduct[]> {
  const res = await fetch('/api/financial/products');
  return res.json();
}

export async function fetchEligibleProducts(farmerId: string): Promise<ProductEligibility> {
  const res = await fetch(`/api/financial/products/${farmerId}`);
  return res.json();
}

export async function fetchRiskScore(farmerId: string): Promise<FarmerRiskScore> {
  const res = await fetch(`/api/financial/risk-score/${farmerId}`);
  return res.json();
}
