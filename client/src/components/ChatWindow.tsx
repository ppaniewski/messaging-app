import { Avatar, Box, Flex, Heading, Icon, Input, Stack } from "@chakra-ui/react"
import { getConversationMessages, type Conversation, type Message } from "../api/conversations"
import { useUserData, type UserData } from "../contexts/UserDataContext"
import { useEffect, useLayoutEffect, useRef, useState } from "react"
import { IoChatboxEllipses } from "react-icons/io5"
import MessageStack from "./MessageStack"
import ChatPlaceholder from "./ChatPlaceholder"
import { markConversationRead, sendMessage } from "../websocket/chatEmitters"
import type { ConversationUser } from "../api/users"

type Props = {
    chats: Conversation[]
    setChats: React.Dispatch<React.SetStateAction<Conversation[]>>
    selectedChatId: number | null
}

const ChatWindow = ({ chats, setChats, selectedChatId }: Props) => {
    const userData = useUserData()
    const [textInput, setTextInput] = useState("")

    const chat = chats.find(chat => selectedChatId === chat.id)
    const chatRef = useRef(chat)
    chatRef.current = chat
    
    useEffect(() => {
        ensureChatIsRead(chat, setChats, userData.userId)
    }, [selectedChatId, chat?.messages.length])

    const stackRef = useRef<HTMLDivElement>(null)
    const stackTopRef = useRef<HTMLDivElement>(null)
    const stackBottomRef = useRef<HTMLDivElement>(null)
    const prevScrollHeightRef = useRef(0)
    const prevScrollTopRef = useRef(0)
    const prependingRef = useRef(false)

    useEffect(() => {
        // Instant scroll down upon opening chat
        stackBottomRef.current?.scrollIntoView()
    }, [selectedChatId])

    useEffect(() => {
        const stackTop = stackTopRef.current
        const stack = stackRef.current
        if (!stackTop || !stack) return

        const observer = new IntersectionObserver(([entry]) => {
            if (entry.isIntersecting) {
                if (!chatRef.current) return

                prevScrollHeightRef.current = stack.scrollHeight
                prevScrollTopRef.current = stack.scrollTop
                prependingRef.current = true

                loadMoreMessages(chatRef.current, setChats, chatRef.current.messages.length)
            }
        }, { root: stack })

        observer.observe(stackTop)

        return () => observer.disconnect()
    }, [selectedChatId])

    useLayoutEffect(() => {
        const stack = stackRef.current
        
        if (stack && prependingRef.current) {
            const newScrollHeight = stack.scrollHeight
            const delta = newScrollHeight - prevScrollHeightRef.current
            stack.scrollTop = prevScrollTopRef.current + delta

            prependingRef.current = false
        }
    }, [chat?.messages.length])

    if (!chat) return <Stack flex="1" justifyContent="center" alignItems="center" pr={4}>
        <Icon size="2xl">
            <IoChatboxEllipses />
        </Icon>
        <Heading>No chat selected</Heading>
    </Stack>
    
    const otherUser = chat.users.find(u => u.id != userData.userId)
    if (!otherUser) throw new Error("Other user not found")

    const messageStacks = getMessageStacks(chat, userData, otherUser)

    return (
        <Stack bg="bg.panel" mt="0.5vh" flex="1" gap={0} mr={5} rounded="xl" borderColor="border" borderWidth={1}>
            <Flex 
                py={2} px={4} roundedTop="xl" alignItems="center" gap={2}
                flexShrink={0} borderColor="border" borderBottomWidth={1} 
            >
                <Avatar.Root size="lg">
                    <Avatar.Fallback name={otherUser.username} />
                    <Avatar.Image />
                </Avatar.Root>
                <Heading>{otherUser.username}</Heading>
            </Flex>

            <Stack overflowY="auto" px={4} pb={5} gap={2} flex="1" ref={stackRef}>
                <Box h={1} minH={1} flexShrink={0} ref={stackTopRef}></Box>
                {messageStacks.length > 0 ? messageStacks : <ChatPlaceholder />}
                <Box h={1} minH={1} flexShrink={0} ref={stackBottomRef}></Box>
            </Stack>

            <Flex flexShrink={0} justifySelf="flex-end" px={[16, 16, 16, 24, 32]} py={3}>
                <Input 
                    value={textInput} onChange={(e) => setTextInput(e.target.value)}
                    bg="slightBg" rounded="3xl" h={10} fontSize="md"
                    placeholder="Aa" focusRing="none" border="none"
                    onKeyDown={(e) => (e.key === "Enter" && !e.shiftKey) && 
                        sendInput(textInput, setTextInput, otherUser.id, setChats)
                    }
                />
            </Flex>
        </Stack>
    )
}

async function sendInput(
    textInput: string, 
    setTextInput: React.Dispatch<React.SetStateAction<string>>,
    otherUserId: number,
    setChats: React.Dispatch<React.SetStateAction<Conversation[]>>
) {
    if (textInput === "") return

    sendMessage(textInput, otherUserId, setChats)
    setTextInput("")
}

async function loadMoreMessages(
    chat: Conversation,
    setChats: React.Dispatch<React.SetStateAction<Conversation[]>>,
    offset: number
) {
    const res = await getConversationMessages(chat.id, offset)
    if (!res.ok) return

    const newMessages: Message[] = await res.json()
    setChats(prev => prev.map(c => 
        c.id !== chat.id ? c : {
            ...c,
            messages: [...c.messages, ...newMessages]
        }
    ))
}

function ensureChatIsRead(
    chat: Conversation | undefined,
    setChats: React.Dispatch<React.SetStateAction<Conversation[]>>,
    userId: number
) {
    if (!chat) return

    const chatUser = chat.users.find(u => u.id === userId)
    if (!chatUser || !chatUser.isUnread) return

    // Chat hasn't been read yet, mark it as read
    markConversationRead(chat.id, userId, setChats)
}

function getMessageStacks(
    chat: Conversation, 
    userData: UserData, 
    otherUser: ConversationUser
) {
    const groupedMessages = groupMessages(chat.messages, userData, otherUser)
    return groupedMessages.map(group => {
        return <MessageStack key={group.messages[0].id} messageGroup={group} otherUser={otherUser} />
    })
}

export interface MessageGroup {
    messages: Message[]
    includeDateTag: boolean
    includeReadTag: boolean
}

function groupMessages(
    messages: Message[], 
    userData: UserData,
    otherUser: ConversationUser
): MessageGroup[] {
    // Reverse the order for display from date descending to ascending
    const reversedMessages = [...messages].reverse()

    const MAX_DATE_DIFF_MS = 1000 * 60 * 60 // 1 hour
    const messageGroups: MessageGroup[] = []
    let lastUserId = null
    let lastDate = ""

    for (const m of reversedMessages) {
        const dateDiffPassed = dateDiffSurpassed(MAX_DATE_DIFF_MS, lastDate, m.createdAt)

        // Divide messages into groups if either the user changes or the
        // date difference between messages surpasses the max difference
        if (lastUserId !== m.userId || dateDiffPassed) {
            const newGroup: MessageGroup = {
                messages: [] as Message[],
                includeDateTag: false,
                includeReadTag: false
            }
            messageGroups.push(newGroup)
            
            lastUserId = m.userId
            lastDate = m.createdAt
        }

        const currentGroup = messageGroups[messageGroups.length - 1]
        currentGroup.messages.push(m)

        if (dateDiffPassed) {
            currentGroup.includeDateTag = true
        }
    }

    // If the other user has read the chat, include a read tag on the last group
    if (!otherUser.isUnread) {
        const lastUserGroup = [...messageGroups].reverse().find(group => 
        group.messages[0].userId === userData.userId)

        if (lastUserGroup) lastUserGroup.includeReadTag = true
    }
    
    return messageGroups
}

function dateDiffSurpassed(maxDiffMs: number, date1: string, date2: string): boolean {
    if (date1 === "" || date2 === "") return true

    const date1Ms = new Date(date1).getTime()
    const date2Ms = new Date(date2).getTime()
    const dateDiff = Math.abs(date2Ms - date1Ms)

    if (dateDiff > maxDiffMs) {
        return true
    }

    return false
}
 
export default ChatWindow