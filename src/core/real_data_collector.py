"""
Real Data Collection Module
Provides actual web search, news, and market data
"""
import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import json
import time
from datetime import datetime, timedelta
import re
from urllib.parse import urljoin, urlparse
from src.core.logger import logger

class WebSearcher:
    """Performs real web searches and data collection"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        })
    
    async def search_duckduckgo(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search DuckDuckGo for current information"""
        try:
            from ddgs import DDGS
            
            results = []
            with DDGS() as ddgs:
                search_results = ddgs.text(query, max_results=max_results)
                
                for result in search_results:
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('href', ''),
                        'snippet': result.get('body', ''),
                        'source': 'duckduckgo'
                    })
            
            logger.info(f"Found {len(results)} DuckDuckGo results for: {query}")
            return results
            
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
            return []
    
    async def get_wikipedia_summary(self, topic: str) -> Dict:
        """Get Wikipedia summary for topic"""
        try:
            import wikipedia
            
            # Search for the topic
            search_results = wikipedia.search(topic, results=3)
            if not search_results:
                return {"error": "No Wikipedia results found"}
            
            # Get summary of the first result
            page = wikipedia.page(search_results[0])
            
            return {
                'title': page.title,
                'summary': page.summary,  # Remove 1000 char limit - show full summary
                'url': page.url,
                'source': 'wikipedia'
            }
            
        except Exception as e:
            logger.error(f"Wikipedia search failed: {e}")
            return {"error": str(e)}
    
    async def scrape_webpage(self, url: str) -> Dict:
        """Scrape content from a webpage"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return {
                'url': url,
                'title': soup.title.string if soup.title else '',
                'content': text,  # Remove 2000 char limit - show full content
                'word_count': len(text.split()),
                'scraped_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Web scraping failed for {url}: {e}")
            return {"error": str(e), "url": url}
    
    async def get_news_articles(self, topic: str, days_back: int = 7) -> List[Dict]:
        """Get recent news articles about topic"""
        try:
            # Using RSS feeds from major news sources
            news_sources = [
                'https://rss.cnn.com/rss/edition.rss',
                'https://feeds.bbci.co.uk/news/rss.xml',
                'https://www.reuters.com/tools/rss'
            ]
            
            articles = []
            
            import feedparser
            
            for source_url in news_sources:
                try:
                    feed = feedparser.parse(source_url)
                    
                    for entry in feed.entries[:10]:  # Increase from 5 to 10 entries per source
                        # Check if article is relevant to topic
                        if topic.lower() in entry.title.lower() or topic.lower() in entry.summary.lower():
                            articles.append({
                                'title': entry.title,
                                'summary': entry.summary,  # Remove 300 char limit - show full summary
                                'url': entry.link,
                                'published': entry.published if hasattr(entry, 'published') else '',
                                'source': feed.feed.title if hasattr(feed.feed, 'title') else 'Unknown'
                            })
                            
                except Exception as e:
                    logger.warning(f"Failed to parse feed {source_url}: {e}")
                    continue
            
            logger.info(f"Found {len(articles)} relevant news articles for: {topic}")
            return articles[:20]  # Increase from 10 to 20 total articles
            
        except Exception as e:
            logger.error(f"News search failed: {e}")
            return []
    
    async def get_market_data(self, symbol: str) -> Dict:
        """Get stock/market data"""
        try:
            import yfinance as yf
            
            ticker = yf.Ticker(symbol)
            info = ticker.info
            history = ticker.history(period="1mo")
            
            current_price = history['Close'].iloc[-1] if not history.empty else None
            price_change = ((current_price - history['Close'].iloc[0]) / history['Close'].iloc[0] * 100) if not history.empty and len(history) > 1 else 0
            
            return {
                'symbol': symbol,
                'current_price': float(current_price) if current_price else None,
                'price_change_30d': float(price_change) if price_change else 0,
                'company_name': info.get('longName', 'Unknown'),
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'source': 'yahoo_finance',
                'retrieved_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Market data retrieval failed for {symbol}: {e}")
            return {"error": str(e), "symbol": symbol}

class RealDataCollector:
    """Main class for collecting real data from multiple sources"""
    
    def __init__(self):
        self.web_searcher = WebSearcher()
    
    async def comprehensive_research(self, topic: str, questions: List[str] = None) -> Dict:
        """Perform comprehensive research using multiple real data sources"""
        
        logger.info(f"Starting comprehensive research on: {topic}")
        
        research_data = {
            'topic': topic,
            'research_started_at': datetime.utcnow().isoformat(),
            'sources_used': [],
            'findings': {}
        }
        
        # 1. Web Search
        logger.info("Searching web...")
        web_results = await self.web_searcher.search_duckduckgo(topic, max_results=8)
        if web_results:
            research_data['findings']['web_search'] = web_results
            research_data['sources_used'].append('web_search')
        
        # 2. Wikipedia Summary
        logger.info("Getting Wikipedia data...")
        wiki_data = await self.web_searcher.get_wikipedia_summary(topic)
        if 'error' not in wiki_data:
            research_data['findings']['wikipedia'] = wiki_data
            research_data['sources_used'].append('wikipedia')
        
        # 3. News Articles
        logger.info("Searching for news...")
        news_articles = await self.web_searcher.get_news_articles(topic)
        if news_articles:
            research_data['findings']['news'] = news_articles
            research_data['sources_used'].append('news')
        
        # 4. Market Data (if topic seems financial)
        financial_keywords = [
            'stock', 'stocks', 'company', 'companies', 'market', 'markets', 
            'share', 'shares', 'equity', 'investment', 'trading', 'ticker',
            'nasdaq', 'nyse', 'sp500', 's&p', 'dow', 'price', 'valuation',
            # Company names
            'tesla', 'apple', 'google', 'microsoft', 'amazon', 'meta', 
            'facebook', 'netflix', 'nvidia', 'intel', 'amd', 'ibm',
            'oracle', 'salesforce', 'adobe', 'twitter', 'uber', 'lyft',
            'airbnb', 'spotify', 'zoom', 'slack', 'dropbox', 'paypal',
            # Stock symbols (if typed explicitly)
            'tsla', 'aapl', 'googl', 'msft', 'amzn', 'meta', 'nflx', 'nvda'
        ]
        if any(keyword in topic.lower() for keyword in financial_keywords):
            logger.info("Topic appears financial - Getting market data...")
            # Try to extract company symbols
            potential_symbols = self._extract_stock_symbols(topic)
            if potential_symbols:
                market_data = []
                for symbol in potential_symbols[:3]:  # Max 3 symbols
                    data = await self.web_searcher.get_market_data(symbol)
                    if 'error' not in data:
                        market_data.append(data)
                
                if market_data:
                    research_data['findings']['market_data'] = market_data
                    research_data['sources_used'].append('market_data')
        
        # 5. Detailed Content from Top URLs
        logger.info("Scraping detailed content...")
        if 'web_search' in research_data['findings']:
            top_urls = [result['url'] for result in research_data['findings']['web_search'][:3]]
            scraped_content = []
            
            for url in top_urls:
                content = await self.web_searcher.scrape_webpage(url)
                if 'error' not in content:
                    scraped_content.append(content)
            
            if scraped_content:
                research_data['findings']['detailed_content'] = scraped_content
                research_data['sources_used'].append('detailed_content')
        
        research_data['research_completed_at'] = datetime.utcnow().isoformat()
        research_data['total_sources'] = len(research_data['sources_used'])
        
        logger.info(f"Research completed! Used {research_data['total_sources']} data sources")
        
        return research_data
    
    def _extract_stock_symbols(self, text: str) -> List[str]:
        """Extract potential stock symbols from text"""
        # Common company mappings
        company_symbols = {
            # Tech Giants
            'tesla': 'TSLA',
            'apple': 'AAPL', 
            'microsoft': 'MSFT',
            'google': 'GOOGL',
            'alphabet': 'GOOGL',
            'amazon': 'AMZN',
            'meta': 'META',
            'facebook': 'META',
            'netflix': 'NFLX',
            'nvidia': 'NVDA',
            'intel': 'INTC',
            'amd': 'AMD',
            'ibm': 'IBM',
            # Other Companies
            'oracle': 'ORCL',
            'salesforce': 'CRM',
            'adobe': 'ADBE',
            'uber': 'UBER',
            'airbnb': 'ABNB',
            'spotify': 'SPOT',
            'zoom': 'ZM',
            'paypal': 'PYPL',
            'shopify': 'SHOP',
            'snap': 'SNAP',
            'coinbase': 'COIN',
            'walmart': 'WMT',
            'disney': 'DIS',
            'nike': 'NKE',
            'starbucks': 'SBUX'
        }
        
        symbols = []
        text_lower = text.lower()
        
        for company, symbol in company_symbols.items():
            if company in text_lower:
                symbols.append(symbol)
        
        # Also look for explicit stock symbols (3-5 uppercase letters)
        import re
        symbol_pattern = r'\b[A-Z]{3,5}\b'
        found_symbols = re.findall(symbol_pattern, text)
        symbols.extend(found_symbols)
        
        # If no symbols found, default to popular tech stocks
        if not symbols:
            logger.info("No specific companies found, using default tech stocks")
            symbols = ['AAPL', 'MSFT', 'GOOGL']
        
        return list(set(symbols))[:5]  # Remove duplicates, limit to 5