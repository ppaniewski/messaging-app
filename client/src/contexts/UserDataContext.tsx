import { createContext, useContext } from "react"

const UserDataContext = createContext<UserData | undefined>(undefined)

export const useUserData = () => {
    const context = useContext(UserDataContext)
    if (context === undefined) {
        throw new Error("useUserData must be used within Dashboard")
    }

    return context
}

export interface UserData {
    userId: number
    username: string
}

export default UserDataContext