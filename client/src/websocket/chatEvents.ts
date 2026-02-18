import type { Conversation, Message } from "../api/conversations";

export function onMessageReceived(
    data: any, 
    setChats: React.Dispatch<React.SetStateAction<Conversation[]>>
) {
    const chatId = data.conversation_id
    const message: Message = {
        text: data.text,
        id: data.message_id,
        userId: data.user_id,
        isDeleted: data.is_deleted,
        createdAt: data.created_at
    }

    setChats(prev => prev.map(chat => 
        chat.id !== chatId ? chat : {
            ...chat,
            messages: [message, ...chat.messages], // Add message
            users: chat.users.map(u =>
                u.id === data.user_id ? u : {
                    ...u,
                    isUnread: true // Mark the conversation as unread for yourself
                }
            )
        }
    ))
}

export function onMessageDeleted(
    data: any, 
    setChats: React.Dispatch<React.SetStateAction<Conversation[]>>
) {
    const chatId = data.conversation_id
    const messageId = data.message_id
    const message: Message = {
        text: data.text,
        id: messageId, 
        userId: data.user_id,
        isDeleted: data.is_deleted,
        createdAt: data.created_at
    }

    setChats(prev => prev.map(chat => 
        chat.id !== chatId ? chat : {
            ...chat,
            messages: chat.messages.map(m =>
                m.id !== messageId ? m : message
            )
        }
    ))
}

export function onConversationRead(
    data: any, 
    setChats: React.Dispatch<React.SetStateAction<Conversation[]>>
) {
    const chatId = data.conversation_id
    const userId = data.user_id

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

export function onUserIsTyping(data: any) {
    
}