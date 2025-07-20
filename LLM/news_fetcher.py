"""
News Fetcher for Veritas Dashboard
Fetches top 5 news articles for each genre: Politics, Economics, Celebrity, Sports
"""

import asyncio
import aiohttp
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from dataclasses import dataclass
import json
import re

# LLM imports
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NewsArticle:
    """Data class for news articles"""
    headline: str
    time: str
    description: str
    url: str
    source: str
    category: str

class NewsDescriptionGenerator:
    """Generates engaging descriptions using LLM"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the LLM model for description generation"""
        try:
            model_name = "microsoft/DialoGPT-medium"  # Lightweight model for descriptions
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            logger.info(f"Initialized LLM model on {self.device}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM model: {e}")
            self.model = None
    
    def generate_description(self, headline: str, content: str = "") -> str:
        """Generate an engaging description from headline and content"""
        if not self.model:
            # Fallback: extract first sentence and add ellipsis
            return self._fallback_description(headline, content)
        
        try:
            # Create prompt for description generation
            prompt = f"Create a brief, engaging news description for: {headline}"
            if content:
                prompt += f" Content: {content[:200]}"
            
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 50,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            description = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            description = description.replace(prompt, "").strip()
            
            # Clean and format description
            description = self._clean_description(description)
            return description + "..."
            
        except Exception as e:
            logger.error(f"LLM description generation failed: {e}")
            return self._fallback_description(headline, content)
    
    def _fallback_description(self, headline: str, content: str = "") -> str:
        """Fallback description generation without LLM"""
        if content:
            # Extract first meaningful sentence
            sentences = re.split(r'[.!?]+', content)
            for sentence in sentences:
                if len(sentence.strip()) > 20:
                    return sentence.strip()[:100] + "..."
        
        # Generate from headline
        words = headline.split()
        if len(words) > 8:
            return " ".join(words[:8]) + "..."
        return headline + "..."
    
    def _clean_description(self, description: str) -> str:
        """Clean and format the generated description"""
        # Remove extra whitespace and newlines
        description = re.sub(r'\s+', ' ', description).strip()
        
        # Limit length
        if len(description) > 120:
            description = description[:120]
            # Cut at last complete word
            last_space = description.rfind(' ')
            if last_space > 80:
                description = description[:last_space]
        
        return description

class NewsAPIFetcher:
    """Fetches news from various APIs"""
    
    def __init__(self):
        self.news_api_key = os.getenv('NEWSAPI_KEY')
        self.description_generator = NewsDescriptionGenerator()
        
        # Category mappings for different APIs
        self.category_mappings = {
            'politics': ['politics', 'government', 'election', 'policy'],
            'economics': ['business', 'economy', 'finance', 'market'],
            'celebrity': ['entertainment', 'celebrity', 'hollywood', 'music'],
            'sports': ['sports', 'football', 'basketball', 'soccer']
        }
    
    async def fetch_news_for_category(self, category: str, limit: int = 5) -> List[NewsArticle]:
        """Fetch news for a specific category"""
        articles = []
        
        try:
            # Try NewsAPI first
            if self.news_api_key:
                newsapi_articles = await self._fetch_from_newsapi(category, limit)
                articles.extend(newsapi_articles)
            
            # If we don't have enough articles, try other sources
            if len(articles) < limit:
                remaining = limit - len(articles)
                # Add other news sources here (RSS feeds, etc.)
                fallback_articles = await self._fetch_fallback_news(category, remaining)
                articles.extend(fallback_articles)
            
            # Generate descriptions using LLM
            for article in articles:
                if not article.description or len(article.description) < 20:
                    article.description = self.description_generator.generate_description(
                        article.headline, article.description
                    )
            
            return articles[:limit]
            
        except Exception as e:
            logger.error(f"Error fetching news for {category}: {e}")
            return self._get_fallback_articles(category, limit)
    
    async def _fetch_from_newsapi(self, category: str, limit: int) -> List[NewsArticle]:
        """Fetch news from NewsAPI"""
        if not self.news_api_key:
            return []
        
        articles = []
        category_terms = self.category_mappings.get(category, [category])
        
        async with aiohttp.ClientSession() as session:
            for term in category_terms[:2]:  # Try first 2 terms
                try:
                    url = "https://newsapi.org/v2/everything"
                    params = {
                        'q': term,
                        'apiKey': self.news_api_key,
                        'language': 'en',
                        'sortBy': 'publishedAt',
                        'pageSize': limit,
                        'from': (datetime.now() - timedelta(days=2)).isoformat()
                    }
                    
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            for item in data.get('articles', []):
                                if len(articles) >= limit:
                                    break
                                
                                article = NewsArticle(
                                    headline=item.get('title', ''),
                                    time=self._format_time(item.get('publishedAt', '')),
                                    description=item.get('description', ''),
                                    url=item.get('url', ''),
                                    source=item.get('source', {}).get('name', 'Unknown'),
                                    category=category
                                )
                                
                                if article.headline and article.url:
                                    articles.append(article)
                    
                    if len(articles) >= limit:
                        break
                        
                except Exception as e:
                    logger.error(f"NewsAPI error for {term}: {e}")
                    continue
        
        return articles
    
    async def _fetch_fallback_news(self, category: str, limit: int) -> List[NewsArticle]:
        """Fetch news from fallback sources (RSS feeds, etc.)"""
        # This is where you could add RSS feeds or other news sources
        # For now, return empty list
        return []
    
    def _get_fallback_articles(self, category: str, limit: int) -> List[NewsArticle]:
        """Generate fallback articles when APIs fail"""
        fallback_data = {
            'politics': [
                "Global Climate Summit Reaches Historic Agreement",
                "Trade Relations Show Signs of Improvement", 
                "Election Security Measures Enhanced",
                "Infrastructure Bill Passes Final Vote",
                "International Peace Talks Resume"
            ],
            'economics': [
                "Stock Markets Reach Record Highs",
                "Cryptocurrency Regulation Framework Announced",
                "Unemployment Rates Hit Decade Low",
                "Green Energy Investment Soars",
                "Housing Market Shows Stability"
            ],
            'celebrity': [
                "Hollywood Stars Launch Charity Initiative",
                "Music Industry Embraces AI Technology",
                "Film Festival Announces Lineup",
                "Fashion Week Highlights Sustainability",
                "Celebrity Chef Opens New Restaurant"
            ],
            'sports': [
                "Championship Finals Set Record Viewership",
                "Olympic Preparations Underway",
                "New Stadium Opens to Fanfare",
                "Rookie Breaks Long-Standing Record",
                "Team Announces New Coaching Staff"
            ]
        }
        
        headlines = fallback_data.get(category, [])
        articles = []
        
        for i, headline in enumerate(headlines[:limit]):
            article = NewsArticle(
                headline=headline,
                time=self._format_time(datetime.now().isoformat()),
                description=self.description_generator.generate_description(headline),
                url=f"https://example.com/news/{category}/{i+1}",
                source="News Source",
                category=category
            )
            articles.append(article)
        
        return articles
    
    def _format_time(self, time_str: str) -> str:
        """Format time string to readable format"""
        try:
            if time_str:
                dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except:
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class NewsDashboardFetcher:
    """Main class for fetching dashboard news"""
    
    def __init__(self):
        self.api_fetcher = NewsAPIFetcher()
        self.categories = ['politics', 'economics', 'celebrity', 'sports']
    
    async def fetch_all_news(self) -> Dict[str, List[Dict]]:
        """Fetch top 5 news for all categories"""
        logger.info("Starting news fetch for all categories")
        
        tasks = []
        for category in self.categories:
            task = self.api_fetcher.fetch_news_for_category(category, 5)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        news_data = {}
        for i, category in enumerate(self.categories):
            if isinstance(results[i], Exception):
                logger.error(f"Error fetching {category}: {results[i]}")
                news_data[category] = []
            else:
                articles = results[i]
                news_data[category] = [
                    {
                        'id': f"{category}_{j+1}",
                        'title': article.headline,
                        'summary': article.description,
                        'category': category,
                        'source': article.source,
                        'publishedAt': article.time,
                        'url': article.url
                    }
                    for j, article in enumerate(articles)
                ]
        
        logger.info(f"Successfully fetched news for {len(news_data)} categories")
        return news_data
    
    async def fetch_category_news(self, category: str) -> List[Dict]:
        """Fetch news for a specific category"""
        if category not in self.categories:
            raise ValueError(f"Invalid category. Must be one of: {self.categories}")
        
        articles = await self.api_fetcher.fetch_news_for_category(category, 5)
        
        return [
            {
                'id': f"{category}_{i+1}",
                'title': article.headline,
                'summary': article.description,
                'category': category,
                'source': article.source,
                'publishedAt': article.time,
                'url': article.url
            }
            for i, article in enumerate(articles)
        ]

# Main execution function
async def main():
    """Test the news fetcher"""
    fetcher = NewsDashboardFetcher()
    
    # Fetch all news
    all_news = await fetcher.fetch_all_news()
    
    # Print results
    for category, articles in all_news.items():
        print(f"\n=== {category.upper()} NEWS ===")
        for article in articles:
            print(f"Title: {article['title']}")
            print(f"Time: {article['publishedAt']}")
            print(f"Description: {article['summary']}")
            print(f"Source: {article['source']}")
            print(f"URL: {article['url']}")
            print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
