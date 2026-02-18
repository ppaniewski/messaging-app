import { authFetch } from "./authFetch";

export async function registerUser(username: string, password: string) {
    return fetch("/api/auth/register",  {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username,
            password
        })
    })
}

export async function verifyUser() {
    return authFetch("/api/auth/verify", {
        method: "POST"
    })
}