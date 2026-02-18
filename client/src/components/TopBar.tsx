import { Button, Flex, Heading } from '@chakra-ui/react'
import { useNavigate } from 'react-router-dom'
import { logoutUser } from '../helpers/authStore'
import { ColorModeButton } from './ui/color-mode'

type Variation = "main" | "login" | "register"

type TopBarProps = {
    variation: Variation
}

const TopBar = ({ variation }: TopBarProps) => {
    const navigate = useNavigate()

    const logoutPressed = async () => {
        const res = await logoutUser()
        if (res.ok) navigate("/login")
    }

    const buttonStyles = {
        variant: "outline",
        colorPalette: "green",
        rounded: "md",
        mr: 6
    } as const

    const loginButton = <Button {...buttonStyles} onClick={() => navigate("/register")}>Register</Button>
    const registerButton = <Button {...buttonStyles} onClick={() => navigate("/login")}>Login</Button>
    const mainButton = <Button {...buttonStyles} onClick={() => logoutPressed()}>Sign out</Button>

    return (
        <Flex 
            position="fixed" h={14} 
            borderColor="border" borderBottomWidth={1} 
            w="100%" zIndex="10" bg="bg.panel"
            alignItems="center" px={2} gap={0}
            justifyContent="space-between"
        >
            <Heading size="2xl" fontWeight="extrabold" pl={12}>Messager 2.0</Heading>
            <Flex gap={8} alignItems="center">
                <ColorModeButton />
                {variation === "main" ? mainButton : (variation === "login" ? loginButton : registerButton)}
            </Flex>
        </Flex>
    )
}

export default TopBar