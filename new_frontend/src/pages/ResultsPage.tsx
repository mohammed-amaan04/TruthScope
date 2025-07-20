import { useState, useEffect } from 'react'
import { useLocation, useNavigate, Link } from 'react-router-dom'
import { ArrowLeft, CheckCircle, XCircle, AlertCircle, Clock } from 'lucide-react'

interface VerificationResult {
  truth_score: number
  confidence: number
  verdict: string
  matching_articles: Array<{
    title: string
    source: string
    url: string
    similarity_score?: number
  }>
  contradicting_articles: Array<{
    title: string
    source: string
    url: string
    similarity_score?: number
  }>
  processing_time: number
}

const ResultsPage = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const [result, setResult] = useState<VerificationResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const text = location.state?.text

  useEffect(() => {
    if (!text) {
      navigate('/')
      return
    }

    const fetchResult = async () => {
      try {
        setLoading(true)
        const response = await fetch('http://localhost:8000/api/v1/verify/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            text: text,
            claim_type: 'sentence',
            language: 'en'
          })
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        setResult(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred')
      } finally {
        setLoading(false)
      }
    }

    fetchResult()
  }, [text, navigate])

  const getVerdictIcon = (verdict: string) => {
    switch (verdict) {
      case 'MOST_LIKELY_TRUE':
        return <CheckCircle className="w-8 h-8 text-green-600" />
      case 'LIKELY_FALSE':
        return <XCircle className="w-8 h-8 text-red-600" />
      case 'INCONCLUSIVE_MIXED':
        return <AlertCircle className="w-8 h-8 text-yellow-600" />
      default:
        return <AlertCircle className="w-8 h-8 text-gray-600" />
    }
  }

  const getVerdictText = (verdict: string) => {
    const verdictMap: { [key: string]: string } = {
      'MOST_LIKELY_TRUE': 'MOST LIKELY TRUE',
      'LIKELY_TRUE_NEEDS_SUPPORT': 'LIKELY TRUE (NEEDS MORE SUPPORT)',
      'INCONCLUSIVE_MIXED': 'INCONCLUSIVE / MIXED EVIDENCE',
      'LIKELY_FALSE': 'LIKELY FALSE',
      'INSUFFICIENT_DATA': 'INSUFFICIENT DATA'
    }
    return verdictMap[verdict] || verdict
  }

  const getScoreColor = (score: number) => {
    if (score >= 0.7) return 'text-green-600'
    if (score >= 0.4) return 'text-yellow-600'
    return 'text-red-600'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Clock className="w-12 h-12 animate-spin mx-auto mb-4 text-newspaper-black" />
          <h2 className="newspaper-subheading text-2xl text-newspaper-black">
            ANALYZING CLAIM...
          </h2>
          <p className="newspaper-body text-newspaper-gray mt-2">
            Our AI is verifying the information
          </p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center bg-white newspaper-border p-8 max-w-md">
          <XCircle className="w-12 h-12 mx-auto mb-4 text-red-600" />
          <h2 className="newspaper-subheading text-2xl text-newspaper-black mb-4">
            ANALYSIS FAILED
          </h2>
          <p className="newspaper-body text-newspaper-gray mb-6">
            {error}
          </p>
          <Link 
            to="/" 
            className="inline-block bg-newspaper-black text-white px-6 py-3 newspaper-body hover:bg-newspaper-gray transition-colors"
          >
            Return to Home
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b-4 border-newspaper-black">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link 
              to="/" 
              className="flex items-center space-x-2 text-newspaper-black hover:text-newspaper-gray transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              <span className="newspaper-body font-semibold">Back to Home</span>
            </Link>
            <div className="text-center">
              <h1 className="newspaper-headline text-2xl md:text-4xl text-newspaper-black">
                VERIFICATION REPORT
              </h1>
            </div>
            <div className="text-right">
              <p className="newspaper-caption text-sm">
                {new Date().toLocaleDateString('en-US', { 
                  weekday: 'long', 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })}
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Claim Section */}
        <section className="bg-white newspaper-border p-6 mb-8">
          <h2 className="newspaper-subheading text-xl mb-4 text-newspaper-black">
            CLAIM UNDER INVESTIGATION
          </h2>
          <div className="newspaper-divider mb-4"></div>
          <blockquote className="newspaper-body text-lg italic text-newspaper-gray border-l-4 border-newspaper-black pl-4">
            "{text}"
          </blockquote>
        </section>

        {result && (
          <>
            {/* Verdict Section */}
            <section className="bg-white newspaper-border p-8 mb-8">
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  {getVerdictIcon(result.verdict)}
                </div>
                <h2 className="newspaper-headline text-3xl text-newspaper-black mb-4">
                  {getVerdictText(result.verdict)}
                </h2>
                <div className="newspaper-divider w-32 mx-auto mb-6"></div>
                
                {/* Scores */}
                <div className="grid md:grid-cols-2 gap-8 max-w-2xl mx-auto">
                  <div className="text-center">
                    <h3 className="newspaper-subheading text-lg mb-2">TRUTH SCORE</h3>
                    <div className={`text-6xl font-bold ${getScoreColor(result.truth_score)}`}>
                      {Math.round(result.truth_score * 100)}%
                    </div>
                  </div>
                  <div className="text-center">
                    <h3 className="newspaper-subheading text-lg mb-2">CONFIDENCE</h3>
                    <div className={`text-6xl font-bold ${getScoreColor(result.confidence)}`}>
                      {Math.round(result.confidence * 100)}%
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* Sources Section */}
            <div className="grid md:grid-cols-2 gap-8">
              {/* Supporting Sources */}
              <section className="bg-white newspaper-border p-6">
                <h3 className="newspaper-subheading text-xl mb-4 text-green-700">
                  SUPPORTING SOURCES ({result.matching_articles?.length || 0})
                </h3>
                <div className="newspaper-divider mb-4"></div>
                {result.matching_articles && result.matching_articles.length > 0 ? (
                  <div className="space-y-4">
                    {result.matching_articles.slice(0, 5).map((article, index) => (
                      <div key={index} className="border-b border-newspaper-border pb-3 last:border-b-0">
                        <h4 className="newspaper-body font-semibold text-newspaper-black mb-1">
                          {article.title}
                        </h4>
                        <p className="newspaper-caption text-newspaper-gray">
                          Source: {article.source}
                        </p>
                        {article.url && (
                          <a 
                            href={article.url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:underline text-sm"
                          >
                            Read Article →
                          </a>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="newspaper-body text-newspaper-gray italic">
                    No supporting sources found.
                  </p>
                )}
              </section>

              {/* Contradicting Sources */}
              <section className="bg-white newspaper-border p-6">
                <h3 className="newspaper-subheading text-xl mb-4 text-red-700">
                  CONTRADICTING SOURCES ({result.contradicting_articles?.length || 0})
                </h3>
                <div className="newspaper-divider mb-4"></div>
                {result.contradicting_articles && result.contradicting_articles.length > 0 ? (
                  <div className="space-y-4">
                    {result.contradicting_articles.slice(0, 5).map((article, index) => (
                      <div key={index} className="border-b border-newspaper-border pb-3 last:border-b-0">
                        <h4 className="newspaper-body font-semibold text-newspaper-black mb-1">
                          {article.title}
                        </h4>
                        <p className="newspaper-caption text-newspaper-gray">
                          Source: {article.source}
                        </p>
                        {article.url && (
                          <a 
                            href={article.url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:underline text-sm"
                          >
                            Read Article →
                          </a>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="newspaper-body text-newspaper-gray italic">
                    No contradicting sources found.
                  </p>
                )}
              </section>
            </div>

            {/* Processing Info */}
            <section className="bg-newspaper-light-gray p-4 mt-8 text-center">
              <p className="newspaper-caption">
                Analysis completed in {result.processing_time.toFixed(2)} seconds | 
                Powered by Veritas AI | 
                Report generated on {new Date().toLocaleString()}
              </p>
            </section>
          </>
        )}
      </main>
    </div>
  )
}

export default ResultsPage
