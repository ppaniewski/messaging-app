import { Outlet, useLocation } from 'react-router-dom'
import { Box } from '@chakra-ui/react'
import TopBar from './TopBar'

const MainLayout = () => {
    const location = useLocation()
    const path = location.pathname
    const topBarVariation = path === "/login" ? "login" : (path === "/register" ? "register" : "main")

    return (
        <>
            <TopBar variation={topBarVariation} />
            <Box pt={14} h="100vh" bg="bg.muted">
                <Outlet />
            </Box>
        </>
    )
}

export default MainLayout