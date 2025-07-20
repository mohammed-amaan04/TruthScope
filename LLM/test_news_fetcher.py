"""
Test script for the news fetcher
Run this to test if the news fetcher is working correctly
"""

import asyncio
import sys
import os

# Add the LLM directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from news_fetcher import NewsDashboardFetcher

async def test_news_fetcher():
    """Test the news fetcher functionality"""
    print("🔍 Testing Veritas News Fetcher...")
    print("=" * 50)
    
    try:
        # Initialize the fetcher
        fetcher = NewsDashboardFetcher()
        print("✅ News fetcher initialized successfully")
        
        # Test fetching all categories
        print("\n📰 Fetching news for all categories...")
        all_news = await fetcher.fetch_all_news()
        
        # Display results
        for category, articles in all_news.items():
            print(f"\n🏷️  {category.upper()} NEWS ({len(articles)} articles)")
            print("-" * 40)
            
            for i, article in enumerate(articles, 1):
                print(f"{i}. {article['title']}")
                print(f"   📅 {article['publishedAt']}")
                print(f"   📝 {article['summary']}")
                print(f"   🔗 {article['source']}")
                print(f"   🌐 {article['url']}")
                print()
        
        print("✅ News fetching completed successfully!")
        
        # Test individual category
        print("\n🎯 Testing individual category fetch (politics)...")
        politics_news = await fetcher.fetch_category_news('politics')
        print(f"✅ Fetched {len(politics_news)} politics articles")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_description_generator():
    """Test the description generator separately"""
    print("\n🤖 Testing LLM Description Generator...")
    
    try:
        from news_fetcher import NewsDescriptionGenerator
        
        generator = NewsDescriptionGenerator()
        
        # Test headlines
        test_headlines = [
            "Global Climate Summit Reaches Historic Agreement",
            "Stock Markets Surge to Record Highs",
            "Celebrity Chef Opens Revolutionary Restaurant",
            "Championship Finals Break Viewership Records"
        ]
        
        for headline in test_headlines:
            description = generator.generate_description(headline)
            print(f"📰 {headline}")
            print(f"📝 {description}")
            print()
        
        print("✅ Description generator working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Description generator error: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Starting Veritas News Fetcher Tests")
    print("=" * 60)
    
    # Test description generator first (doesn't require API)
    desc_success = test_description_generator()
    
    # Test news fetcher
    news_success = await test_news_fetcher()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS:")
    print(f"   Description Generator: {'✅ PASS' if desc_success else '❌ FAIL'}")
    print(f"   News Fetcher: {'✅ PASS' if news_success else '❌ FAIL'}")
    
    if desc_success and news_success:
        print("\n🎉 All tests passed! News fetcher is ready to use.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        
        if not news_success:
            print("\n💡 Tips for fixing news fetcher issues:")
            print("   1. Make sure you have NEWSAPI_KEY in your .env file")
            print("   2. Install required dependencies: pip install aiohttp")
            print("   3. Check your internet connection")

if __name__ == "__main__":
    asyncio.run(main())
