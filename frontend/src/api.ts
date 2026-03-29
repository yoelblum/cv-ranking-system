const BASE_URL = import.meta.env.VITE_API_URL || "";

interface GenerateResponse {
  message: string;
  count: number;
}

export interface RankedCandidate {
  id: string;
  name: string;
  title: string;
  years_experience: number;
  skills: string[];
  previous_experience: string;
  score: number;
  pros: string;
  cons: string;
}

interface RankResponse {
  candidates: RankedCandidate[];
}

async function request<T>(
  path: string,
  body: object,
  apiKey?: string
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (apiKey) {
    headers["X-API-Key"] = apiKey;
  }

  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }

  return res.json();
}

export async function generateCvs(
  jobDescription: string,
  apiKey?: string
): Promise<GenerateResponse> {
  return request<GenerateResponse>(
    "/api/generate-cvs",
    { job_description: jobDescription },
    apiKey
  );
}

export async function rankCvs(
  jobDescription: string,
  apiKey?: string
): Promise<RankedCandidate[]> {
  const data = await request<RankResponse>(
    "/api/rank-cvs",
    { job_description: jobDescription },
    apiKey
  );
  return data.candidates;
}
