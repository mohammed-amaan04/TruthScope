import { useState } from 'react'
import { Search, FileText, Link as LinkIcon } from 'lucide-react'

interface FactCheckInputProps {
  value: string
  onChange: (value: string) => void
  onSubmit: (text: string) => void
}

const FactCheckInput = ({ value, onChange, onSubmit }: FactCheckInputProps) => {
  const [inputType, setInputType] = useState<'text' | 'url'>('text')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (value.trim()) {
      onSubmit(value.trim())
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Input Type Selector */}
      <div className="flex justify-center mb-6">
        <div className="flex division-bg rounded-lg p-1 shadow-sm">
          <button
            type="button"
            onClick={() => setInputType('text')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors ${
              inputType === 'text'
                ? 'paper-texture text-newspaper-black shadow-sm'
                : 'text-newspaper-gray hover:text-newspaper-black'
            }`}
          >
            <FileText className="w-4 h-4" />
            <span className="newspaper-body font-medium">Text/Article</span>
          </button>
          <button
            type="button"
            onClick={() => setInputType('url')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors ${
              inputType === 'url'
                ? 'paper-texture text-newspaper-black shadow-sm'
                : 'text-newspaper-gray hover:text-newspaper-black'
            }`}
          >
            <LinkIcon className="w-4 h-4" />
            <span className="newspaper-body font-medium">URL</span>
          </button>
        </div>
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <textarea
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={
              inputType === 'text'
                ? "Enter the news article, headline, or claim you want to fact-check...\n\nExample: \"Scientists have discovered a new planet in our solar system\""
                : "Enter the URL of the article you want to fact-check...\n\nExample: https://example.com/news-article"
            }
            className="w-full h-32 p-4 newspaper-body text-newspaper-black paper-texture newspaper-border resize-none focus:outline-none focus:ring-2 focus:ring-newspaper-black focus:border-transparent"
            required
          />
          <div className="absolute bottom-4 right-4">
            <Search className="w-5 h-5 text-newspaper-gray" />
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-between space-y-4 sm:space-y-0">
          <div className="text-sm text-newspaper-gray newspaper-body">
            <p>
              <strong>Tip:</strong> {inputType === 'text' 
                ? 'Paste the full article text or just the headline for best results.'
                : 'We\'ll extract and analyze the content from the provided URL.'
              }
            </p>
          </div>
          
          <button
            type="submit"
            disabled={!value.trim()}
            className="bg-newspaper-black text-white px-8 py-3 newspaper-body font-semibold hover:bg-newspaper-gray transition-colors disabled:bg-newspaper-border disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <Search className="w-4 h-4" />
            <span>VERIFY CLAIM</span>
          </button>
        </div>
      </form>

      {/* Example Claims */}
      <div className="mt-8 p-6 division-bg">
        <h4 className="newspaper-subheading text-lg mb-4 text-newspaper-black">
          EXAMPLE CLAIMS TO TRY:
        </h4>
        <div className="grid md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <button
              type="button"
              onClick={() => onChange("Climate change is causing more frequent extreme weather events worldwide.")}
              className="text-left w-full p-3 paper-texture newspaper-border hover:shadow-sm transition-shadow"
            >
              <p className="newspaper-body text-newspaper-black">
                "Climate change is causing more frequent extreme weather events worldwide."
              </p>
            </button>
            <button
              type="button"
              onClick={() => onChange("The COVID-19 vaccines have been proven 95% effective in preventing severe illness.")}
              className="text-left w-full p-3 paper-texture newspaper-border hover:shadow-sm transition-shadow"
            >
              <p className="newspaper-body text-newspaper-black">
                "The COVID-19 vaccines have been proven 95% effective in preventing severe illness."
              </p>
            </button>
          </div>
          <div className="space-y-2">
            <button
              type="button"
              onClick={() => onChange("Artificial intelligence will replace 50% of jobs by 2030.")}
              className="text-left w-full p-3 paper-texture newspaper-border hover:shadow-sm transition-shadow"
            >
              <p className="newspaper-body text-newspaper-black">
                "Artificial intelligence will replace 50% of jobs by 2030."
              </p>
            </button>
            <button
              type="button"
              onClick={() => onChange("Electric vehicles now account for over 10% of global car sales.")}
              className="text-left w-full p-3 paper-texture newspaper-border hover:shadow-sm transition-shadow"
            >
              <p className="newspaper-body text-newspaper-black">
                "Electric vehicles now account for over 10% of global car sales."
              </p>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default FactCheckInput
