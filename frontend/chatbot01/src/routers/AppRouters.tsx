import { Route, Routes } from 'react-router-dom'
import ChatPage from '../pages/main/ChatPage'
import ProfilePage from '../pages/main/ProfilePage'
import SettingsPage from '../components/SettingPage'
import NotificationPage from '../pages/main/NotificationPage'

const AppRouters = () => {
  return (
    <div>
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path='/notification' element={<NotificationPage/>}/>
      </Routes>
    </div>
  )
}

export default AppRouters;