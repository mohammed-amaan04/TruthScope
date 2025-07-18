"""
News Source Weighting System
Based on annotations.xml categorization with sophisticated weight calculation
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

class NewsSourceWeights:
    """
    Sophisticated news source weighting system based on:
    - Category (Global, National, Local, Specialized)
    - Region (Global, India, Hyderabad)
    - Expertise (General, Business, Sports, etc.)
    - Timeline (Recency factor)
    """
    
    def __init__(self):
        self.source_database = self._build_source_database()
        
    def _build_source_database(self) -> Dict[str, Dict]:
        """Build comprehensive source database from annotations.xml"""
        return {
            # 🌍 GLOBAL NEWS - Highest credibility, worldwide reach
            "bbc.com": {
                "category": "global",
                "region": "global", 
                "expertise": "general",
                "credibility": 0.95,
                "reach": "international",
                "bias": "center",
                "established": 1922
            },
            "reuters.com": {
                "category": "global",
                "region": "global",
                "expertise": "general", 
                "credibility": 0.98,
                "reach": "international",
                "bias": "center",
                "established": 1851
            },
            "cnn.com": {
                "category": "global",
                "region": "global",
                "expertise": "general",
                "credibility": 0.85,
                "reach": "international", 
                "bias": "center-left",
                "established": 1980
            },
            "aljazeera.com": {
                "category": "global",
                "region": "middle-east",
                "expertise": "general",
                "credibility": 0.80,
                "reach": "international",
                "bias": "center",
                "established": 1996
            },
            "theguardian.com": {
                "category": "global",
                "region": "global",
                "expertise": "general",
                "credibility": 0.88,
                "reach": "international",
                "bias": "center-left", 
                "established": 1821
            },
            "apnews.com": {
                "category": "global",
                "region": "global",
                "expertise": "general",
                "credibility": 0.96,
                "reach": "international",
                "bias": "center",
                "established": 1846
            },
            
            # 🇮🇳 INDIA NATIONAL - High credibility for Indian topics
            "thehindu.com": {
                "category": "national",
                "region": "india",
                "expertise": "general",
                "credibility": 0.92,
                "reach": "national",
                "bias": "center-left",
                "established": 1878
            },
            "timesofindia.indiatimes.com": {
                "category": "national", 
                "region": "india",
                "expertise": "general",
                "credibility": 0.75,
                "reach": "national",
                "bias": "center",
                "established": 1838
            },
            "indianexpress.com": {
                "category": "national",
                "region": "india", 
                "expertise": "general",
                "credibility": 0.88,
                "reach": "national",
                "bias": "center",
                "established": 1932
            },
            "scroll.in": {
                "category": "national",
                "region": "india",
                "expertise": "general",
                "credibility": 0.82,
                "reach": "national",
                "bias": "center-left",
                "established": 2012
            },
            "hindustantimes.com": {
                "category": "national",
                "region": "india",
                "expertise": "general", 
                "credibility": 0.80,
                "reach": "national",
                "bias": "center",
                "established": 1924
            },
            "news18.com": {
                "category": "national",
                "region": "india",
                "expertise": "general",
                "credibility": 0.70,
                "reach": "national",
                "bias": "center-right",
                "established": 2005
            },
            
            # 📰 HYDERABAD LOCAL - Regional expertise
            "telanganatoday.com": {
                "category": "local",
                "region": "hyderabad",
                "expertise": "regional",
                "credibility": 0.75,
                "reach": "regional",
                "bias": "center",
                "established": 2013
            },
            "siasat.com": {
                "category": "local",
                "region": "hyderabad", 
                "expertise": "regional",
                "credibility": 0.70,
                "reach": "regional",
                "bias": "center",
                "established": 1948
            },
            "deccanchronicle.com": {
                "category": "local",
                "region": "hyderabad",
                "expertise": "regional",
                "credibility": 0.78,
                "reach": "regional",
                "bias": "center",
                "established": 1938
            },
            "ntnews.com": {
                "category": "local",
                "region": "hyderabad",
                "expertise": "regional", 
                "credibility": 0.65,
                "reach": "regional",
                "bias": "center",
                "established": 2010
            },
            "eenadu.net": {
                "category": "local",
                "region": "hyderabad",
                "expertise": "regional",
                "credibility": 0.80,
                "reach": "regional",
                "bias": "center",
                "established": 1974
            },
            
            # 💼 BUSINESS NEWS - Specialized expertise
            "economictimes.indiatimes.com": {
                "category": "specialized",
                "region": "india",
                "expertise": "business",
                "credibility": 0.90,
                "reach": "national",
                "bias": "center",
                "established": 1961
            },
            "moneycontrol.com": {
                "category": "specialized",
                "region": "india",
                "expertise": "business",
                "credibility": 0.85,
                "reach": "national", 
                "bias": "center",
                "established": 1999
            },
            "business-standard.com": {
                "category": "specialized",
                "region": "india",
                "expertise": "business",
                "credibility": 0.88,
                "reach": "national",
                "bias": "center",
                "established": 1975
            },
            "bloomberg.com": {
                "category": "specialized",
                "region": "global",
                "expertise": "business",
                "credibility": 0.95,
                "reach": "international",
                "bias": "center",
                "established": 1981
            },
            "cnbc.com": {
                "category": "specialized",
                "region": "global", 
                "expertise": "business",
                "credibility": 0.85,
                "reach": "international",
                "bias": "center",
                "established": 1989
            },
            "livemint.com": {
                "category": "specialized",
                "region": "india",
                "expertise": "business",
                "credibility": 0.82,
                "reach": "national",
                "bias": "center",
                "established": 2007
            },
            
            # ⚽ SPORTS NEWS - Specialized expertise
            "espn.in": {
                "category": "specialized",
                "region": "india",
                "expertise": "sports",
                "credibility": 0.88,
                "reach": "national",
                "bias": "center",
                "established": 1979
            },
            "cricbuzz.com": {
                "category": "specialized",
                "region": "india",
                "expertise": "sports",
                "credibility": 0.85,
                "reach": "national",
                "bias": "center",
                "established": 2004
            },
            "sportskeeda.com": {
                "category": "specialized",
                "region": "india",
                "expertise": "sports",
                "credibility": 0.70,
                "reach": "national",
                "bias": "center",
                "established": 2009
            },
            "sports.ndtv.com": {
                "category": "specialized",
                "region": "india",
                "expertise": "sports",
                "credibility": 0.80,
                "reach": "national",
                "bias": "center",
                "established": 1988
            },
            "olympics.com": {
                "category": "specialized",
                "region": "global",
                "expertise": "sports",
                "credibility": 0.95,
                "reach": "international",
                "bias": "center",
                "established": 1894
            }
        }
    
    def extract_domain(self, url: str) -> str:
        """Extract clean domain from URL"""
        try:
            domain = urlparse(url).netloc.lower()
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except:
            return ""
    
    def get_source_info(self, url: str) -> Dict:
        """Get source information for a given URL"""
        domain = self.extract_domain(url)
        
        # Direct match
        if domain in self.source_database:
            return self.source_database[domain]
        
        # Partial match for subdomains
        for source_domain, info in self.source_database.items():
            if source_domain in domain or domain in source_domain:
                return info
        
        # Default for unknown sources
        return {
            "category": "unknown",
            "region": "unknown",
            "expertise": "general",
            "credibility": 0.50,
            "reach": "unknown",
            "bias": "unknown",
            "established": 2000
        }
    
    def calculate_source_weight(self, url: str, claim_category: str = "general", 
                              claim_region: str = "global") -> float:
        """
        Calculate comprehensive weight for a news source
        
        Args:
            url: Article URL
            claim_category: Category of the claim (business, sports, general, etc.)
            claim_region: Geographic relevance (global, india, hyderabad)
        
        Returns:
            Weight between 0.0 and 1.0
        """
        source_info = self.get_source_info(url)
        
        # Base credibility weight (40% of total)
        credibility_weight = source_info["credibility"] * 0.4
        
        # Category expertise bonus (25% of total)
        expertise_bonus = 0.0
        if source_info["expertise"] == claim_category:
            expertise_bonus = 0.25  # Perfect match
        elif source_info["expertise"] == "general":
            expertise_bonus = 0.15  # General coverage
        else:
            expertise_bonus = 0.10  # Different specialty
        
        # Regional relevance bonus (20% of total)
        region_bonus = 0.0
        if source_info["region"] == claim_region:
            region_bonus = 0.20  # Perfect regional match
        elif source_info["region"] == "global":
            region_bonus = 0.15  # Global sources are always relevant
        elif claim_region == "global":
            region_bonus = 0.12  # Local sources for global claims
        else:
            region_bonus = 0.08  # Different regions
        
        # Reach multiplier (15% of total)
        reach_multiplier = {
            "international": 0.15,
            "national": 0.12,
            "regional": 0.08,
            "unknown": 0.05
        }.get(source_info["reach"], 0.05)
        
        # Calculate final weight
        total_weight = credibility_weight + expertise_bonus + region_bonus + reach_multiplier
        
        # Ensure weight is between 0.0 and 1.0
        return min(max(total_weight, 0.0), 1.0)
    
    def calculate_recency_factor(self, published_date: str) -> float:
        """Calculate recency factor (1.0 = today, decreases with age)"""
        try:
            if not published_date:
                return 0.5  # Default for unknown dates
            
            # Parse date (handle various formats)
            pub_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
            now = datetime.now(pub_date.tzinfo)
            
            days_old = (now - pub_date).days
            
            # Recency scoring
            if days_old == 0:
                return 1.0  # Today
            elif days_old <= 1:
                return 0.9  # Yesterday
            elif days_old <= 7:
                return 0.8  # This week
            elif days_old <= 30:
                return 0.6  # This month
            elif days_old <= 90:
                return 0.4  # Last 3 months
            else:
                return 0.2  # Older than 3 months
                
        except Exception as e:
            logger.warning(f"Error parsing date {published_date}: {e}")
            return 0.5
    
    def get_category_from_claim(self, claim: str) -> str:
        """Determine claim category from text analysis"""
        claim_lower = claim.lower()
        
        # Business keywords
        business_keywords = ['stock', 'market', 'economy', 'financial', 'business', 
                           'revenue', 'profit', 'investment', 'bank', 'currency']
        if any(keyword in claim_lower for keyword in business_keywords):
            return "business"
        
        # Sports keywords  
        sports_keywords = ['cricket', 'football', 'sports', 'match', 'tournament',
                          'olympics', 'player', 'team', 'score', 'game']
        if any(keyword in claim_lower for keyword in sports_keywords):
            return "sports"
        
        # Default to general
        return "general"
    
    def get_region_from_claim(self, claim: str) -> str:
        """Determine geographic relevance from claim"""
        claim_lower = claim.lower()
        
        # Hyderabad/Telangana keywords
        hyderabad_keywords = ['hyderabad', 'telangana', 'secunderabad', 'cyberabad']
        if any(keyword in claim_lower for keyword in hyderabad_keywords):
            return "hyderabad"
        
        # India keywords
        india_keywords = ['india', 'indian', 'delhi', 'mumbai', 'bangalore', 'chennai']
        if any(keyword in claim_lower for keyword in india_keywords):
            return "india"
        
        # Default to global
        return "global"

# Global instance
news_weights = NewsSourceWeights()
