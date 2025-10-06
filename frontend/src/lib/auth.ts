// src/lib/auth.ts
export function saveToken(token: string) {
  localStorage.setItem("token", token);
}
export function loadToken() {
  return localStorage.getItem("token");
}

// base64url -> base64
function b64urlToB64(s: string) {
  return s.replace(/-/g, "+").replace(/_/g, "/") + "===".slice((s.length + 3) % 4);
}

export type JwtPayload = { sub: string; role?: "EMPLOYEE" | "EMPLOYER"; [k: string]: any };

export function parseJwt(token: string): JwtPayload | null {
  try {
    const [, payload] = token.split(".");
    const json = atob(b64urlToB64(payload));
    return JSON.parse(json);
  } catch {
    return null;
  }
}

export function getCurrentRole(): "EMPLOYEE" | "EMPLOYER" | null {
  const t = loadToken();
  if (!t) return null;
  const p = parseJwt(t);
  return (p?.role as any) ?? null;
}
