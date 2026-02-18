import { Flex, Heading } from "@chakra-ui/react"

const ChatPlaceholder = () => {
    return (
        <Flex h="100%" pb={32} w="100%" justifyContent="center" alignItems="center">
            <Heading>
                This chat has no messages
            </Heading>
        </Flex>
    )
}

export default ChatPlaceholder