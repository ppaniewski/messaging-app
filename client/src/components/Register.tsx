import { Field, Heading, Center, Stack, Input, Button } from "@chakra-ui/react"
import { useNavigate, type NavigateFunction } from "react-router-dom"
import { toaster, Toaster } from "./ui/toaster"
import { PasswordInput } from "./ui/password-input"
import { useState } from "react"
import { registerUser } from "../api/auth"

const Register = () => {
    const navigate = useNavigate()

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [usernameError, setUsernameError] = useState("")
    const [passwordError, setPasswordError] = useState("")

    const usernameHelperText = "At least 5 characters long"
    const passwordHelperText = "At least 6 characters long, including at least one letter, one digit, and one special symbol (e.g %,*,$)"

    async function registerButtonClicked() {
        if (!validUsername(username, setUsernameError)) {
            return
        }

        if (!validPassword(password, setPasswordError)) {
            return
        }

        await register(username as string, password as string, navigate)
    }

    return (
        <>
            <Center>
                <Stack gap={5} w={["250px", "350px"]}>
                    <Heading textAlign="center" pt={12}>Sign up</Heading>
                    <Field.Root invalid={usernameError !== "" ? true : false}>
                        <Field.Label>
                            Username
                        </Field.Label>
                        <Input 
                            fontSize="md" rounded="md" focusRingColor="blue.600" 
                            value={username} onChange={(e) => setUsername(e.target.value)} 
                        />
                        {usernameError !== "" ? <Field.ErrorText>{usernameError}</Field.ErrorText> : 
                            <Field.HelperText>{usernameHelperText}</Field.HelperText> }
                    </Field.Root>
                    <Field.Root invalid={passwordError !== "" ? true : false}>
                        <Field.Label>
                            Password
                        </Field.Label>
                        <PasswordInput 
                            fontSize="md" rounded="md" focusRingColor="blue.600" 
                            value={password} onChange={(e) => setPassword(e.target.value)} 
                        />
                        {passwordError !== "" ? <Field.ErrorText>{passwordError}</Field.ErrorText> :
                            <Field.HelperText>{passwordHelperText}</Field.HelperText>}
                    </Field.Root>
                    <Button mt={2} variant="solid" colorPalette="green" rounded="md" onClick={() => registerButtonClicked()}>
                        Create account
                    </Button>
                </Stack>
            </Center>
            <Toaster />
        </>
    )
}

const register = async (
    username: string,
    password: string,
    navigate: NavigateFunction
) => {
    const res = await registerUser(username, password)
    const body = await res.json()

    if (!res.ok) {
        toaster.create({
            description: body.detail,
            type: "error",
            duration: 7000
        })
    }
    else {
        navigate("/login")
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

    if (!/\d/.test(password)) {
        setPasswordError("Must contain at least one digit")
        return false
    }

    if (!/[A-Za-z]/.test(password)) {
        setPasswordError("Must contain at least one character")
        return false
    }

    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        setPasswordError("Must contain at least one special symbol")
        return false
    }

    setPasswordError("")
    return true
}

export default Register