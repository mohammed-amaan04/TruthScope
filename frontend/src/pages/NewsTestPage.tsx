import { useState, useEffect } from 'react'
import { newsService, NewsStatusResponse } from '../services/newsService'
import { CheckCircle, XCircle, AlertCircle, RefreshCw } from 'lucide-react'

const NewsTestPage = () => {
  const [status, setStatus] = useState<NewsStatusResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [testResults, setTestResults] = useState<{ [key: string]: boolean }>({})

  const runTests = async () => {
    setLoading(true)
    setError(null)
    const results: { [key: string]: boolean } = {}

    try {
      // Test 1: Get service status
      console.log('Testing service status...')
      const statusResult = await newsService.getNewsStatus()
      setStatus(statusResult)
      results['status'] = statusResult.status === 'success'

      // Test 2: Fetch all news
      console.log('Testing fetch all news...')
      const allNews = await newsService.getAllNews()
      results['allNews'] = allNews.status === 'success' && Object.keys(allNews.data).length > 0

      // Test 3: Fetch category news
      console.log('Testing fetch category news...')
      const politicsNews = await newsService.getCategoryNews('politics')
      results['categoryNews'] = politicsNews.status === 'success' && politicsNews.data.length > 0

      // Test 4: Test utility functions
      console.log('Testing utility functions...')
      const validUrl = newsService.isValidPreviewUrl('https://example.com')
      const invalidUrl = newsService.isValidPreviewUrl('invalid-url')
      const timestamp = newsService.formatTimestamp(new Date().toISOString())
      results['utilities'] = validUrl && !invalidUrl && timestamp.length > 0

      setTestResults(results)
    } catch (err) {
      console.error('Test error:', err)
      setError(err instanceof Error ? err.message : 'Test failed')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    runTests()
  }, [])

  const getStatusIcon = (success: boolean) => {
    return success ? (
      <CheckCircle className="w-5 h-5 text-green-500" />
    ) : (
      <XCircle className="w-5 h-5 text-red-500" />
    )
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <div className="paper-texture newspaper-border p-8 mb-8">
          <h1 className="newspaper-headline-bold text-4xl text-newspaper-black mb-4">
            NEWS SERVICE TEST PAGE
          </h1>
          <div className="newspaper-divider mb-6"></div>
          
          <div className="flex items-center justify-between mb-6">
            <p className="newspaper-body text-newspaper-gray">
              This page tests the integration between frontend and backend news services.
            </p>
            <button
              onClick={runTests}
              disabled={loading}
              className="flex items-center space-x-2 px-4 py-2 bg-newspaper-black text-white hover:bg-newspaper-gray transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              <span>Run Tests</span>
            </button>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 flex items-center space-x-2">
              <AlertCircle className="w-5 h-5 text-red-500" />
              <span className="text-red-700">{error}</span>
            </div>
          )}

          {/* Service Status */}
          {status && (
            <div className="mb-8">
              <h2 className="newspaper-subheading-bold text-2xl mb-4">Service Status</h2>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="division-bg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="newspaper-body font-semibold">Service Available</span>
                    {getStatusIcon(status.service_available)}
                  </div>
                  <p className="text-sm text-newspaper-gray">
                    {status.service_available ? 'News fetcher is running' : 'News fetcher unavailable'}
                  </p>
                </div>
                
                <div className="division-bg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="newspaper-body font-semibold">Cache Valid</span>
                    {getStatusIcon(status.cache_valid)}
                  </div>
                  <p className="text-sm text-newspaper-gray">
                    {status.cache_valid ? 'Cache is fresh' : 'Cache needs refresh'}
                  </p>
                </div>
                
                <div className="division-bg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="newspaper-body font-semibold">Last Updated</span>
                    <span className="text-sm text-newspaper-gray">
                      {status.last_updated ? new Date(status.last_updated).toLocaleString() : 'Never'}
                    </span>
                  </div>
                </div>
                
                <div className="division-bg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="newspaper-body font-semibold">Categories</span>
                    <span className="text-sm text-newspaper-gray">
                      {status.categories.length}
                    </span>
                  </div>
                  <p className="text-sm text-newspaper-gray">
                    {status.categories.join(', ')}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Test Results */}
          <div className="mb-8">
            <h2 className="newspaper-subheading-bold text-2xl mb-4">Test Results</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 division-bg">
                <span className="newspaper-body">Service Status Check</span>
                {loading ? (
                  <RefreshCw className="w-5 h-5 animate-spin text-newspaper-gray" />
                ) : (
                  getStatusIcon(testResults['status'])
                )}
              </div>
              
              <div className="flex items-center justify-between p-3 division-bg">
                <span className="newspaper-body">Fetch All News</span>
                {loading ? (
                  <RefreshCw className="w-5 h-5 animate-spin text-newspaper-gray" />
                ) : (
                  getStatusIcon(testResults['allNews'])
                )}
              </div>
              
              <div className="flex items-center justify-between p-3 division-bg">
                <span className="newspaper-body">Fetch Category News</span>
                {loading ? (
                  <RefreshCw className="w-5 h-5 animate-spin text-newspaper-gray" />
                ) : (
                  getStatusIcon(testResults['categoryNews'])
                )}
              </div>
              
              <div className="flex items-center justify-between p-3 division-bg">
                <span className="newspaper-body">Utility Functions</span>
                {loading ? (
                  <RefreshCw className="w-5 h-5 animate-spin text-newspaper-gray" />
                ) : (
                  getStatusIcon(testResults['utilities'])
                )}
              </div>
            </div>
          </div>

          {/* Instructions */}
          <div className="division-bg p-6">
            <h3 className="newspaper-subheading text-lg mb-3">Next Steps</h3>
            <div className="space-y-2 text-sm text-newspaper-gray">
              <p>1. Make sure your backend is running: <code className="bg-newspaper-light-gray px-2 py-1">uvicorn app.main:app --reload</code></p>
              <p>2. Check that the news endpoints are accessible at: <code className="bg-newspaper-light-gray px-2 py-1">http://localhost:8000/api/v1/news/all</code></p>
              <p>3. If tests fail, check the browser console for detailed error messages</p>
              <p>4. For real news data, add your NEWSAPI_KEY to the .env file</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default NewsTestPage
