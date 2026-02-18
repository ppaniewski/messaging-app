import { io } from "socket.io-client"
import { getToken } from "../helpers/authStore"

const URL = undefined

const socket = io(URL, {
    autoConnect: false,
    auth: (cb) => cb({ token: getToken() })
})

export const ensureConnected = async () => {
    return new Promise<void>((resolve, reject) => {
        if (socket.connected) {
            console.log("WE WERE ALREADY CONNECTED")
            resolve()
            return
        }
        
        const onConnect = () => {
            cleanup()
            resolve()
        }

        const onError = () => {
            cleanup()
            reject()
        }

        const cleanup = () => {
            socket.off("connect", onConnect)
            socket.off("connect-error", onError)
        }

        socket.on("connect", onConnect)
        socket.on("connect-error", onError)

        socket.connect()
    })
} 

export const disconnectSocket = () => {
    socket.disconnect()
}

export default socket