import { Avatar, Button, Flex, Heading, Stack } from "@chakra-ui/react"
import { type User } from "../api/users"
import { sendFriendRequest } from "../websocket/friendEmitters"

type Props = {
    user: User
    setSentRequests: React.Dispatch<React.SetStateAction<User[]>>
}

const UserEntry = ({ user, setSentRequests }: Props) => {
    return <Flex 
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
                >
                    {user.username}
                </Heading>
            </Stack>
        </Flex>
        <Button 
            colorPalette="green" variant="surface" size={["xs", "xs", "sm", "sm" ,"md"]}
            onClick={() => sendFriendRequest(user, setSentRequests)}
        >
            Add Friend
        </Button>
    </Flex>
}

export default UserEntry