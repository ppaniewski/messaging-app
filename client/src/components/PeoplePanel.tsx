import { useState, useRef } from "react" 
import { Stack, Heading } from "@chakra-ui/react"
import { type User } from "../api/users"
import { useOutletContext } from "react-router-dom"
import UserSearch from "./UserSearch"
import UserList from "./UserList"
import type { DashboardOutletContext } from "../contexts/DashboardOutletContext"

const PeoplePanel = () => {
    const { friends, setFriends, receivedRequests, setReceivedRequests, 
        sentRequests, setSentRequests }: DashboardOutletContext = useOutletContext()

    const [users, setUsers] = useState<User[]>([])
    const loadMoreUsersRef = useRef<(() => Promise<void>) | null>(null)

    return (
        <>
            <Stack 
                bg="bg.panel" mt="0.5vh" 
                w={["40%", "40%", "40%", "35%", "30%"]} px={4} pt={3} 
                rounded="xl" borderColor="border" borderWidth={1}
            >
                <Heading fontWeight="bold" size="2xl" mb={2}>People</Heading>

                <UserSearch setUsers={setUsers} loadMoreUsersRef={loadMoreUsersRef} />
                <UserList 
                    users={users} loadMoreUsersRef={loadMoreUsersRef} friends={friends} setFriends={setFriends} 
                    receivedRequests={receivedRequests} setReceivedRequests={setReceivedRequests} 
                    sentRequests={sentRequests} setSentRequests={setSentRequests}
                />
            </Stack>
        </>
    )
}

export default PeoplePanel