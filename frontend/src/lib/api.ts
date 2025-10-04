export type Role = "EMPLOYEE" | "EMPLOYER";

const BASE = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000";

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