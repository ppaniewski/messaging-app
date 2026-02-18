import { Heading, Stack } from "@chakra-ui/react"
import { isRouteErrorResponse, useNavigate, useRouteError } from "react-router-dom"

const ErrorPage = () => {
    const error = useRouteError()
    const navigate = useNavigate()

    if (isRouteErrorResponse(error)) {
        return (
            <Stack p={4}>
                <Heading>
                    {`Error ${error.status}: `}
                    <br></br>
                    {error.data}
                </Heading>
                {error.status === 404 && 
                    <Heading 
                        size="lg" color="teal.400" _hover={{ cursor: "pointer" }}
                        onClick={() => navigate("/dashboard")}
                    >
                        Return to Dashboard
                    </Heading>
                }
            </Stack>
        )
    }
    
    return (
        <Heading p={4}>
            {`${error}`}
        </Heading>
    )
}

export default ErrorPage