import { Avatar, Flex, Heading, Stack, Text } from "@chakra-ui/react"
import { useUserData } from "../contexts/UserDataContext"
import type { User } from "../api/users"
import type { MessageGroup } from "./ChatWindow"

type Props = {
    messageGroup: MessageGroup
    otherUser: User
}

const MessageStack = ({ messageGroup, otherUser }: Props) => {
    const userData = useUserData()

    const messageElements = [] 
    const sentByUser = messageGroup.messages[0].userId === userData.userId

    for (const m of messageGroup.messages) {
        if (!sentByUser) {
            messageElements.push(
                <Flex w="55%" key={m.id}>
                    <Text px={4} py={2} rounded="3xl" bg="midBg" color="fg">{m.text}</Text>
                </Flex>
            )
        }
        else {
            messageElements.push(
                <Flex w="55%" justifyContent="flex-end" key={m.id}>
                    <Text px={4} py={2} rounded="3xl" bg="teal.500" color="white">{m.text}</Text>
                </Flex>
            )
        }
    }
    
    const dateTag = <Heading size="xs" fontWeight="semibold" color="fg.subtle" alignSelf="center" py={2}>
                {formatDate(messageGroup.messages[0].createdAt)}
            </Heading>
    
    if (!sentByUser) {
        return (
            <Stack>
                {messageGroup.includeDateTag && dateTag}
                <Flex justifyContent="flex-start" alignItems="flex-end" gap={2}>
                    <Avatar.Root size="sm">
                        <Avatar.Fallback name={otherUser.username} />
                        <Avatar.Image />
                    </Avatar.Root>
                    <Stack gap={0.5} w="100%">
                        {messageElements}
                    </Stack>
                </Flex> 
            </Stack>
        )
    }

    const readTag = <Flex>
        <Avatar.Root size="2xs" mt={1} mr={2}>
            <Avatar.Fallback name={otherUser.username} />
            <Avatar.Image />
        </Avatar.Root>
    </Flex>

    return (
        <Stack>
            {messageGroup.includeDateTag && dateTag}
            <Flex gap={2}>
                <Stack alignItems="flex-end" gap={0.5} w="100%">
                    {messageElements}
                    {messageGroup.includeReadTag && readTag}
                </Stack>
            </Flex>
        </Stack>
    )
}

function formatDate(date: string) {
    const dateChanged = new Date(date)
    const timeParts = dateChanged.toLocaleTimeString().split(":")
    const localeTime = `${timeParts[0]}:${timeParts[1]}`

    return `${dateChanged.toLocaleDateString()}, ${localeTime}`
}

export default MessageStack