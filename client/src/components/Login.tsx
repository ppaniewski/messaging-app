import { Field, Heading, Center, Stack, Input, Button } from "@chakra-ui/react"
import { useNavigate, type NavigateFunction } from "react-router-dom"
import { toaster, Toaster } from "./ui/toaster"
import { PasswordInput } from "./ui/password-input"
import { useState } from "react"
import { loginUser } from "../helpers/authStore"

const Login = () => {
    const navigate = useNavigate()

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [usernameError, setUsernameError] = useState("")
    const [passwordError, setPasswordError] = useState("")

    async function loginButtonClicked() {
        if (!validUsername(username, setUsernameError)) {
            return
        }

        if (!validPassword(password, setPasswordError)) {
            return
        }

        await login(username as string, password as string, setUsernameError, setPasswordError, navigate)
    }

    return (
        <>
            <Center>
                <Stack gap={5} w={["250px", "350px"]}>
                    <Heading textAlign="center" pt={12}>Sign in</Heading>
                    <Field.Root invalid={usernameError !== "" ? true : false}>
                        <Field.Label>
                            Username
                        </Field.Label>
                        <Input 
                            fontSize="md" rounded="md" focusRingColor="blue.600" 
                            value={username} onChange={(e) => setUsername(e.target.value)} 
                        />
                        {usernameError !== "" ? <Field.ErrorText>{usernameError}</Field.ErrorText> : null}
                    </Field.Root>
                    <Field.Root invalid={passwordError !== "" ? true : false}>
                        <Field.Label>
                            Password
                        </Field.Label>
                        <PasswordInput 
                            fontSize="md" rounded="md" focusRingColor="blue.600" 
                            value={password} onChange={(e) => setPassword(e.target.value)} 
                        />
                        {passwordError !== "" ? <Field.ErrorText>{passwordError}</Field.ErrorText> : null}
                    </Field.Root>
                    <Button mt={2} variant="solid" colorPalette="green" rounded="md" onClick={() => loginButtonClicked()}>
                        Sign in
                    </Button>
                </Stack>
            </Center>
            <Toaster />
        </>
    )
}

const login = async (
    username: string,
    password: string,
    setUsernameError: React.Dispatch<React.SetStateAction<string>>,
    setPasswordError: React.Dispatch<React.SetStateAction<string>>,
    navigate: NavigateFunction
) => {
    const res = await loginUser(username, password)

    if (res.ok) {
        navigate("/")
    }
    else if (res.status === 404) {
        setUsernameError("User not found")
    }
    else if (res.status === 401) {
        setPasswordError("Incorrect password")
    }
    else {
        const error = await res.text()
        toaster.create({
            description: error,
            type: "error",
            duration: 7000
        })
    }
}

const validUsername = (
    username: string | undefined,
    setUsernameError: React.Dispatch<React.SetStateAction<string>>
): boolean => {
    if (!username) {
        setUsernameError("Username is required")
        return false
    }

    if (username.length < 3) {
        setUsernameError("Username is too short")
        return false
    }

    if (username.length > 50) {
        setUsernameError("Username is too long")
        return false
    }

    setUsernameError("")
    return true
}

const validPassword = (
    password: string | undefined, 
    setPasswordError: React.Dispatch<React.SetStateAction<string>>
): boolean => {
    if (!password) {
        setPasswordError("Password is required")
        return false
    }

    if (password.length > 64) {
        setPasswordError("Password is too long")
        return false
    }

    if (password.length < 6) {
        setPasswordError("Password is too short")
        return false
    }

    setPasswordError("")
    return true
}

export default Login