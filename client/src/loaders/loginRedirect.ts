import { redirect } from "react-router-dom"
import { verifyUser } from "../api/auth"

const loginRedirect = async () => {
    const res = await verifyUser()

    if (res.ok) {
        return redirect("/dashboard/chats")
    }
}

export default loginRedirect