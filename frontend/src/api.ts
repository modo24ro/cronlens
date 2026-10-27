export interface FieldInfo {
  name: string;
  source: string;
  values: number[];
}

export interface ExplainResponse {
  expression: string;
  description: string;
  fields: FieldInfo[];
  next_runs: string[];
}

export class CronError extends Error {
  constructor(
    message: string,
    public field: string | null,
  ) {
    super(message);
  }
}

export async function explain(expression: string, count = 10): Promise<ExplainResponse> {
  const response = await fetch("/api/explain", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ expression, count }),
  });
  if (response.ok) {
    return (await response.json()) as ExplainResponse;
  }
  const body = await response.json().catch(() => null);
  const detail = body?.detail;
  if (detail && typeof detail === "object" && "message" in detail) {
    throw new CronError(detail.message, detail.field ?? null);
  }
  throw new CronError(`Request failed (${response.status})`, null);
}
