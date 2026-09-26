const BACKEND_ORIGIN =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export function getMediaUrl(path?: string | null): string {
  if (!path) return "";

  if (path.startsWith("http://") || path.startsWith("https://")) {
    return path;
  }

  const normalized = path.startsWith("/") ? path : `/${path}`;

  return `${BACKEND_ORIGIN}${normalized}`;
}
