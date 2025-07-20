import { useState, useEffect } from 'react'
import { ChevronLeft, ChevronRight } from 'lucide-react'

interface NewsItem {
  id: string
  title: string
  summary: string
  category: string
  image?: string
  source: string
  publishedAt: string
}

const mockNews: { [key: string]: NewsItem[] } = {
  politics: [
    {
      id: '1',
      title: 'Global Climate Summit Reaches Historic Agreement',
      summary: 'World leaders unite on unprecedented climate action plan with binding commitments for carbon neutrality by 2050.',
      category: 'politics',
      source: 'Reuters',
      publishedAt: '2025-01-18T10:00:00Z'
    },
    {
      id: '2',
      title: 'Trade Relations Show Signs of Improvement',
      summary: 'Diplomatic talks yield positive results in ongoing trade negotiations.',
      category: 'politics',
      source: 'Associated Press',
      publishedAt: '2025-01-18T09:30:00Z'
    },
    {
      id: '3',
      title: 'Election Security Measures Enhanced',
      summary: 'New cybersecurity protocols implemented nationwide.',
      category: 'politics',
      source: 'BBC News',
      publishedAt: '2025-01-18T08:45:00Z'
    },
    {
      id: '4',
      title: 'Infrastructure Bill Passes Final Vote',
      summary: 'Landmark legislation promises major improvements to national infrastructure.',
      category: 'politics',
      source: 'CNN',
      publishedAt: '2025-01-18T08:00:00Z'
    },
    {
      id: '5',
      title: 'International Peace Talks Resume',
      summary: 'Diplomatic efforts continue with renewed optimism for resolution.',
      category: 'politics',
      source: 'The Guardian',
      publishedAt: '2025-01-18T07:30:00Z'
    }
  ],
  economics: [
    {
      id: '6',
      title: 'Stock Markets Reach Record Highs',
      summary: 'Technology sector leads unprecedented growth as markets surge to new peaks amid investor optimism.',
      category: 'economics',
      source: 'Financial Times',
      publishedAt: '2025-01-18T10:15:00Z'
    },
    {
      id: '7',
      title: 'Cryptocurrency Regulation Framework Announced',
      summary: 'New guidelines provide clarity for digital asset markets.',
      category: 'economics',
      source: 'Wall Street Journal',
      publishedAt: '2025-01-18T09:45:00Z'
    },
    {
      id: '8',
      title: 'Unemployment Rates Hit Decade Low',
      summary: 'Job market shows remarkable recovery with strong hiring trends.',
      category: 'economics',
      source: 'Bloomberg',
      publishedAt: '2025-01-18T09:00:00Z'
    },
    {
      id: '9',
      title: 'Green Energy Investment Soars',
      summary: 'Renewable energy sector attracts record funding levels.',
      category: 'economics',
      source: 'Reuters',
      publishedAt: '2025-01-18T08:30:00Z'
    },
    {
      id: '10',
      title: 'Housing Market Shows Stability',
      summary: 'Real estate prices stabilize after months of volatility.',
      category: 'economics',
      source: 'CNBC',
      publishedAt: '2025-01-18T08:00:00Z'
    }
  ],
  celebrity: [
    {
      id: '11',
      title: 'Hollywood Stars Launch Charity Initiative',
      summary: 'A-list celebrities unite for global education fund, raising millions for underprivileged children worldwide.',
      category: 'celebrity',
      source: 'Entertainment Weekly',
      publishedAt: '2025-01-18T11:00:00Z'
    },
    {
      id: '12',
      title: 'Music Industry Embraces AI Technology',
      summary: 'Artists explore new creative possibilities with artificial intelligence.',
      category: 'celebrity',
      source: 'Rolling Stone',
      publishedAt: '2025-01-18T10:30:00Z'
    },
    {
      id: '13',
      title: 'Film Festival Announces Lineup',
      summary: 'International cinema showcase features diverse storytelling.',
      category: 'celebrity',
      source: 'Variety',
      publishedAt: '2025-01-18T10:00:00Z'
    },
    {
      id: '14',
      title: 'Fashion Week Highlights Sustainability',
      summary: 'Designers showcase eco-friendly collections and practices.',
      category: 'celebrity',
      source: 'Vogue',
      publishedAt: '2025-01-18T09:30:00Z'
    },
    {
      id: '15',
      title: 'Celebrity Chef Opens New Restaurant',
      summary: 'Michelin-starred venue focuses on local and organic ingredients.',
      category: 'celebrity',
      source: 'Food & Wine',
      publishedAt: '2025-01-18T09:00:00Z'
    }
  ],
  sports: [
    {
      id: '16',
      title: 'Championship Finals Set Record Viewership',
      summary: 'Historic match draws global audience as underdog team advances to finals in stunning upset victory.',
      category: 'sports',
      source: 'ESPN',
      publishedAt: '2025-01-18T11:30:00Z'
    },
    {
      id: '17',
      title: 'Olympic Preparations Underway',
      summary: 'Athletes gear up for upcoming games with intensive training.',
      category: 'sports',
      source: 'Sports Illustrated',
      publishedAt: '2025-01-18T11:00:00Z'
    },
    {
      id: '18',
      title: 'New Stadium Opens to Fanfare',
      summary: 'State-of-the-art facility features cutting-edge technology.',
      category: 'sports',
      source: 'The Athletic',
      publishedAt: '2025-01-18T10:30:00Z'
    },
    {
      id: '19',
      title: 'Rookie Breaks Long-Standing Record',
      summary: 'Young athlete achieves milestone in debut professional season.',
      category: 'sports',
      source: 'Fox Sports',
      publishedAt: '2025-01-18T10:00:00Z'
    },
    {
      id: '20',
      title: 'Team Announces New Coaching Staff',
      summary: 'Management changes signal new direction for franchise.',
      category: 'sports',
      source: 'CBS Sports',
      publishedAt: '2025-01-18T09:30:00Z'
    }
  ]
}

const NewsDashboard = () => {
  const [currentSlide, setCurrentSlide] = useState(0)
  const categories = ['politics', 'economics', 'celebrity', 'sports']
  const categoryTitles = {
    politics: 'POLITICS',
    economics: 'ECONOMICS', 
    celebrity: 'CELEBRITY',
    sports: 'SPORTS'
  }

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % categories.length)
  }

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + categories.length) % categories.length)
  }

  useEffect(() => {
    const interval = setInterval(nextSlide, 8000) // Auto-advance every 8 seconds
    return () => clearInterval(interval)
  }, [])

  const currentCategory = categories[currentSlide]
  const currentNews = mockNews[currentCategory]

  return (
    <div className="relative">
      {/* Category Navigation */}
      <div className="flex justify-center mb-6">
        <div className="flex space-x-1 bg-newspaper-light-gray p-1 rounded">
          {categories.map((category, index) => (
            <button
              key={category}
              onClick={() => setCurrentSlide(index)}
              className={`px-4 py-2 newspaper-body font-semibold transition-colors ${
                index === currentSlide
                  ? 'bg-newspaper-black text-white'
                  : 'text-newspaper-gray hover:text-newspaper-black'
              }`}
            >
              {categoryTitles[category as keyof typeof categoryTitles]}
            </button>
          ))}
        </div>
      </div>

      {/* Slideshow Container */}
      <div className="relative overflow-hidden">
        <div 
          className="flex transition-transform duration-500 ease-in-out"
          style={{ transform: `translateX(-${currentSlide * 100}%)` }}
        >
          {categories.map((category) => (
            <div key={category} className="w-full flex-shrink-0">
              <div className="text-center mb-4">
                <h3 className="newspaper-subheading text-2xl text-newspaper-black">
                  {categoryTitles[category as keyof typeof categoryTitles]} NEWS
                </h3>
                <div className="newspaper-divider w-24 mx-auto mt-2"></div>
              </div>
              
              {/* News Layout: 1 big + 2 + 2 */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Big news item (left) */}
                <div className="md:col-span-2">
                  <div className="newspaper-border p-6 h-full bg-white hover:shadow-lg transition-shadow">
                    <div className="mb-4">
                      <span className="text-xs font-semibold text-newspaper-accent uppercase tracking-wide">
                        {categoryTitles[category as keyof typeof categoryTitles]} • {mockNews[category][0].source}
                      </span>
                    </div>
                    <h4 className="newspaper-subheading text-xl mb-3 text-newspaper-black leading-tight">
                      {mockNews[category][0].title}
                    </h4>
                    <p className="newspaper-body text-newspaper-gray mb-4">
                      {mockNews[category][0].summary}
                    </p>
                    <div className="text-xs text-newspaper-gray">
                      {new Date(mockNews[category][0].publishedAt).toLocaleString()}
                    </div>
                  </div>
                </div>

                {/* Smaller news items (right) */}
                <div className="space-y-6">
                  {mockNews[category].slice(1, 5).map((item, index) => (
                    <div key={item.id} className="newspaper-border p-4 bg-white hover:shadow-lg transition-shadow">
                      <div className="mb-2">
                        <span className="text-xs font-semibold text-newspaper-accent uppercase tracking-wide">
                          {item.source}
                        </span>
                      </div>
                      <h5 className="newspaper-body font-semibold text-newspaper-black mb-2 leading-tight">
                        {item.title}
                      </h5>
                      <p className="text-sm text-newspaper-gray line-clamp-2">
                        {item.summary}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Navigation Arrows */}
        <button
          onClick={prevSlide}
          className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white newspaper-border p-2 hover:bg-newspaper-light-gray transition-colors"
        >
          <ChevronLeft className="w-6 h-6 text-newspaper-black" />
        </button>
        <button
          onClick={nextSlide}
          className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white newspaper-border p-2 hover:bg-newspaper-light-gray transition-colors"
        >
          <ChevronRight className="w-6 h-6 text-newspaper-black" />
        </button>
      </div>

      {/* Slide Indicators */}
      <div className="flex justify-center mt-6 space-x-2">
        {categories.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentSlide(index)}
            className={`w-3 h-3 rounded-full transition-colors ${
              index === currentSlide ? 'bg-newspaper-black' : 'bg-newspaper-border'
            }`}
          />
        ))}
      </div>
    </div>
  )
}

export default NewsDashboard
