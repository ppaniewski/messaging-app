import { Avatar, Button, Flex, Heading, Stack } from "@chakra-ui/react"
import { type User } from "../api/users"
import { acceptFriendRequest, declineFriendRequest } from "../websocket/friendEmitters"
import { useChats } from "../contexts/ChatsContext"

type Props = {
    user: User
    setFriends: React.Dispatch<React.SetStateAction<User[]>>
    setReceivedRequests: React.Dispatch<React.SetStateAction<User[]>>
}

const FriendRequest = ({ user, setFriends, setReceivedRequests }: Props) => {
    const { setRefreshChats } = useChats()

    return (
        <Flex
            py={3} px={2} rounded="lg" justifyContent="space-between"
            _hover={{bg: "slightBg"}} alignItems="center" 
        >
            <Flex gap={2} alignItems="center" minW={0}>
                <Avatar.Root size={["md", "md", "md", "lg", "xl"]}>
                    <Avatar.Fallback name={user.username} />
                    <Avatar.Image />
                </Avatar.Root>
                <Stack gap={0} minW={0}>
                    <Heading 
                        size={["md", "lg", "xl", "2xl", "2xl"]}
                        textOverflow="ellipsis" whiteSpace="nowrap" overflow="hidden"
                    >{
                        user.username}
                    </Heading>
                </Stack>
            </Flex>
            <Flex 
                justifyContent="space-evenly" gap={2} alignItems="center" 
                direction={["column", undefined, undefined, "row", "row"]}
            >
                <Button 
                    colorPalette="green" size={["xs", "xs", "sm", "sm" ,"md"]} variant="surface"
                    onClick={() => acceptFriendRequest(user, setFriends, setReceivedRequests, setRefreshChats)}
                >Accept</Button>
                <Button 
                    colorPalette="red" size={["xs", "xs", "sm", "sm" ,"md"]} variant="surface" 
                    onClick={() => declineFriendRequest(user, setReceivedRequests)}
                >Decline</Button>
            </Flex>
        </Flex>
    )
}

export default FriendRequest