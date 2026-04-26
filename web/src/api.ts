import type { LimiMessage, QueryResponse } from './types';

/**
 * Send an advisory query to the Limi API.
 * Proxied through Vite dev server → FastAPI on port 8000.
 */
export async function sendQuery(message: LimiMessage): Promise<QueryResponse> {
  const response = await fetch('/api/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(message),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`API error ${response.status}: ${detail}`);
  }

  return response.json();
}

/** Health check. */
export async function checkHealth(): Promise<{ status: string }> {
  const response = await fetch('/health');
  return response.json();
}
