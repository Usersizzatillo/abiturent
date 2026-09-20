export const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

export class ApiError extends Error {
  status: number;
  detail: unknown;

  constructor(status: number, detail: unknown) {
    super(typeof detail === "string" ? detail : "API error");
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

function getCsrfToken(): string | null {
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : null;
}

async function ensureCsrfToken(): Promise<string | null> {
  const existing = getCsrfToken();
  if (existing) return existing;
  try {
    await fetch(`${API_BASE}/auth/csrf/`, { credentials: "include" });
  } catch {
    // ignore
  }
  return getCsrfToken();
}

export async function api<T = unknown>(
  path: string,
  options: RequestInit & { skipCsrf?: boolean } = {}
): Promise<T> {
  const { skipCsrf, ...init } = options;
  const headers = new Headers(init.headers);

  if (init.body) {
    headers.set("Content-Type", "application/json");
  }

  if (!skipCsrf && init.method && !["GET", "HEAD", "OPTIONS"].includes(init.method)) {
    const token = await ensureCsrfToken();
    if (token) headers.set("X-CSRFToken", token);
  }

  const res = await fetch(`${API_BASE}${path}`, {
    credentials: "include",
    ...init,
    headers,
  });

  if (res.status === 204) {
    return undefined as T;
  }

  let body: unknown = null;
  const text = await res.text();
  if (text) {
    try {
      body = JSON.parse(text);
    } catch {
      body = text;
    }
  }

  if (!res.ok) {
    const detail =
      body && typeof body === "object" && "detail" in body
        ? (body as { detail: unknown }).detail
        : body;
    throw new ApiError(res.status, detail);
  }

  return body as T;
}

export interface CurrentUser {
  id: number;
  username: string;
  email: string;
  role: "student" | "teacher" | "admin";
  phone: string;
  first_name: string;
  last_name: string;
  date_joined: string;
  is_staff: boolean;
}

export function extractFieldError(
  detail: unknown,
  field?: string
): string | null {
  if (field && typeof detail === "object" && detail !== null) {
    const obj = detail as Record<string, unknown>;
    const value = obj[field];
    if (Array.isArray(value) && value.length > 0) return String(value[0]);
    if (typeof value === "string") return value;
  }
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail) && detail.length > 0) return String(detail[0]);
  return null;
}

export async function fetchUser(): Promise<CurrentUser | null> {
  try {
    return await api<CurrentUser>("/auth/me/");
  } catch (e) {
    if (e instanceof ApiError && (e.status === 401 || e.status === 403)) {
      return null;
    }
    throw e;
  }
}