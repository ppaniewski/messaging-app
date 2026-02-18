import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, redirect, RouterProvider } from 'react-router-dom'
import { Provider } from "./components/ui/provider"

import './index.css'
import authLoader from "./loaders/authLoader"
import loginRedirect from './loaders/loginRedirect'
import dashboardLoader from './loaders/dashboardLoader'
import MainLayout from './components/MainLayout'
import Login from './components/Login'
import Register from './components/Register'
import ErrorPage from './components/ErrorPage'
import Dashboard from './components/Dashboard'
import PeoplePanel from './components/PeoplePanel'
import ChatPanel from './components/ChatPanel'
import FriendsPanel from './components/FriendsPanel'
import SocketProvider from './components/SocketProvider'

const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <SocketProvider>
        <MainLayout />
      </SocketProvider>
      ),
    loader: authLoader,
    errorElement: <ErrorPage />,
    HydrateFallback: () => null,
    children: [
      {
        index: true,
        element: <Dashboard />,
        loader: () => redirect("/dashboard/chats")
      },
      {
        path: "/dashboard",
        element: <Dashboard />,
        loader: dashboardLoader,
        children: [
          {
            index: true,
            element: <ChatPanel />,
            loader: () => redirect("/dashboard/chats")
          },
          {
            path: "/dashboard/chats",
            element: <ChatPanel />,
            loader: () => null
          },
          {
            path: "/dashboard/people",
            element: <PeoplePanel />,
            loader: () => null
          },
          {
            path: "/dashboard/friends",
            element: <FriendsPanel />,
            loader: () => null
          }
        ]
      }
    ]
  },
  {
    path: "/login",
    element: <MainLayout />,
    loader: loginRedirect,
    errorElement: <ErrorPage />,
    HydrateFallback: () => null,
    children: [
      {
        index: true,
        element: <Login />
      }
    ]
  },
  {
    path: "/register",
    element: <MainLayout />,
    loader: loginRedirect,
    errorElement: <ErrorPage />,
    HydrateFallback: () => null,
    children: [
      {
        index: true,
        element: <Register />
      }
    ]
  }
])

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Provider>
      <RouterProvider router={router} />
    </Provider>
  </StrictMode>,
)
