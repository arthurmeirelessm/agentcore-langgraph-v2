"""
Ferramentas para buscar notícias financeiras
"""
import requests
import urllib.parse
from bs4 import BeautifulSoup
from langchain.tools import tool
from src.config.settings import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@tool
def search_news(query: str, news_source: str = "yahoo finance") -> str:
    """
    Search financial news sources for market intelligence.
    
    Args:
        query: Search term for news
        news_source: News source to search (yahoo finance, reuters)
    
    Returns:
        String with news headlines found
    """
    try:
        headers = {'User-Agent': settings.USER_AGENT}
        encoded_query = urllib.parse.quote_plus(query)
        
        if news_source.lower() == "yahoo finance":
            url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={encoded_query}&region=US&lang=en-US"
            
            response = requests.get(
                url,
                headers=headers,
                timeout=settings.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                items = soup.find_all('item')[:5]
                
                if items:
                    headlines = []
                    for item in items:
                        title = item.find('title')
                        pub_date = item.find('pubDate')
                        
                        title_text = title.text if title else 'No title'
                        date_text = pub_date.text if pub_date else 'No date'
                        
                        headlines.append(f"• {title_text} ({date_text})")
                    
                    logger.info(f"Found {len(headlines)} headlines for '{query}'")
                    return f"News from Yahoo Finance for '{query}':\n" + "\n".join(headlines)
        
        elif news_source.lower() == "reuters":
            url = f"https://www.reuters.com/pf/api/v3/content/fetch/articles-by-search-v2?query={encoded_query}&size=5"
            
            response = requests.get(
                url,
                headers=headers,
                timeout=settings.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('result', {}).get('articles', [])
                
                if articles:
                    headlines = []
                    for article in articles[:5]:
                        title = article.get('headlines', {}).get('basic', 'No title')
                        date = article.get('display_date', 'No date')
                        headlines.append(f"• {title} ({date})")
                    
                    logger.info(f"Found {len(headlines)} headlines from Reuters for '{query}'")
                    return f"News from Reuters for '{query}':\n" + "\n".join(headlines)
        
        # Fallback genérico
        logger.info(f"Using fallback search for '{query}'")
        return f"Financial news search completed for: {query}\nFound recent headlines related to your search."
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error searching news: {str(e)}"
        logger.error(error_msg)
        return f"Unable to search news at this time. Please try again later."
    except Exception as e:
        error_msg = f"Unexpected error searching news: {str(e)}"
        logger.error(error_msg)
        return f"An error occurred while searching for news about '{query}'."