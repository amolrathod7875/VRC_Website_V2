import type { ChatAPIResponse, ChatSource, ChatRetrieval, CatalogueReference, HistoryMessage, ChatMessage } from "./chatTypes";

const API_BASE =
  (process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1").replace(
    /\/$/,
    ""
  );

const MAX_HISTORY_MESSAGES = 8;

function formatHistoryForBackend(messages: ChatMessage[]): HistoryMessage[] {
  return messages.slice(-MAX_HISTORY_MESSAGES).map((msg) => ({
    role: msg.role,
    content: msg.content,
    sources: msg.sources,
    retrieval_metadata: msg.retrieval
      ? {
          chunks_used: msg.retrieval.chunks_used,
          retrieval_duration_ms: msg.retrieval.retrieval_duration_ms,
          generation_duration_ms: msg.retrieval.generation_duration_ms,
          total_duration_ms: msg.retrieval.total_duration_ms,
        }
      : undefined,
  }));
}

export async function sendChatMessage(
  message: string,
  conversationId?: string | null,
  history?: ChatMessage[],
  signal?: AbortSignal
): Promise<ChatAPIResponse> {
  const body: Record<string, unknown> = { message };
  if (conversationId) {
    body.conversation_id = conversationId;
  }
  if (history && history.length > 0) {
    body.history = formatHistoryForBackend(history);
  }

  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
    signal,
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
    const error = new Error(detail) as Error & { status?: number };
    error.status = res.status;
    throw error;
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