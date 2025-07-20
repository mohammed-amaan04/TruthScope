/**
 * News Service for Veritas Frontend
 * Handles API calls to the news endpoints
 */

const API_BASE_URL = 'http://localhost:8000/api/v1'

export interface NewsArticle {
  id: string
  title: string
  summary: string
  category: string
  source: string
  publishedAt: string
  url?: string
}

export interface NewsResponse {
  status: string
  data: { [category: string]: NewsArticle[] }
  last_updated?: string
  categories: string[]
  total_articles: number
}

export interface CategoryNewsResponse {
  status: string
  category: string
  data: NewsArticle[]
  count: number
}

export interface NewsStatusResponse {
  status: string
  service_available: boolean
  cache_valid: boolean
  last_updated?: string
  cache_duration_minutes: number
  categories: string[]
}

class NewsService {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  /**
   * Fetch all news categories
   */
  async getAllNews(refresh: boolean = false): Promise<NewsResponse> {
    const url = new URL(`${this.baseUrl}/news/all`)
    if (refresh) {
      url.searchParams.append('refresh', 'true')
    }

    const response = await fetch(url.toString())
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  /**
   * Fetch news for a specific category
   */
  async getCategoryNews(category: string): Promise<CategoryNewsResponse> {
    const response = await fetch(`${this.baseUrl}/news/${category}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  /**
   * Refresh news cache
   */
  async refreshNewsCache(): Promise<{ status: string; message: string; timestamp: string }> {
    const response = await fetch(`${this.baseUrl}/news/refresh`, {
      method: 'POST'
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  /**
   * Get news service status
   */
  async getNewsStatus(): Promise<NewsStatusResponse> {
    const response = await fetch(`${this.baseUrl}/news/status`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  /**
   * Check if a URL is valid for preview
   */
  isValidPreviewUrl(url?: string): boolean {
    if (!url) return false
    
    // Don't preview example URLs or invalid URLs
    if (url.includes('example.com') || url === '#') return false
    
    try {
      new URL(url)
      return true
    } catch {
      return false
    }
  }

  /**
   * Format timestamp for display
   */
  formatTimestamp(timestamp: string): string {
    try {
      const date = new Date(timestamp)
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return timestamp
    }
  }

  /**
   * Get fallback news data when API is unavailable
   */
  getFallbackNews(): { [category: string]: NewsArticle[] } {
    const now = new Date()
    
    return {
      politics: [
        {
          id: 'politics_1',
          title: 'Global Climate Summit Reaches Historic Agreement',
          summary: 'World leaders unite on unprecedented climate action plan with binding commitments for carbon neutrality by 2050...',
          category: 'politics',
          source: 'Reuters',
          publishedAt: now.toISOString(),
          url: 'https://reuters.com'
        },
        {
          id: 'politics_2',
          title: 'Trade Relations Show Signs of Improvement',
          summary: 'Diplomatic talks yield positive results in ongoing trade negotiations between major economic powers...',
          category: 'politics',
          source: 'Associated Press',
          publishedAt: new Date(now.getTime() - 2 * 60 * 60 * 1000).toISOString(),
          url: 'https://apnews.com'
        },
        {
          id: 'politics_3',
          title: 'Election Security Measures Enhanced',
          summary: 'New cybersecurity protocols implemented nationwide to protect electoral integrity...',
          category: 'politics',
          source: 'BBC News',
          publishedAt: new Date(now.getTime() - 4 * 60 * 60 * 1000).toISOString(),
          url: 'https://bbc.com'
        },
        {
          id: 'politics_4',
          title: 'Infrastructure Bill Passes Final Vote',
          summary: 'Landmark legislation promises major improvements to national infrastructure and job creation...',
          category: 'politics',
          source: 'CNN',
          publishedAt: new Date(now.getTime() - 6 * 60 * 60 * 1000).toISOString(),
          url: 'https://cnn.com'
        },
        {
          id: 'politics_5',
          title: 'International Peace Talks Resume',
          summary: 'Diplomatic efforts continue with renewed optimism for resolution of long-standing conflicts...',
          category: 'politics',
          source: 'The Guardian',
          publishedAt: new Date(now.getTime() - 8 * 60 * 60 * 1000).toISOString(),
          url: 'https://theguardian.com'
        }
      ],
      economics: [
        {
          id: 'economics_1',
          title: 'Stock Markets Reach Record Highs',
          summary: 'Technology sector leads unprecedented growth as markets surge to new peaks amid investor optimism...',
          category: 'economics',
          source: 'Financial Times',
          publishedAt: now.toISOString(),
          url: 'https://ft.com'
        },
        {
          id: 'economics_2',
          title: 'Cryptocurrency Regulation Framework Announced',
          summary: 'New guidelines provide clarity for digital asset markets and institutional adoption...',
          category: 'economics',
          source: 'Wall Street Journal',
          publishedAt: new Date(now.getTime() - 1 * 60 * 60 * 1000).toISOString(),
          url: 'https://wsj.com'
        },
        {
          id: 'economics_3',
          title: 'Unemployment Rates Hit Decade Low',
          summary: 'Job market shows remarkable recovery with strong hiring trends across multiple sectors...',
          category: 'economics',
          source: 'Bloomberg',
          publishedAt: new Date(now.getTime() - 3 * 60 * 60 * 1000).toISOString(),
          url: 'https://bloomberg.com'
        },
        {
          id: 'economics_4',
          title: 'Green Energy Investment Soars',
          summary: 'Renewable energy sector attracts record funding levels as sustainability becomes priority...',
          category: 'economics',
          source: 'Reuters',
          publishedAt: new Date(now.getTime() - 5 * 60 * 60 * 1000).toISOString(),
          url: 'https://reuters.com'
        },
        {
          id: 'economics_5',
          title: 'Housing Market Shows Stability',
          summary: 'Real estate prices stabilize after months of volatility, signaling market maturation...',
          category: 'economics',
          source: 'CNBC',
          publishedAt: new Date(now.getTime() - 7 * 60 * 60 * 1000).toISOString(),
          url: 'https://cnbc.com'
        }
      ],
      celebrity: [
        {
          id: 'celebrity_1',
          title: 'Hollywood Stars Launch Charity Initiative',
          summary: 'A-list celebrities unite for global education fund, raising millions for underprivileged children worldwide...',
          category: 'celebrity',
          source: 'Entertainment Weekly',
          publishedAt: now.toISOString(),
          url: 'https://ew.com'
        },
        {
          id: 'celebrity_2',
          title: 'Music Industry Embraces AI Technology',
          summary: 'Artists explore new creative possibilities with artificial intelligence in music production...',
          category: 'celebrity',
          source: 'Rolling Stone',
          publishedAt: new Date(now.getTime() - 2 * 60 * 60 * 1000).toISOString(),
          url: 'https://rollingstone.com'
        },
        {
          id: 'celebrity_3',
          title: 'Film Festival Announces Lineup',
          summary: 'International cinema showcase features diverse storytelling from emerging and established directors...',
          category: 'celebrity',
          source: 'Variety',
          publishedAt: new Date(now.getTime() - 4 * 60 * 60 * 1000).toISOString(),
          url: 'https://variety.com'
        },
        {
          id: 'celebrity_4',
          title: 'Fashion Week Highlights Sustainability',
          summary: 'Designers showcase eco-friendly collections and practices in major fashion capitals...',
          category: 'celebrity',
          source: 'Vogue',
          publishedAt: new Date(now.getTime() - 6 * 60 * 60 * 1000).toISOString(),
          url: 'https://vogue.com'
        },
        {
          id: 'celebrity_5',
          title: 'Celebrity Chef Opens New Restaurant',
          summary: 'Michelin-starred venue focuses on local and organic ingredients with innovative culinary techniques...',
          category: 'celebrity',
          source: 'Food & Wine',
          publishedAt: new Date(now.getTime() - 8 * 60 * 60 * 1000).toISOString(),
          url: 'https://foodandwine.com'
        }
      ],
      sports: [
        {
          id: 'sports_1',
          title: 'Championship Finals Set Record Viewership',
          summary: 'Historic match draws global audience as underdog team advances to finals in stunning upset victory...',
          category: 'sports',
          source: 'ESPN',
          publishedAt: now.toISOString(),
          url: 'https://espn.com'
        },
        {
          id: 'sports_2',
          title: 'Olympic Preparations Underway',
          summary: 'Athletes gear up for upcoming games with intensive training and qualification events...',
          category: 'sports',
          source: 'Sports Illustrated',
          publishedAt: new Date(now.getTime() - 1 * 60 * 60 * 1000).toISOString(),
          url: 'https://si.com'
        },
        {
          id: 'sports_3',
          title: 'New Stadium Opens to Fanfare',
          summary: 'State-of-the-art facility features cutting-edge technology and sustainable design elements...',
          category: 'sports',
          source: 'The Athletic',
          publishedAt: new Date(now.getTime() - 3 * 60 * 60 * 1000).toISOString(),
          url: 'https://theathletic.com'
        },
        {
          id: 'sports_4',
          title: 'Rookie Breaks Long-Standing Record',
          summary: 'Young athlete achieves milestone in debut professional season, surpassing veteran achievements...',
          category: 'sports',
          source: 'Fox Sports',
          publishedAt: new Date(now.getTime() - 5 * 60 * 60 * 1000).toISOString(),
          url: 'https://foxsports.com'
        },
        {
          id: 'sports_5',
          title: 'Team Announces New Coaching Staff',
          summary: 'Management changes signal new direction for franchise with experienced leadership team...',
          category: 'sports',
          source: 'CBS Sports',
          publishedAt: new Date(now.getTime() - 7 * 60 * 60 * 1000).toISOString(),
          url: 'https://cbssports.com'
        }
      ]
    }
  }
}

// Export singleton instance
export const newsService = new NewsService()
export default newsService
