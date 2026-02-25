import socket, { ensureConnected } from "./socket";
import type { Conversation, Message } from "../api/conversations";

const TIMEOUT = 5000

export async function sendMessage(
    text: string,
    recipientId: number,
    setChats: React.Dispatch<React.SetStateAction<Conversation[]>>
) {
    await ensureConnected()

    try {
        const response = await socket.timeout(TIMEOUT).emitWithAck("send_message", text, recipientId)
        if (!response.ok) return

        const data = response.data
        const newMessage: Message = {
            text: data.text,
            id: data.message_id,
            userId: data.user_id,
            isDeleted: data.is_deleted,
            createdAt: data.created_at
        }

        setChats(prev => prev.map(chat => 
            chat.id !== data.conversation_id ? chat : {
                ...chat,
                messages: [newMessage, ...chat.messages],
                users: chat.users.map(u =>
                    u.id !== recipientId ? u : {
                        ...u,
                        isUnread: true // Mark it as unread for the recipient
                    }
                )
            }
        ))
    }
    catch (err) {
        return
    }
}

export async function deleteMessage(messageId: number) {
    await ensureConnected()

    try {
        const response = await socket.timeout(TIMEOUT).emitWithAck("delete_message", messageId)
        if (!response.ok) return
    }
    catch (err) {
        return
    }
}

export async function markConversationRead(
    chatId: number,
    userId: number,
    setChats: React.Dispatch<React.SetStateAction<Conversation[]>>
) {
    await ensureConnected()

    try {
        const response = await socket.timeout(TIMEOUT).emitWithAck("mark_conversation_read", chatId)
        if (!response.ok) return

        setChats(prev => prev.map(chat => 
            chat.id !== chatId ? chat : {
                ...chat,
                users: chat.users.map(u => 
                    u.id !== userId ? u : {
                        ...u,
                        isUnread: false
                    }
                )
            }
        ))
    }   
    catch (err) {
        return
    }
}

export async function isTyping(
    conversationId: number
) {
    await ensureConnected()

    try {
        const response = await socket.timeout(TIMEOUT).emitWithAck("is_typing", conversationId)
        if (!response.ok) return
    }
    catch (err) {
        return
    }
}