export async function fetchUnitEconomics(days = 30) {
  const res = await fetch(`/api/analytics/unit-economics?days=${days}`);
  return res.json();
}

export async function fetchIntentDistribution(days = 30) {
  const res = await fetch(`/api/analytics/intents?days=${days}`);
  return res.json();
}

export async function fetchQueryVolume(days = 30) {
  const res = await fetch(`/api/analytics/queries?days=${days}`);
  return res.json();
}

export async function fetchEscalationRate(days = 30) {
  const res = await fetch(`/api/analytics/escalation-rate?days=${days}`);
  return res.json();
}

export async function fetchFunnel() {
  const res = await fetch('/api/analytics/funnel');
  return res.json();
}
