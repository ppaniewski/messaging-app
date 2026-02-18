import { Avatar, Button, Flex, Heading, Stack } from "@chakra-ui/react"
import { type User } from "../api/users"

type Props = {
    user: User
}

const RequestSent = ({ user }: Props) => {
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
            size={["xs", "xs", "sm", "sm" ,"md"]}
            disabled colorPalette="green" variant="surface"
        >
            Request sent
        </Button>
    </Flex>
}

export default RequestSent