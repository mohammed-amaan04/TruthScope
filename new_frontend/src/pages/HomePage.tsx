import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import NewsDashboard from '../components/NewsDashboard'
import FactCheckInput from '../components/FactCheckInput'

const HomePage = () => {
  const navigate = useNavigate()
  const [inputText, setInputText] = useState('')

  const handleFactCheck = (text: string) => {
    if (text.trim()) {
      // Navigate to results page with the text as state
      navigate('/results', { state: { text: text.trim() } })
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Newspaper Header */}
      <header className="bg-white border-b-4 border-newspaper-black">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="text-center">
            <h1 className="newspaper-headline text-4xl md:text-6xl text-newspaper-black mb-2">
              TRUTH SCOPE
            </h1>
            <div className="newspaper-divider w-full max-w-2xl mx-auto"></div>
            <p className="newspaper-caption text-lg mt-2">
              A PLATFORM TO ANALYSE AND CRITICISE NEWS FROM AROUND THE WORLD
            </p>
            <div className="flex justify-between items-center mt-4 text-sm text-newspaper-gray">
              <span>SUNDAY 15/06/2025</span>
              <span className="font-semibold">PRESENTED BY VERITAS.AI</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* News Dashboard Section */}
        <section className="mb-12">
          <div className="bg-white newspaper-border p-6 mb-8">
            <h2 className="newspaper-subheading text-2xl text-center mb-6 text-newspaper-black">
              TODAY'S TOP STORIES
            </h2>
            <NewsDashboard />
          </div>
        </section>

        {/* Fact Check Input Section */}
        <section className="mb-8">
          <div className="bg-white newspaper-border p-8">
            <div className="text-center mb-6">
              <h2 className="newspaper-subheading text-3xl text-newspaper-black mb-4">
                VERIFY YOUR NEWS
              </h2>
              <div className="newspaper-divider w-32 mx-auto"></div>
              <p className="newspaper-body text-newspaper-gray mt-4">
                Enter any news article, headline, or claim to verify its authenticity using our AI-powered fact-checking system.
              </p>
            </div>
            
            <FactCheckInput 
              value={inputText}
              onChange={setInputText}
              onSubmit={handleFactCheck}
            />
          </div>
        </section>

        {/* AI System Info */}
        <section className="bg-newspaper-black text-white p-8">
          <div className="text-center">
            <h3 className="newspaper-subheading text-2xl mb-4">
              AI-POWERED DISINFORMATION INTELLIGENCE SYSTEM
            </h3>
            <div className="grid md:grid-cols-3 gap-8 mt-8">
              <div className="flex items-start space-x-4">
                <div className="bg-white text-newspaper-black w-8 h-8 flex items-center justify-center font-bold">
                  1
                </div>
                <div>
                  <p className="newspaper-body">
                    An agent-based multimodal framework for real-time claim verification
                  </p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="bg-white text-newspaper-black w-8 h-8 flex items-center justify-center font-bold">
                  2
                </div>
                <div>
                  <p className="newspaper-body">
                    Accessible via a low-latency web dashboard + Telegram/X response bot
                  </p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="bg-white text-newspaper-black w-8 h-8 flex items-center justify-center font-bold">
                  3
                </div>
                <div>
                  <p className="newspaper-body">
                    Integrates NLP-based semantic inference, CV-driven media forensics, and LLM-based contextual reasoning
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t-2 border-newspaper-black mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="text-center">
            <p className="newspaper-caption">
              © 2025 Truth Scope - Powered by Veritas AI | All Rights Reserved
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default HomePage
