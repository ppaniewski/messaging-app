import { getToken, refreshAccess } from "../helpers/authStore"

export async function authFetch(path: string, init: RequestInit = {}): Promise<Response> {
    let token = getToken()

    if (!token) {
        await refreshAccess()
        token = getToken()
    }

    const headers = new Headers(init.headers)
    headers.set("Authorization", `Bearer ${token}`)

    const res = await fetch(path, {
        ...init,
        headers,
        credentials: "same-origin"
    })

    if (res.status === 401) {
        await refreshAccess()
        token = getToken()
        if (!token) return res

        headers.set("Authorization", `Bearer ${token}`)

        return fetch(path, {
            ...init,
            headers,
            credentials: "same-origin"
        })
    }

    return res
}