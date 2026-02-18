import { authFetch } from "./authFetch";
import { type ConversationUser } from "./users";

export interface Message {
    text: string
    id: number
    userId: number
    isDeleted: boolean
    createdAt: string
}

export interface Conversation {
    id: number
    isGroupChat: boolean
    name?: string
    messages: Message[]
    users: ConversationUser[]
}

export async function getConversations(
    messageLimit: number = 20, 
    limit?: number, 
    offset?: number
) {
    let path = `/api/conversations?message_limit=${messageLimit}`
    if (limit) path += `&limit=${limit}`
    if (offset) path += `&offset=${offset}`

    return authFetch(path)
}

export async function getConversationMessages(
    conversationId: number,
    offset: number,
    amount: number = 15
) {
    return authFetch(`/api/conversations/${conversationId}?offset=${offset}&amount=${amount}`)
}