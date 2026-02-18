import { Stack, Heading } from "@chakra-ui/react"
import {  useOutletContext } from "react-router-dom"
import type { DashboardOutletContext } from "../contexts/DashboardOutletContext"
import ChatEntry from "./ChatEntry"
import { useChats } from "../contexts/ChatsContext"

const ChatPanel = () => {
    const { chats } = useChats()
    const { selectedChatId, setSelectedChatId }: DashboardOutletContext = useOutletContext()

    const chatList = chats.map((chat, index) => {
        return <ChatEntry chat={chat} key={index} selectedChatId={selectedChatId} setSelectedChatId={setSelectedChatId} />
    })

    return (
        <Stack 
            bg="bg.panel" minH={0} mt="0.5vh" 
            w={["40%", "40%", "40%", "35%", "30%"]} px={4} py={3} 
            rounded="xl" borderColor="border" borderWidth={1}
        >
            <Heading fontWeight="bold" size="2xl" flexShrink={0}>Chats</Heading>
            
            <Stack flex="1" minH={0} overflowY="auto" gap={0}>
                {chatList}
            </Stack>
        </Stack>
    )
}

export default ChatPanel