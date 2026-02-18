import { useEffect, useState } from "react"
import socket from "../websocket/socket"
import type { User } from "../api/users"
import { onMessageReceived, onMessageDeleted, onConversationRead, onUserIsTyping } from "../websocket/chatEvents"
import { onFriendRequestReceived, onFriendRequestAccepted, onFriendRequestDeclined, onFriendRemoved } from "../websocket/friendEvents"
import { FriendsDataContext } from "../contexts/FriendsDataContext"
import type { Conversation } from "../api/conversations"
import { ChatsContext } from "../contexts/ChatsContext"

type Props = {
    children: React.ReactNode
}

const SocketProvider = ({ children }: Props) => {
    const [isConnected, setIsConnected] = useState(socket.connected)

    const [friends, setFriends] = useState<User[]>([])
    const [sentRequests, setSentRequests] = useState<User[]>([])
    const [receivedRequests, setReceivedRequests] = useState<User[]>([])

    const [chats, setChats] = useState<Conversation[]>([])
    const [refreshChats, setRefreshChats] = useState(false)

    useEffect(() => {
        function onConnect() {
            setIsConnected(true)
        }

        function onDisconnect() {
            setIsConnected(false)
        }

        const messageReceived = (data: any) => onMessageReceived(data, setChats)
        const messageDeleted = (data: any) => onMessageDeleted(data, setChats)
        const conversationRead = (data: any) => onConversationRead(data, setChats)
        const userIsTyping = (data: any) => onUserIsTyping(data)

        const friendAccepted = (data: any) => onFriendRequestAccepted(data, setFriends, setSentRequests, setRefreshChats)
        const friendDeclined = (data: any) => onFriendRequestDeclined(data, setSentRequests)
        const friendReceived = (data: any) => onFriendRequestReceived(data, setReceivedRequests)
        const friendRemoved = (data: any) => onFriendRemoved(data, setFriends, setRefreshChats)

        socket.on("connect", onConnect)
        socket.on("disconnect", onDisconnect)

        socket.on("message_received", messageReceived)
        socket.on("message_deleted", messageDeleted)
        socket.on("conversation_read", conversationRead)
        socket.on("user_is_typing", userIsTyping)

        socket.on("friend_request_accepted", friendAccepted)
        socket.on("friend_request_declined", friendDeclined)
        socket.on("friend_request_received", friendReceived)
        socket.on("friend_removed", friendRemoved)

        return () => {
            socket.off("connect", onConnect)
            socket.off("disconnect", onDisconnect)

            socket.off("message_received", messageReceived)
            socket.off("message_deleted", messageDeleted)
            socket.off("conversation_read", conversationRead)
            socket.off("user_is_typing", userIsTyping)

            socket.off("friend_request_accepted", friendAccepted)
            socket.off("friend_request_declined", friendDeclined)
            socket.off("friend_request_received", friendReceived)
            socket.off("friend_removed", friendRemoved)
        }
    }, [])
    
    return (
        <FriendsDataContext.Provider 
            value={{friends, setFriends, sentRequests, setSentRequests, receivedRequests, setReceivedRequests}}
        >
            <ChatsContext.Provider value={{chats, setChats, refreshChats, setRefreshChats}}>
                {children}
            </ChatsContext.Provider>
        </FriendsDataContext.Provider>
    )
}

export default SocketProvider