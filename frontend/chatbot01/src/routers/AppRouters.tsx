import { Route, Routes } from 'react-router-dom'
import ChatPage from '../pages/main/ChatPage'
import ProfilePage from '../pages/main/ProfilePage'
import SettingsPage from '../components/SettingPage'
import NotificationPage from '../pages/main/NotificationPage'
import LoginPage from '../pages/authentication/LoginPage'

const AppRouters = () => {
  return (
    <div>
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path='/notification' element={<NotificationPage/>}/>
        <Route path='/login' element={<LoginPage/>}/>
      </Routes>
    </div>
  )
}

export default AppRouters;