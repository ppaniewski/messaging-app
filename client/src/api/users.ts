import { authFetch } from "./authFetch";

export interface User {
    id: number
    username: string
}

export interface ConversationUser extends User {
    isUnread: boolean
}

export async function getUsers(matchString?: string, limit?: number, offset: number = 0) {
    let path = `/api/users?offset=${offset}`
    
    if (limit) {
        path += `&limit=${limit}`
    }

    if (matchString) {
        path += `&match_string=${matchString}`
    }

    return authFetch(path)
}

export async function getFriends() {
    return authFetch("/api/users/friends")
}

export async function getSentRequests() {
    return authFetch("/api/users/friends/sent_requests")
}

export async function getReceivedRequests() {
    return authFetch("/api/users/friends/received_requests")
}

export async function sendFriendRequest(user: User) {
    return authFetch(`/api/users/friends/add/${user.id}`, {
        method: "POST"
    })
}

export async function removeFriend(user: User) {
    return authFetch(`/api/users/friends/remove/${user.id}`, {
        method: "DELETE"    
    })
}

export async function acceptFriendRequest(user: User) {
    return authFetch(`/api/users/friends/accept_request/${user.id}`, {
        method: "POST"
    })
}

export async function declineFriendRequest(user: User) {
    return authFetch(`/api/users/friends/decline_request/${user.id}`, {
        method: "POST"
    })
}