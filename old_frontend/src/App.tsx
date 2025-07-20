import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Index from './pages/index'
import Profile from './pages/profile'
import ArticlePage from './pages/ArticlePage'
import ChatroomListPage from './pages/ChatroomListPage'
import ChatroomPage from './pages/ChatroomPage'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/article/:id" element={<ArticlePage />} />
        <Route path="/debates" element={<ChatroomListPage />} />
        <Route path="/debate/:id" element={<ChatroomPage />} />
      </Routes>
    </Router>
  )
}

export default App
