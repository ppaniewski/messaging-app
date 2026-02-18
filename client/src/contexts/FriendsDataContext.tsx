import { createContext, useContext } from "react"
import type { User } from "../api/users"

export const FriendsDataContext = createContext<FriendsData | undefined>(undefined)

export const useFriendsData = () => {
    const context = useContext(FriendsDataContext)
    if (context === undefined) {
        throw new Error("useFriendsData must be used within SocketProvider")
    }

    return context
}

export interface FriendsData {
    friends: User[]
    setFriends: React.Dispatch<React.SetStateAction<User[]>>
    sentRequests: User[]
    setSentRequests: React.Dispatch<React.SetStateAction<User[]>>
    receivedRequests: User[]
    setReceivedRequests: React.Dispatch<React.SetStateAction<User[]>>
}