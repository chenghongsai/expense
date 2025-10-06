import { loadToken } from "./auth";
const BASE = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000";

function authHeaders() {
  const t = loadToken();
  if (!t) throw new Error("Not authenticated");
  return { Authorization: `Bearer ${t}`, "Content-Type": "application/json" };
}

export type Role = "EMPLOYEE" | "EMPLOYER";

export type Ticket = {
  id: number;
  owner_id: number;
  spent_at: string;          // ISO string
  amount: string | number;   // 后端可能返回字符串（Decimal），显示时转成 number
  link?: string | null;
  description?: string | null;
  status: "PENDING" | "APPROVED" | "DENIED";
};

export async function getMyTickets(): Promise<Ticket[]> {
  const res = await fetch(`${BASE}/tickets/me`, { headers: authHeaders() });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getAllTickets(): Promise<Ticket[]> {
  const res = await fetch(`${BASE}/tickets`, { headers: authHeaders() });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function createTicket(input: {
  spent_at: string;  // ISO
  amount: number;    // number 即可，后端会转 Decimal
  link?: string;
  description?: string;
}): Promise<Ticket> {
  const res = await fetch(`${BASE}/tickets`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(input),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function approveTicket(id: number) {
  const res = await fetch(`${BASE}/admin/tickets/${id}/approve`, {
    method: "POST",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error(await res.text());
}

export async function denyTicket(id: number) {
  const res = await fetch(`${BASE}/admin/tickets/${id}/deny`, {
    method: "POST",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error(await res.text());
}

export async function login(email:string, password: string){
    const res = await fetch(`${BASE}/auth/login`,{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({email,password}),
    });
    if(!res.ok){
        const err = await res.json().catch(() => ({}));
        throw {status: res.status, detail:err?.detail ?? "Login failed"};
    }
    return (await res.json()) as {access_token:string; token_type: string};
}

export async function register(email:string, password:string, role:Role){
    const res = await fetch(`${BASE}/auth/register`,{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({email,password,role}),
    });
    if(!res.ok){
        const err = await res.json().catch(() => ({}));
        throw {status:res.status,detail:err?.detail ?? "Register failed"};
    }
    return (await res.json()) as {access_token:string;token_type:string};
}