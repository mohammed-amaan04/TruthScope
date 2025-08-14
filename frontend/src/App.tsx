import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Suspense, lazy } from 'react'

const HomePage = lazy(() => import('./pages/HomePage'))
const ResultsPage = lazy(() => import('./pages/ResultsPage'))
const NewsTestPage = lazy(() => import('./pages/NewsTestPage'))
const ImageTestPage = lazy(() => import('./pages/ImageTestPage'))

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Suspense fallback={<div className="p-8">Loading...</div>}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/results" element={<ResultsPage />} />
            <Route path="/test-news" element={<NewsTestPage />} />
            <Route path="/test-images" element={<ImageTestPage />} />
          </Routes>
        </Suspense>
      </div>
    </Router>
  )
}

export default App
