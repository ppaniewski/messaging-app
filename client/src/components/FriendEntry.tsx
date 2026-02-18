import { Avatar, Button, Flex, Heading, Stack } from "@chakra-ui/react"
import { type User } from "../api/users"
import { removeFriend } from "../websocket/friendEmitters"
import { useChats } from "../contexts/ChatsContext"

type Props = {
    friend: User
    setFriends: React.Dispatch<React.SetStateAction<User[]>>
}

const FriendEntry = ({ friend, setFriends }: Props) => {
    const { setRefreshChats } = useChats()

    return (
        <Flex 
            py={3} px={2} rounded="lg" justifyContent="space-between"
            _hover={{bg: "slightBg"}} alignItems="center" 
        >
            <Flex gap={2} alignItems="center" minW={0}>
                <Avatar.Root size={["md", "md", "md", "lg", "xl"]}>
                    <Avatar.Fallback name={friend.username} />
                    <Avatar.Image />
                </Avatar.Root>
                <Stack gap={0} minW={0}>
                    <Heading 
                        size={["md", "lg", "xl", "2xl", "2xl"]}
                        textOverflow="ellipsis" whiteSpace="nowrap" overflow="hidden"
                    >
                        {friend.username}
                    </Heading>
                </Stack>
            </Flex>
            <Button 
                colorPalette="red" variant="surface" size={["xs", "xs", "sm", "sm" ,"md"]}
                onClick={() => removeFriend(friend, setFriends, setRefreshChats)}
            >
                Remove Friend
            </Button>
        </Flex>
    )
}

export default FriendEntry