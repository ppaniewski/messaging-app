import { ensureConnected, disconnectSocket } from "../websocket/socket"

let accessToken: string | null = null
let refreshPromise: Promise<UserOutLogin | null> | null = null
let userId: number | null = null
let username: string | null = null

refreshAccess()

interface UserOutLogin {
    accessToken: string
    id: number
    username: string
}

export function getToken(): string | null {
    return accessToken
}

export async function getUserData() {
    if (userId && username) {
        return { userId, username }
    }

    await refreshAccess()

    return { userId, username }
} 

export function isAuthenticated(): boolean {
    return accessToken != null
}

export async function refreshAccess() {
    const data = await refreshAccessOnce()
    if (!data) return

    accessToken = data.accessToken
    userId = data.id
    username = data.username

    ensureConnected()
}

function refreshAccessOnce(): Promise<UserOutLogin | null> {
    if (!refreshPromise) {
        refreshPromise = doRefresh()
        refreshPromise.finally(() => {
            refreshPromise = null
        })        
    }

    return refreshPromise
}

async function doRefresh(): Promise<UserOutLogin | null> {
    const res = await fetch("/api/auth/refresh", {
        method: "POST",
        credentials: "include"
    })

    if (!res.ok) return null

    const data = await res.json()
    return data
}

export async function loginUser(username: string, password: string): Promise<Response> {
    const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username,
            password
        })
    })

    if (!res.ok) {
        return res
    }

    const data: UserOutLogin = await res.json()
    accessToken = data.accessToken
    userId = data.id
    username = data.username

    ensureConnected()
    
    return res
}

export async function logoutUser(): Promise<Response> {
    const res = await fetch("/api/auth/logout", {
        method: "POST"
    })

    if (!res.ok) {
        return res
    }

    accessToken = null

    disconnectSocket()

    return res
}