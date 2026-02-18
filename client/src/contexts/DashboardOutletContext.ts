import type { User } from "../api/users";

export interface DashboardOutletContext {
    selectedChatId: number | null
    setSelectedChatId: React.Dispatch<React.SetStateAction<number | null>>
    friends: User[]
    setFriends: React.Dispatch<React.SetStateAction<User[]>>
    sentRequests: User[]
    setSentRequests: React.Dispatch<React.SetStateAction<User[]>>
    receivedRequests: User[]
    setReceivedRequests: React.Dispatch<React.SetStateAction<User[]>>
}