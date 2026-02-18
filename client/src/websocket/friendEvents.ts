import type { User } from "../api/users";

export function onFriendRequestAccepted(
    data: any, 
    setFriends: React.Dispatch<React.SetStateAction<User[]>>,
    setSentRequests: React.Dispatch<React.SetStateAction<User[]>>,
    setRefreshChats: React.Dispatch<React.SetStateAction<boolean>>
) {
    const user: User = {
        id: data.user_id,
        username: data.username
    }

    setSentRequests(prev => prev.filter(u => u.id !== user.id))
    setFriends(prev => [...prev, user])
    setRefreshChats(true) // Refresh chats in case a new chat gets created
}

export function onFriendRequestDeclined(
    data: any,
    setSentRequests: React.Dispatch<React.SetStateAction<User[]>>
) {
    setSentRequests(prev => prev.filter(u => u.id !== data.user_id))
}

export function onFriendRequestReceived(
    data: any,
    setReceivedRequests: React.Dispatch<React.SetStateAction<User[]>>
) {
    const user: User = {
        id: data.user_id,
        username: data.username
    }

    setReceivedRequests(prev => [...prev, user])
}

export function onFriendRemoved(
   data: any,
   setFriends: React.Dispatch<React.SetStateAction<User[]>>,
   setRefreshChats: React.Dispatch<React.SetStateAction<boolean>>
) {
    setFriends(prev => prev.filter(u => u.id !== data.user_id))
    setRefreshChats(true) // Refresh chats in case an empty chat gets deleted
}