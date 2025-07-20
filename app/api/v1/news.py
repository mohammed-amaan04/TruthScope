"""
News API endpoints for Veritas dashboard
Provides news data for the frontend dashboard
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Optional
import asyncio
import logging
from datetime import datetime, timedelta
import json
import os
import sys

# Add LLM directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'LLM'))

try:
    from LLM.news_fetcher import NewsDashboardFetcher
except ImportError:
    # Fallback if import fails
    NewsDashboardFetcher = None

from app.core.config import settings

# Setup logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Global cache for news data
news_cache = {
    'data': {},
    'last_updated': None,
    'cache_duration': timedelta(minutes=30)  # Cache for 30 minutes
}

class NewsService:
    """Service class for handling news operations"""
    
    def __init__(self):
        self.fetcher = None
        self._initialize_fetcher()
    
    def _initialize_fetcher(self):
        """Initialize the news fetcher"""
        try:
            if NewsDashboardFetcher:
                self.fetcher = NewsDashboardFetcher()
                logger.info("News fetcher initialized successfully")
            else:
                logger.warning("News fetcher not available, using fallback data")
        except Exception as e:
            logger.error(f"Failed to initialize news fetcher: {e}")
            self.fetcher = None
    
    async def get_all_news(self, force_refresh: bool = False) -> Dict[str, List[Dict]]:
        """Get news for all categories with caching"""
        
        # Check cache first
        if not force_refresh and self._is_cache_valid():
            logger.info("Returning cached news data")
            return news_cache['data']
        
        try:
            if self.fetcher:
                logger.info("Fetching fresh news data from APIs")
                news_data = await self.fetcher.fetch_all_news()
            else:
                logger.info("Using fallback news data")
                news_data = self._get_fallback_news()
            
            # Update cache
            news_cache['data'] = news_data
            news_cache['last_updated'] = datetime.now()
            
            return news_data
            
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            
            # Return cached data if available, otherwise fallback
            if news_cache['data']:
                logger.info("Returning cached data due to fetch error")
                return news_cache['data']
            else:
                logger.info("Using fallback data due to fetch error")
                return self._get_fallback_news()
    
    async def get_category_news(self, category: str) -> List[Dict]:
        """Get news for a specific category"""
        valid_categories = ['politics', 'economics', 'celebrity', 'sports']
        
        if category not in valid_categories:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid category. Must be one of: {valid_categories}"
            )
        
        try:
            if self.fetcher:
                articles = await self.fetcher.fetch_category_news(category)
                return articles
            else:
                # Return fallback data for the category
                fallback_data = self._get_fallback_news()
                return fallback_data.get(category, [])
                
        except Exception as e:
            logger.error(f"Error fetching {category} news: {e}")
            fallback_data = self._get_fallback_news()
            return fallback_data.get(category, [])
    
    def _is_cache_valid(self) -> bool:
        """Check if cached data is still valid"""
        if not news_cache['last_updated'] or not news_cache['data']:
            return False
        
        time_since_update = datetime.now() - news_cache['last_updated']
        return time_since_update < news_cache['cache_duration']
    
    def _get_fallback_news(self) -> Dict[str, List[Dict]]:
        """Get fallback news data when APIs are unavailable"""
        return {
            'politics': [
                {
                    'id': 'politics_1',
                    'title': 'Global Climate Summit Reaches Historic Agreement',
                    'summary': 'World leaders unite on unprecedented climate action plan with binding commitments for carbon neutrality by 2050...',
                    'category': 'politics',
                    'source': 'Reuters',
                    'publishedAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/politics/1'
                },
                {
                    'id': 'politics_2',
                    'title': 'Trade Relations Show Signs of Improvement',
                    'summary': 'Diplomatic talks yield positive results in ongoing trade negotiations between major economic powers...',
                    'category': 'politics',
                    'source': 'Associated Press',
                    'publishedAt': (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/politics/2'
                },
                {
                    'id': 'politics_3',
                    'title': 'Election Security Measures Enhanced',
                    'summary': 'New cybersecurity protocols implemented nationwide to protect electoral integrity...',
                    'category': 'politics',
                    'source': 'BBC News',
                    'publishedAt': (datetime.now() - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/politics/3'
                },
                {
                    'id': 'politics_4',
                    'title': 'Infrastructure Bill Passes Final Vote',
                    'summary': 'Landmark legislation promises major improvements to national infrastructure and job creation...',
                    'category': 'politics',
                    'source': 'CNN',
                    'publishedAt': (datetime.now() - timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/politics/4'
                },
                {
                    'id': 'politics_5',
                    'title': 'International Peace Talks Resume',
                    'summary': 'Diplomatic efforts continue with renewed optimism for resolution of long-standing conflicts...',
                    'category': 'politics',
                    'source': 'The Guardian',
                    'publishedAt': (datetime.now() - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/politics/5'
                }
            ],
            'economics': [
                {
                    'id': 'economics_1',
                    'title': 'Stock Markets Reach Record Highs',
                    'summary': 'Technology sector leads unprecedented growth as markets surge to new peaks amid investor optimism...',
                    'category': 'economics',
                    'source': 'Financial Times',
                    'publishedAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/economics/1'
                },
                {
                    'id': 'economics_2',
                    'title': 'Cryptocurrency Regulation Framework Announced',
                    'summary': 'New guidelines provide clarity for digital asset markets and institutional adoption...',
                    'category': 'economics',
                    'source': 'Wall Street Journal',
                    'publishedAt': (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/economics/2'
                },
                {
                    'id': 'economics_3',
                    'title': 'Unemployment Rates Hit Decade Low',
                    'summary': 'Job market shows remarkable recovery with strong hiring trends across multiple sectors...',
                    'category': 'economics',
                    'source': 'Bloomberg',
                    'publishedAt': (datetime.now() - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/economics/3'
                },
                {
                    'id': 'economics_4',
                    'title': 'Green Energy Investment Soars',
                    'summary': 'Renewable energy sector attracts record funding levels as sustainability becomes priority...',
                    'category': 'economics',
                    'source': 'Reuters',
                    'publishedAt': (datetime.now() - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/economics/4'
                },
                {
                    'id': 'economics_5',
                    'title': 'Housing Market Shows Stability',
                    'summary': 'Real estate prices stabilize after months of volatility, signaling market maturation...',
                    'category': 'economics',
                    'source': 'CNBC',
                    'publishedAt': (datetime.now() - timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/economics/5'
                }
            ],
            'celebrity': [
                {
                    'id': 'celebrity_1',
                    'title': 'Hollywood Stars Launch Charity Initiative',
                    'summary': 'A-list celebrities unite for global education fund, raising millions for underprivileged children worldwide...',
                    'category': 'celebrity',
                    'source': 'Entertainment Weekly',
                    'publishedAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/celebrity/1'
                },
                {
                    'id': 'celebrity_2',
                    'title': 'Music Industry Embraces AI Technology',
                    'summary': 'Artists explore new creative possibilities with artificial intelligence in music production...',
                    'category': 'celebrity',
                    'source': 'Rolling Stone',
                    'publishedAt': (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/celebrity/2'
                },
                {
                    'id': 'celebrity_3',
                    'title': 'Film Festival Announces Lineup',
                    'summary': 'International cinema showcase features diverse storytelling from emerging and established directors...',
                    'category': 'celebrity',
                    'source': 'Variety',
                    'publishedAt': (datetime.now() - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/celebrity/3'
                },
                {
                    'id': 'celebrity_4',
                    'title': 'Fashion Week Highlights Sustainability',
                    'summary': 'Designers showcase eco-friendly collections and practices in major fashion capitals...',
                    'category': 'celebrity',
                    'source': 'Vogue',
                    'publishedAt': (datetime.now() - timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/celebrity/4'
                },
                {
                    'id': 'celebrity_5',
                    'title': 'Celebrity Chef Opens New Restaurant',
                    'summary': 'Michelin-starred venue focuses on local and organic ingredients with innovative culinary techniques...',
                    'category': 'celebrity',
                    'source': 'Food & Wine',
                    'publishedAt': (datetime.now() - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/celebrity/5'
                }
            ],
            'sports': [
                {
                    'id': 'sports_1',
                    'title': 'Championship Finals Set Record Viewership',
                    'summary': 'Historic match draws global audience as underdog team advances to finals in stunning upset victory...',
                    'category': 'sports',
                    'source': 'ESPN',
                    'publishedAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/sports/1'
                },
                {
                    'id': 'sports_2',
                    'title': 'Olympic Preparations Underway',
                    'summary': 'Athletes gear up for upcoming games with intensive training and qualification events...',
                    'category': 'sports',
                    'source': 'Sports Illustrated',
                    'publishedAt': (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/sports/2'
                },
                {
                    'id': 'sports_3',
                    'title': 'New Stadium Opens to Fanfare',
                    'summary': 'State-of-the-art facility features cutting-edge technology and sustainable design elements...',
                    'category': 'sports',
                    'source': 'The Athletic',
                    'publishedAt': (datetime.now() - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/sports/3'
                },
                {
                    'id': 'sports_4',
                    'title': 'Rookie Breaks Long-Standing Record',
                    'summary': 'Young athlete achieves milestone in debut professional season, surpassing veteran achievements...',
                    'category': 'sports',
                    'source': 'Fox Sports',
                    'publishedAt': (datetime.now() - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/sports/4'
                },
                {
                    'id': 'sports_5',
                    'title': 'Team Announces New Coaching Staff',
                    'summary': 'Management changes signal new direction for franchise with experienced leadership team...',
                    'category': 'sports',
                    'source': 'CBS Sports',
                    'publishedAt': (datetime.now() - timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': 'https://example.com/sports/5'
                }
            ]
        }

# Initialize the service
news_service = NewsService()

@router.get("/news/all")
async def get_all_news(refresh: bool = False):
    """
    Get top 5 news articles for all categories
    
    - **refresh**: Force refresh of cached data
    """
    try:
        news_data = await news_service.get_all_news(force_refresh=refresh)
        
        return {
            "status": "success",
            "data": news_data,
            "last_updated": news_cache['last_updated'].isoformat() if news_cache['last_updated'] else None,
            "categories": list(news_data.keys()),
            "total_articles": sum(len(articles) for articles in news_data.values())
        }
        
    except Exception as e:
        logger.error(f"Error in get_all_news endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch news data")

@router.get("/news/{category}")
async def get_category_news(category: str):
    """
    Get top 5 news articles for a specific category
    
    - **category**: One of: politics, economics, celebrity, sports
    """
    try:
        articles = await news_service.get_category_news(category)
        
        return {
            "status": "success",
            "category": category,
            "data": articles,
            "count": len(articles)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_category_news endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch {category} news")

@router.post("/news/refresh")
async def refresh_news_cache(background_tasks: BackgroundTasks):
    """
    Manually refresh the news cache
    """
    try:
        # Refresh in background to avoid timeout
        background_tasks.add_task(news_service.get_all_news, True)
        
        return {
            "status": "success",
            "message": "News cache refresh initiated",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in refresh_news_cache endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to refresh news cache")

@router.get("/news/status")
async def get_news_status():
    """
    Get status information about the news service
    """
    return {
        "status": "success",
        "service_available": news_service.fetcher is not None,
        "cache_valid": news_service._is_cache_valid(),
        "last_updated": news_cache['last_updated'].isoformat() if news_cache['last_updated'] else None,
        "cache_duration_minutes": news_cache['cache_duration'].total_seconds() / 60,
        "categories": ['politics', 'economics', 'celebrity', 'sports']
    }
