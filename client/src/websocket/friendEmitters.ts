import type { User } from "../api/users";
import socket, { ensureConnected } from "./socket";

const TIMEOUT = 5000

export async function acceptFriendRequest(
    friend: User,
    setFriends: React.Dispatch<React.SetStateAction<User[]>>,
    setReceivedRequests: React.Dispatch<React.SetStateAction<User[]>>,
    setRefreshChats: React.Dispatch<React.SetStateAction<boolean>>
) {
    await ensureConnected()

    try {
        const response = await socket.timeout(TIMEOUT).emitWithAck("accept_friend_request", friend.id)
        if (!response.ok) return

        setReceivedRequests(prev => prev.filter(u => u.id !== friend.id))
        setFriends(prev => [...prev, friend])
        setRefreshChats(true) // Refresh chats in case a new chat gets created
    }
    catch (err) {
        return
    }
}

export async function declineFriendRequest(
    friend: User,
    setReceivedRequests: React.Dispatch<React.SetStateAction<User[]>>
) {
    await ensureConnected()

    try {
        const response = await socket.timeout(TIMEOUT).emitWithAck("decline_friend_request", friend.id)
        if (!response.ok) return

        setReceivedRequests(prev => prev.filter(u => u.id !== friend.id))
    }
    catch (err) {
        return
    }
}

export async function sendFriendRequest(
    friend: User, 
    setSentRequests: React.Dispatch<React.SetStateAction<User[]>>
) {
    await ensureConnected()

    try {
        const response = await socket.timeout(TIMEOUT).emitWithAck("send_friend_request", friend.id)
        if (!response.ok) return

        setSentRequests(prev => [...prev, friend])
    }
    catch (err) {
        return
    }
}

export async function removeFriend(
    friend: User, 
    setFriends: React.Dispatch<React.SetStateAction<User[]>>,
    setRefreshChats: React.Dispatch<React.SetStateAction<boolean>>
) {
    await ensureConnected()

    try {
        const response = await socket.timeout(TIMEOUT).emitWithAck("remove_friend", friend.id)
        if (!response.ok) return

        setFriends(prev => prev.filter(f => f.id !== friend.id))
        setRefreshChats(true) // Refresh chats in case an empty chat gets deleted
    }
    catch (err) {
        return
    }
}