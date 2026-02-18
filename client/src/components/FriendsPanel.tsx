import { useOutletContext } from "react-router-dom"
import { Heading, Stack } from "@chakra-ui/react"
import FriendEntry from "./FriendEntry"
import FriendRequest from "./FriendRequest"
import type { DashboardOutletContext } from "../contexts/DashboardOutletContext"

const FriendsPanel = () => {
    const { friends, setFriends, receivedRequests, setReceivedRequests }: DashboardOutletContext = useOutletContext()
    
    const friendRequestList = receivedRequests.map(user => {
        return <FriendRequest 
                    key={user.id} user={user} setFriends={setFriends} setReceivedRequests={setReceivedRequests} 
                />
    })

    const friendList = friends.map(friend => {
        return <FriendEntry key={friend.id} friend={friend} setFriends={setFriends} />
    })

    return (
        <Stack 
            bg="bg.panel" mt="0.5vh" 
            w={["40%", "40%", "40%", "35%", "30%"]} px={4} pt={3} 
            rounded="xl" borderColor="border" borderWidth={1}
        >
            <Heading fontWeight="bold" size="2xl">Friend Requests</Heading>
            <Stack>
                {friendRequestList.length >= 1 ? friendRequestList : 
                    <Heading alignSelf="center" size="md" fontWeight="light">You have no new friend requests</Heading>}
            </Stack>
            <Heading fontWeight="bold" size="2xl">Friends</Heading>
            <Stack>
                {friendList}
            </Stack>
        </Stack>
    )
}

export default FriendsPanel