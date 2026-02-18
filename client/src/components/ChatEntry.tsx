import type { Conversation, Message } from "../api/conversations"
import { Avatar, Flex, Heading, Icon, Stack } from "@chakra-ui/react"
import { useUserData } from "../contexts/UserDataContext"
import { GoDotFill } from "react-icons/go"

type Props = {
    chat: Conversation
    selectedChatId: number | null
    setSelectedChatId: React.Dispatch<React.SetStateAction<number | null>>
}

const ChatEntry = ({ chat, selectedChatId, setSelectedChatId }: Props) => {
    const userData = useUserData()

    if (chat.isGroupChat) return <div>Oopsie!</div>
    
    const user = chat.users.find(u => u.id === userData.userId)
    if (!user) throw new Error("User not found")
    const otherUser = chat.users.find(u => u.id !== userData.userId)
    if (!otherUser) throw new Error("Other user not found")

    const newestMessage = getNewestMessage(chat)
    const formattedDate = formatTimePassed(newestMessage?.createdAt)
    const isUnread = user.isUnread
        
    return (
        <Flex 
            py={3} px={2} gap={4} rounded="lg"
            bg={selectedChatId === chat.id ? "slightBg" : undefined}
            justifyContent="flex-start" alignItems="center"
            _hover={{bg: "slightBg", cursor: "pointer"}} onClick={() => setSelectedChatId(chat.id)}
        >
            <Avatar.Root size="xl">
                <Avatar.Fallback name={otherUser.username} />
                <Avatar.Image />
            </Avatar.Root>
            <Stack gap={0} flex="1" minW={0}>
                <Heading size="xl">{otherUser.username}</Heading>
                <Flex alignItems="center">
                    <Heading
                        fontSize="sm" color={isUnread ? "fg" : "fg.muted"} 
                        fontWeight={isUnread ? "bold" : "normal"} 
                        textOverflow="ellipsis" whiteSpace="nowrap" overflow="hidden"
                    >
                        {newestMessage?.userId === userData.userId ? "You: " : ""}{newestMessage?.text || "No messages"}
                    </Heading>
                    <Heading 
                        size="sm" color="fg.muted" pl={1}
                        whiteSpace="nowrap" fontWeight="normal"
                    >
                       {newestMessage && `• ${formattedDate}`}
                    </Heading>
                </Flex>
            </Stack>
            {isUnread && <Icon size="lg" color="blue.600" >
                <GoDotFill />
            </Icon>}
        </Flex>
    )
}

function getNewestMessage(chat: Conversation): Message | undefined {
    if (chat.messages.length < 1) return undefined

    return chat.messages.find(m => !m.isDeleted)
}

function formatTimePassed(date?: string) {
    if (!date) return ""

    const changedDate = new Date(date)
    const currentDate = new Date()
    const timeDiffSeconds = (currentDate.getTime() - changedDate.getTime()) / 1000
    
    if (timeDiffSeconds < 60 * 2) {
        return "1 min" // Anything below 2 minutes is called 1 min
    }
    else if (timeDiffSeconds < 60 * 60) {
        const minutes = cutDecimal(timeDiffSeconds / 60)
        return `${minutes} mins`
    }
    else if (timeDiffSeconds < 60 * 60 * 24) {
        const hours = (timeDiffSeconds / (60 * 60))
        if (hours < 2) return "1 hour"

        return `${cutDecimal(hours)} hours`
    }
    else if (timeDiffSeconds < 60 * 60 * 24 * 7) {
        const days = (timeDiffSeconds / (60 * 60 * 24))
        if (days < 2) return "1 day"

        return `${cutDecimal(days)} days`
    }
    else if (timeDiffSeconds < 60 * 60 * 24 * 7 * 52) {
        const weeks = (timeDiffSeconds / (60 * 60 * 24 * 7))
        if (weeks < 2) return "1 week"

        return `${cutDecimal(weeks)} weeks`
    }
    else {
        const years = (timeDiffSeconds / (60 * 60 * 24 * 7 * 52))
        if (years < 2) return "1 year"

        return `${cutDecimal(years)} years`
    }
}

function cutDecimal(num: number) {
    const numString = num.toString()
    return numString.split(".")[0]
}

export default ChatEntry