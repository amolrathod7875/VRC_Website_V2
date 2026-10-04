import type { ChatAPIResponse, ChatSource, ChatRetrieval, CatalogueReference } from "./chatTypes";

const API_BASE =
  (process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1").replace(
    /\/$/,
    ""
  );

export async function sendChatMessage(
  message: string,
  conversationId?: string | null
): Promise<ChatAPIResponse> {
  const body: Record<string, unknown> = { message };
  if (conversationId) {
    body.conversation_id = conversationId;
  }

  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    let detail = "Something went wrong.";
    try {
      const err = await res.json();
      if (typeof err.detail === "string") detail = err.detail;
      else if (typeof err.detail === "object") detail = JSON.stringify(err.detail);
    } catch {
      // use default detail
    }
    throw new Error(detail);
  }

  const data = (await res.json()) as {
    conversation_id: string;
    answer: string;
    sources: ChatSource[];
    retrieval: ChatRetrieval | null;
    show_sources?: boolean;
    intent?: string | null;
    catalogues: CatalogueReference[];
    show_catalogues?: boolean;
  };

  return {
    conversation_id: data.conversation_id ?? "",
    answer: data.answer ?? "",
    sources: data.sources ?? [],
    retrieval: data.retrieval ?? null,
    show_sources: data.show_sources ?? true,
    intent: data.intent ?? null,
    catalogues: data.catalogues ?? [],
    show_catalogues: data.show_catalogues ?? false,
  };
}

export async function checkChatStatus(): Promise<{ rag_ready: boolean }> {
  const res = await fetch(`${API_BASE}/chat/status`, {
    method: "GET",
    headers: { Accept: "application/json" },
  });

  if (!res.ok) {
    return { rag_ready: false };
  }

  const data = (await res.json()) as { rag_ready?: unknown };
  return { rag_ready: Boolean(data.rag_ready) };
}
