import { Box, Stack } from "@chakra-ui/react"
import { type User } from "../api/users"
import { useEffect, useRef } from "react"
import UserEntry from "./UserEntry"
import FriendEntry from "./FriendEntry"
import RequestSent from "./RequestSent"
import FriendRequest from "./FriendRequest"

type Props = { 
    users: User[]
    loadMoreUsersRef: React.RefObject<(() => Promise<void>) | null>
    friends: User[]
    setFriends: React.Dispatch<React.SetStateAction<User[]>>
    receivedRequests: User[]
    setReceivedRequests: React.Dispatch<React.SetStateAction<User[]>>
    sentRequests: User[]
    setSentRequests: React.Dispatch<React.SetStateAction<User[]>>
}

const UserList = ({ users, friends, setFriends, receivedRequests, 
    setReceivedRequests, sentRequests, setSentRequests, loadMoreUsersRef 
}: Props) => {
    const stackRef = useRef<HTMLDivElement | null>(null)
    const bottomRef = useRef<HTMLDivElement | null>(null)

    useEffect(() => {
        const stack = stackRef.current
        const bottom = bottomRef.current

        if (!stack || !bottom) return

        const observer = new IntersectionObserver(
            ([entry]) => {
                if (!loadMoreUsersRef.current) return
                if (entry.isIntersecting) loadMoreUsersRef.current()
            },
            { root: stack }
        )

        observer.observe(bottom)
        return () => observer.disconnect()
    }, [loadMoreUsersRef.current])

    const userList = users.map(user => {
        const isFriends = friends.some(u => u.id === user.id)
        if (isFriends) return <FriendEntry key={user.id} friend={user} setFriends={setFriends} />

        const requestSent = sentRequests.some(u => u.id === user.id)
        if (requestSent) return <RequestSent key={user.id} user={user} />

        const requestReceived = receivedRequests.some(u => u.id === user.id)
        if (requestReceived) return <FriendRequest key={user.id} user={user} 
            setFriends={setFriends} setReceivedRequests={setReceivedRequests} />

        return <UserEntry user={user} key={user.id} setSentRequests={setSentRequests} />
    })

    return (
        <Stack ref={stackRef} overflowY="auto" gap={0}>
            {userList}
            <Box ref={bottomRef} h="1px" minH="1px" flexShrink={0}></Box>
        </Stack>
    )
}

export default UserList