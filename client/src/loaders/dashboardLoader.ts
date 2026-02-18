import { getConversations, type Conversation } from "../api/conversations"
import { getFriends, getReceivedRequests, getSentRequests, type User } from "../api/users"
import type { UserData } from "../contexts/UserDataContext"
import { getUserData } from "../helpers/authStore"

export interface DashboardLoader {
    userData: UserData
    chatsInit: Conversation[]
    friendsInit: User[]
    sentRequestsInit: User[]
    receivedRequestsInit: User[]
}

const dashboardLoader = async () => {
    const userData = await getUserData()
    if (!userData.userId || !userData.username) {
        throw new Response("Failed to load user data", { status: 500 })
    }

    const chatRes = await getConversations()
    if (!chatRes.ok) {
        throw new Response("Failed to load conversations", { status: chatRes.status })
    }

    const friendRes = await getFriends()
    const sentRequestsRes = await getSentRequests()
    const receivedRequestsRes = await getReceivedRequests()

    if (!friendRes.ok) {
        throw new Response("Failed to load friends", { status: friendRes.status })
    }
    if (!sentRequestsRes.ok) {
        throw new Response("Failed to load sent friend requests", { status: sentRequestsRes.status })
    }
    if (!receivedRequestsRes.ok) {
        throw new Response("Failed to load received friend requests", { status: receivedRequestsRes.status })
    }

    const chatsInit = await chatRes.json()
    const friendsInit = await friendRes.json()
    const sentRequestsInit = await sentRequestsRes.json()
    const receivedRequestsInit = await receivedRequestsRes.json()

    return {
        userData,
        chatsInit,
        friendsInit,
        sentRequestsInit,
        receivedRequestsInit
    }
}

export default dashboardLoader