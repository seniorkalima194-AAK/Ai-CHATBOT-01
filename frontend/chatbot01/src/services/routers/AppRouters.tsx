import { Route, Routes } from 'react-router-dom'
import ChatPage from '../pages/main/ChatPage'
import ProfilePage from '../pages/main/ProfilePage'
import NotificationPage from '../pages/main/NotificationPage'
import SettingsPage from '../components/SettingPage'

const AppRouters = () => {
  return (
    <div>
        <Routes>
            <Route path='/' element={<ChatPage />}  />
            <Route path='/profile' element={<ProfilePage />}  />
            <Route path='/notification' element={<NotificationPage/>}  />
            <Route path="/settings" element={<SettingsPage />} />
        </Routes>
    </div>
  )
}

export default AppRouters;