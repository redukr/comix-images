const API_BASE = "/api";

export interface ComicRequest {
  rank_from: string;
  rank_to: string;
  use_comfy: boolean;
  use_joj_cards: boolean;
}

export async function generateComic(request: ComicRequest) {
  const response = await fetch(`${API_BASE}/comic/build`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to generate comic");
  }

  return response.json();
}

export async function checkStatus(jobId: string) {
  const response = await fetch(`${API_BASE}/comic/status/${jobId}`);
  
  if (!response.ok) {
    throw new Error("Failed to check status");
  }

  return response.json();
}

export async function getRanks() {
  const response = await fetch(`${API_BASE}/joj/ranks`);
  
  if (!response.ok) {
    throw new Error("Failed to load ranks");
  }

  return response.json();
}

export async function getCards(category?: string) {
  const url = category
    ? `${API_BASE}/joj/cards?category=${category}`
    : `${API_BASE}/joj/cards`;
  
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error("Failed to load cards");
  }

  return response.json();
}
