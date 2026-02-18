import { useEffect, useState } from 'react'
import { Stack, Flex, IconButton } from '@chakra-ui/react'
import { Outlet, useNavigate, useLoaderData, useLocation } from 'react-router-dom'
import UserDataContext from '../contexts/UserDataContext'
import { TbMessageCircleFilled } from 'react-icons/tb'
import { IoPeople } from 'react-icons/io5'
import ChatWindow from './ChatWindow'
import { FaGlobe } from 'react-icons/fa'
import type { DashboardLoader } from '../loaders/dashboardLoader'
import { useFriendsData } from '../contexts/FriendsDataContext'
import { useChats } from '../contexts/ChatsContext'
import { getConversations } from '../api/conversations'

const Dashboard = () => {
  const navigate = useNavigate()
  const location = useLocation()

  const { userData, chatsInit, friendsInit, receivedRequestsInit, sentRequestsInit }: DashboardLoader = useLoaderData()
  const { friends, setFriends, receivedRequests, setReceivedRequests, 
    sentRequests, setSentRequests } = useFriendsData()
  const { chats, setChats, refreshChats, setRefreshChats } = useChats()

  useEffect(() => {
    setChats(chatsInit)
    setFriends(friendsInit)
    setSentRequests(sentRequestsInit)
    setReceivedRequests(receivedRequestsInit)
  }, [])

  useEffect(() => {
    if (!refreshChats) return

    async function getChats() {
      const res = await getConversations()
      if (!res.ok) throw new Error("Failed to load chats")

      const data = await res.json()
      setChats(data)
    }

    setRefreshChats(false)
    getChats()
  }, [refreshChats])

  const [selectedChatId, setSelectedChatId] = useState<number | null>(null)
  const [panelPick, setPanelPick] = useState<"chats" | "people" | "friends">("chats")

  useEffect(() => {
    if (location.pathname.endsWith("chats")) setPanelPick("chats")
    if (location.pathname.endsWith("people")) setPanelPick("people")
    if (location.pathname.endsWith("friends")) setPanelPick("friends")
  }, [])

  function chatButtonClicked() {
    setPanelPick("chats")
    navigate("/dashboard/chats")
  }

  function peopleButtonClicked() {
    setPanelPick("people")
    navigate("/dashboard/people")
  }

  function friendsButtonClicked() {
    setPanelPick("friends")
    navigate("/dashboard/friends")
  }

  return (
    <Flex h="100%" w="100%">
      <Stack alignItems="center" gap={2} px={2} py={6}>
          <IconButton 
            size="xl" variant="subtle" rounded="lg" 
            data-hover={panelPick === "chats" || undefined} onClick={chatButtonClicked}
          >
            <TbMessageCircleFilled />
          </IconButton>
          <IconButton 
            size="xl" variant="subtle" rounded="lg"
            data-hover={panelPick === "people" || undefined} onClick={peopleButtonClicked}
          >
            <FaGlobe />
          </IconButton>
          <IconButton 
            size="xl" variant="subtle" rounded="lg"
            data-hover={panelPick === "friends" || undefined} onClick={friendsButtonClicked}
          >
            <IoPeople />
          </IconButton>
      </Stack>

      <UserDataContext.Provider value={userData}>
        <Flex h="100%" minH={0} w="100%" gap={4} pb={4} pt={4}>
          <Outlet context={{ selectedChatId, setSelectedChatId, friends, setFriends, 
            sentRequests, setSentRequests, receivedRequests, setReceivedRequests }} />
          <ChatWindow chats={chats} setChats={setChats} selectedChatId={selectedChatId} />
        </Flex>
      </UserDataContext.Provider>
    </Flex>
  )
}

export default Dashboard