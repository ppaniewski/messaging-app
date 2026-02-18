import { createContext, useContext } from "react";
import type { Conversation } from "../api/conversations";

export const ChatsContext = createContext<Chats | undefined>(undefined)

export const useChats = () => {
    const context = useContext(ChatsContext)
    if (context === undefined) {
        throw new Error("useChats must be used within SocketProvider")
    }

    return context
}

export interface Chats {
    chats: Conversation[]
    setChats: React.Dispatch<React.SetStateAction<Conversation[]>>
    refreshChats: boolean
    setRefreshChats: React.Dispatch<React.SetStateAction<boolean>>
}