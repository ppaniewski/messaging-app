import { InputGroup, Input } from "@chakra-ui/react"
import { useEffect, useState, useRef } from "react"
import { FaSearch } from "react-icons/fa"
import { getUsers, type User } from "../api/users"
import { useUserData } from "../contexts/UserDataContext"

type Props = { 
    setUsers: React.Dispatch<React.SetStateAction<User[]>>
    loadMoreUsersRef: React.RefObject<(() => Promise<void>) | null>
}

const UserSearch = ({ setUsers, loadMoreUsersRef }: Props) => {
    const userLoadLimit = 10

    const [value, setValue] = useState("")
    const valueRef = useRef(value)
    const userOffsetRef = useRef(0)

    const userData = useUserData()

    useEffect(() => {
        valueRef.current = value
    }, [value])

    useEffect(() => {
        loadMoreUsersRef.current = loadMoreUsers
    }, [])

    useEffect(() => {
        searchUsers()
    }, [value])

    async function searchUsers() {
        if (valueRef.current == "") {
            setUsers([])
            return
        }

        const res = await getUsers(valueRef.current, userLoadLimit, 0)
        if (!res.ok) return

        let newUsers: User[] = await res.json()
        userOffsetRef.current = newUsers.length // Set new offset before filtering out users

        newUsers = newUsers.filter(u => u.id !== userData.userId)
        setUsers(newUsers)
    }

    async function loadMoreUsers() {
        if (valueRef.current == "") return

        const res = await getUsers(valueRef.current, userLoadLimit, userOffsetRef.current)
        if (!res.ok) return

        let newUsers: User[] = await res.json()
        userOffsetRef.current += newUsers.length // Update offset before filtering out users

        newUsers = newUsers.filter(u => u.id !== userData.userId)
        setUsers(prevUsers => prevUsers.concat(newUsers))
    }

    return (
        <InputGroup startElement={<FaSearch />}>
            <Input 
                variant="subtle" fontSize="md" placeholder="Search users" 
                rounded="3xl" focusRing="none" borderWidth="0px" 
                value={value} onChange={(e) => setValue(e.target.value)}
            />
        </InputGroup>
    )
}

export default UserSearch