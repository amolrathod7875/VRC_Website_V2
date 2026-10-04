"use client";

import type { ChatAPIResponse, ChatMessage, ChatSource, ChatRetrieval } from "@/lib/chatTypes";
import { checkChatStatus, sendChatMessage } from "@/lib/chatApi";
import { useEffect, useId, useRef, useState } from "react";

const SUGGESTED_PROMPTS = [
  "What is VR Coatings?",
  "What is Tiger used for?",
  "Tell me about Tiger 30:150.",
  "What is the pressure ratio of Tiger 30:150?",
];

const SESSION_KEY = "vr-coatings-conversation-id";

function cn(...classes: (string | false | null | undefined)[]) {
  return classes.filter(Boolean).join(" ");
}

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function renderMarkdown(text: string): string {
  const safe = escapeHtml(text);
  const lines = safe.split("\n");
  const out: string[] = [];
  let inList = false;
  let listType: "ul" | "ol" | null = null;

  const flushList = () => {
    if (inList) {
      out.push(listType === "ul" ? "</ul>" : "</ol>");
      inList = false;
      listType = null;
    }
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    if (trimmed === "") {
      flushList();
      out.push("<br/>");
      continue;
    }

    const orderedMatch = trimmed.match(/^(\d+)\.\s+(.*)$/);
    if (orderedMatch) {
      if (!inList || listType !== "ol") {
        flushList();
        out.push('<ol class="list-decimal pl-5 space-y-1 my-1">');
        inList = true;
        listType = "ol";
      }
      out.push(`<li>${inlineFormat(orderedMatch[2])}</li>`);
      continue;
    }

    if (trimmed.startsWith("- ")) {
      if (!inList || listType !== "ul") {
        flushList();
        out.push('<ul class="list-disc pl-5 space-y-1 my-1">');
        inList = true;
        listType = "ul";
      }
      out.push(`<li>${inlineFormat(trimmed.slice(2))}</li>`);
      continue;
    }

    flushList();
    out.push(`<p class="leading-6">${inlineFormat(trimmed)}</p>`);
  }

  flushList();
  return out.join("");
}

function inlineFormat(text: string): string {
  return text
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>");
}

function uid() {
  return Math.random().toString(36).slice(2, 11);
}

type ChatState =
  | { type: "idle" }
  | { type: "ready" }
  | { type: "open" }
  | { type: "loading" }
  | { type: "slow" }
  | { type: "error"; message: string };

export function ChatWidget() {
  const [status, setStatus] = useState<ChatState>({ type: "idle" });
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [open, setOpen] = useState(false);
  const [panelReady, setPanelReady] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);
  const slowTimerRef = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
  const messagesContainerRef = useRef<HTMLDivElement | null>(null);
  const inputId = useId();

  // Load conversation from sessionStorage on mount
  useEffect(() => {
    try {
      const stored = sessionStorage.getItem(SESSION_KEY);
      if (stored) setConversationId(stored);
    } catch {
      // sessionStorage unavailable
    }
  }, []);

  // Health check (runs once on mount)
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const result = await checkChatStatus();
        if (!cancelled) {
          setStatus(result.rag_ready ? { type: "ready" } : { type: "open" });
        }
      } catch {
        if (!cancelled) {
          setStatus({ type: "open" });
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  // Animate panel open
  useEffect(() => {
    if (open) {
      const t = setTimeout(() => setPanelReady(true), 10);
      return () => clearTimeout(t);
    } else {
      setPanelReady(false);
    }
  }, [open]);

  // Slow-response timer
  useEffect(() => {
    if (status.type === "loading") {
      slowTimerRef.current = setTimeout(() => {
        setStatus({ type: "slow" });
      }, 4000);
    }
    return () => {
      if (slowTimerRef.current) clearTimeout(slowTimerRef.current);
    };
  }, [status.type]);

  // Auto-scroll
  useEffect(() => {
    if (messagesEndRef.current) {
      const el = messagesEndRef.current;
      const container = messagesContainerRef.current;
      if (container) {
        const isNearBottom =
          container.scrollHeight - container.scrollTop - container.clientHeight < 120;
        if (isNearBottom) {
          el.scrollIntoView({ behavior: "smooth", block: "end" });
        }
      } else {
        el.scrollIntoView({ behavior: "smooth", block: "end" });
      }
    }
  }, [messages, status]);

  // Focus input when panel opens
  useEffect(() => {
    if (open && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 350);
    }
  }, [open]);

  // Escape key
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape" && open) {
        handleClose();
      }
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [open, messages, status, conversationId, input]);

  async function handleSubmit(text?: string) {
    const message = (text ?? input).trim();
    if (!message) return;
    if (status.type === "loading") return;

    const userMsg: ChatMessage = {
      id: uid(),
      role: "user",
      content: message,
      sources: [],
      retrieval: null,
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setStatus({ type: "loading" });

    try {
      const result: ChatAPIResponse = await sendChatMessage(message, conversationId);

      setConversationId(result.conversation_id);
      try {
        sessionStorage.setItem(SESSION_KEY, result.conversation_id);
      } catch {
        // sessionStorage unavailable
      }

      const assistantMsg: ChatMessage = {
        id: uid(),
        role: "assistant",
        content: result.answer,
        sources: result.sources,
        retrieval: result.retrieval,
        show_sources: result.show_sources,
        intent: result.intent,
      };

      setMessages((prev) => [...prev, assistantMsg]);
      setStatus({ type: "open" });
    } catch (err) {
      const assistantMsg: ChatMessage = {
        id: uid(),
        role: "assistant",
        content: "",
        sources: [],
        retrieval: null,
        error: "I'm having trouble reaching the VR Coatings knowledge service. Please try again.",
      };

      setMessages((prev) => [...prev, assistantMsg]);
      setStatus({ type: "error", message: err instanceof Error ? err.message : "Something went wrong." });
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  function handleSuggestionClick(prompt: string) {
    handleSubmit(prompt);
  }

  function handleRetry() {
    setStatus({ type: "loading" });
    const lastUserMsg = [...messages].reverse().find((m) => m.role === "user");
    if (lastUserMsg) {
      handleSubmit(lastUserMsg.content);
    } else {
      setStatus({ type: "open" });
    }
  }

  function handleClose() {
    setOpen(false);
    setPanelReady(false);
  }

  function handleNewChat() {
    setMessages([]);
    setConversationId(null);
    setInput("");
    setStatus({ type: "open" });
    try {
      sessionStorage.removeItem(SESSION_KEY);
    } catch {
      // sessionStorage unavailable
    }
    setTimeout(() => inputRef.current?.focus(), 350);
  }

  const isOpen = open;

  function renderSources(sources: ChatSource[]) {
    if (!sources.length) return null;

    return (
      <div className="mt-2 space-y-2">
        <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
          Sources
        </p>
        {sources.map((src, idx) => {
          const srcLabel = [src.section, src.model, src.page ? `Page ${src.page}` : null]
            .filter(Boolean)
            .join(" · ");

          return (
            <div
              key={idx}
              className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-xs"
            >
              <p className="font-medium text-slate-800">
                {src.document || "Unknown document"}
              </p>
              {srcLabel && (
                <p className="mt-0.5 text-slate-500">{srcLabel}</p>
              )}
              {src.url && (
                <a
                  href={src.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-1.5 inline-flex items-center gap-1 text-brand-700 hover:text-brand-800"
                >
                  Open catalogue
                  <svg
                    viewBox="0 0 20 20"
                    className="h-3 w-3"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth={2}
                  >
                    <path
                      d="M5 10h10M11 5l5 5-5 5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </a>
              )}
            </div>
          );
        })}
      </div>
    );
  }

  function renderMessage(msg: ChatMessage) {
    const isUser = msg.role === "user";

    return (
      <div
        className={cn(
          "flex w-full",
          isUser ? "justify-end" : "justify-start"
        )}
      >
        <div
          className={cn(
            "max-w-[88%] rounded-2xl px-4 py-3 text-sm leading-6",
            isUser
              ? "rounded-br-md bg-brand-700 text-white"
              : "rounded-bl-md bg-slate-50 text-slate-800"
          )}
        >
          {msg.error ? (
            <p className="text-sm text-red-700">{msg.error}</p>
          ) : (
            <>
              <div dangerouslySetInnerHTML={{ __html: renderMarkdown(msg.content) }} />
              {!isUser && msg.show_sources !== false && renderSources(msg.sources)}
            </>
          )}
        </div>
      </div>
    );
  }

  function renderContent() {
    if (status.type === "loading" || status.type === "slow") {
      return (
        <div className="flex justify-start">
          <div className="rounded-2xl rounded-bl-md bg-slate-50 px-4 py-3">
            <div className="flex items-center gap-2">
              <div className="flex gap-1">
                {[0, 1, 2].map((i) => (
                  <span
                    key={i}
                    className="h-2 w-2 rounded-full bg-slate-400"
                    style={{
                      animation: `chat-bounce 1.4s ease-in-out infinite`,
                      animationDelay: `${i * 0.18}s`,
                    }}
                  />
                ))}
              </div>
              <span className="text-xs text-slate-500">
                {status.type === "slow"
                  ? "Still working on your answer..."
                  : "Searching VR Coatings knowledge..."}
              </span>
            </div>
          </div>
        </div>
      );
    }

    if (messages.length === 0 && status.type !== "error") {
      return (
        <div className="flex flex-col items-center justify-center text-center px-4">
          <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-brand-50">
            <svg
              viewBox="0 0 24 24"
              className="h-6 w-6 text-brand-700"
              fill="none"
              stroke="currentColor"
              strokeWidth={1.8}
            >
              <path
                d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-5l-5 5v-5z"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
          <h3 className="mb-1 text-base font-semibold text-slate-900">
            Hello! I&apos;m the VR Coatings Assistant.
          </h3>
          <p className="mb-4 text-sm leading-6 text-slate-600">
            I can help you with VR Coatings products, technical specifications,
            applications, and company information.
          </p>
          <div className="flex flex-wrap justify-center gap-2">
            {SUGGESTED_PROMPTS.map((prompt) => (
              <button
                key={prompt}
                type="button"
                onClick={() => handleSuggestionClick(prompt)}
                className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 transition-colors duration-200 hover:border-brand-300 hover:text-brand-800"
              >
                {prompt}
              </button>
            ))}
          </div>
          {status.type === "ready" ? (
            <p className="mt-4 text-xs text-slate-400">
              Responses are based on the current VR Coatings knowledge base.
            </p>
          ) : (
            <p className="mt-4 text-xs text-amber-700">
              Knowledge service is still connecting. Some questions may not be
              available.
            </p>
          )}
        </div>
      );
    }

    if (messages.length === 0 && status.type === "error") {
      return (
        <div className="flex flex-col items-center justify-center text-center px-4">
          <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-red-50">
            <svg
              viewBox="0 0 24 24"
              className="h-6 w-6 text-red-600"
              fill="none"
              stroke="currentColor"
              strokeWidth={1.8}
            >
              <path
                d="M12 9v4M12 17h.01M12 4a9 9 0 1 0 0 18 9 9 0 0 0 0-18z"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
          <p className="text-sm text-red-700">
            I&apos;m having trouble reaching the VR Coatings knowledge service.
          </p>
          <button
            type="button"
            onClick={handleRetry}
            className="mt-3 rounded-full bg-brand-700 px-4 py-1.5 text-sm font-semibold text-white transition-colors hover:bg-brand-800"
          >
            Retry
          </button>
        </div>
      );
    }

    return null;
  }

  const hasMessages = messages.length > 0;
  const isAvailable = ["ready", "open", "error", "loading", "slow"].includes(status.type);

  return (
    <>
      {!isOpen && isAvailable && (
        <button
          type="button"
          onClick={() => setOpen(true)}
          aria-label="Open VR Coatings Assistant"
          className={cn(
            "fixed bottom-7 right-7 z-40 flex h-14 w-14 items-center justify-center rounded-full",
            "bg-brand-700 text-white shadow-lg transition-all duration-300",
            "hover:scale-105 hover:shadow-xl active:scale-95"
          )}
        >
          <svg
            viewBox="0 0 24 24"
            className="h-6 w-6"
            fill="none"
            stroke="currentColor"
            strokeWidth={1.8}
          >
            <path
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-5l-5 5v-5z"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span className="absolute -right-1 -top-1 h-4 w-4 rounded-full bg-green-500 ring-2 ring-white" />
        </button>
      )}

      {isOpen && (
        <div
          className={cn(
            "fixed inset-0 z-50",
            "md:hidden",
            panelReady ? "bg-black/30 backdrop-blur-sm" : "bg-transparent"
          )}
          onClick={handleClose}
          aria-hidden={!panelReady}
        />
      )}

      {isOpen && (
        <div
          role="dialog"
          aria-label="VR Coatings Assistant"
          className={cn(
            "fixed z-50 flex flex-col overflow-hidden",
            "rounded-2xl border border-slate-200 bg-white shadow-2xl",
            "bottom-4 right-4 left-4 top-4 md:inset-auto md:bottom-7 md:right-7",
            "md:w-[410px] md:h-[620px]",
            "transition-all duration-300 ease-out",
            panelReady
              ? "opacity-100 scale-100 translate-y-0"
              : "opacity-0 scale-95 translate-y-3"
          )}
        >
          <div className="flex shrink-0 items-center justify-between bg-brand-700 px-5 py-3.5">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-white/15">
                <svg
                  viewBox="0 0 24 24"
                  className="h-5 w-5 text-white"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth={1.8}
                >
                  <path
                    d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-5l-5 5v-5z"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </div>
              <div>
                <h2 className="text-sm font-semibold text-white">
                  VR Coatings Assistant
                </h2>
                <p className="text-xs text-white/70">
                  Ask about our products, applications and company information.
                </p>
              </div>
            </div>
            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={handleNewChat}
                aria-label="Start new chat"
                className="mr-1 flex h-7 items-center justify-center rounded-md px-2 text-xs font-medium text-white/80 transition-colors hover:bg-white/15 hover:text-white"
              >
                New chat
              </button>
              <span
                className={cn(
                  "mr-1 h-2 w-2 rounded-full",
                  status.type === "loading" || status.type === "slow"
                    ? "bg-amber-300 animate-pulse"
                    : "bg-green-300"
                )}
                aria-hidden
              />
              <button
                type="button"
                onClick={handleClose}
                aria-label="Close VR Coatings Assistant"
                className="flex h-8 w-8 items-center justify-center rounded-md text-white/80 transition-colors hover:bg-white/15 hover:text-white"
              >
                <svg
                  viewBox="0 0 20 20"
                  className="h-4 w-4"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    d="M6 6l8 8M14 6l-8 8"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </button>
            </div>
          </div>

          <div
            ref={messagesContainerRef}
            className="flex-1 overflow-y-auto px-4 py-4"
          >
            {renderContent()}
            <div className="space-y-3">
              {messages.map((msg) => (
                <div key={msg.id}>
                  {renderMessage(msg)}
                </div>
              ))}
            </div>
            <div ref={messagesEndRef} />
          </div>

          {isOpen && (
            <div className="shrink-0 border-t border-slate-200 bg-white px-4 py-3">
              {(status.type === "loading" || status.type === "slow") && (
                <p className="mb-1.5 text-xs text-slate-500">
                  {status.type === "slow"
                    ? "Still working on your answer..."
                    : "Searching VR Coatings knowledge..."}
                </p>
              )}
              {status.type === "error" && (
                <div className="mb-2 flex items-center justify-between rounded-lg bg-red-50 px-3 py-2">
                  <span className="text-xs text-red-700">
                    Unable to reach the knowledge service.
                  </span>
                  <button
                    type="button"
                    onClick={handleRetry}
                    className="text-xs font-semibold text-brand-700 hover:text-brand-800"
                  >
                    Retry
                  </button>
                </div>
              )}
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleSubmit();
                }}
                className="flex items-end gap-2"
              >
                <label htmlFor={inputId} className="sr-only">
                  Ask a question
                </label>
                <textarea
                  ref={inputRef}
                  id={inputId}
                  rows={1}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask about VR Coatings products..."
                  className="max-h-28 min-h-[40px] flex-1 resize-y rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-800 outline-none transition-colors placeholder:text-slate-400 focus:border-brand-400 focus:bg-white"
                  disabled={status.type === "loading" || status.type === "slow"}
                />
                <button
                  type="submit"
                  disabled={
                    !input.trim() ||
                    status.type === "loading" ||
                    status.type === "slow"
                  }
                  aria-label="Send message"
                  className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-brand-700 text-white transition-colors hover:bg-brand-800 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  <svg
                    viewBox="0 0 20 20"
                    className="h-4 w-4"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth={2}
                  >
                    <path
                      d="M3 10h14M13 6l4 4-4 4"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </button>
              </form>
            </div>
          )}
        </div>
      )}
    </>
  );
}
