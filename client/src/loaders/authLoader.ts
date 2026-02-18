import { redirect } from "react-router-dom"
import { verifyUser } from "../api/auth"
import { disconnectSocket } from "../websocket/socket"

const authLoader = async () => {
    const res = await verifyUser()

    if (!res.ok) {
        disconnectSocket()
        throw redirect("/login")
    }
}

export default authLoader