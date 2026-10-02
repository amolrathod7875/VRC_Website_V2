export interface ChatSource {
  source_type?: string | null;
  document?: string | null;
  product?: string | null;
  product_slug?: string | null;
  section?: string | null;
  page?: number | null;
  model?: string | null;
  url?: string | null;
  line_start?: number | null;
  line_end?: number | null;
  verification_status?: string | null;
  authority_priority?: number | null;
}

export interface ChatRetrieval {
  chunks_used: number;
  retrieval_duration_ms?: number | null;
  generation_duration_ms?: number | null;
  total_duration_ms?: number | null;
}

export interface ChatAPIResponse {
  conversation_id: string;
  answer: string;
  sources: ChatSource[];
  retrieval: ChatRetrieval | null;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources: ChatSource[];
  retrieval: ChatRetrieval | null;
  error?: string;
}
