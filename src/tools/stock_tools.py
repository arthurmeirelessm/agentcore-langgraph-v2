"""
Ferramentas para obter dados de ações
"""
import requests
from langchain.tools import tool
from src.config.settings import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@tool
def get_stock_data(symbol: str) -> str:
    """
    Get real-time stock data for a given symbol using Yahoo Finance API.
    
    Args:
        symbol: Stock symbol (e.g., NVDA, AAPL, TSLA)
    
    Returns:
        Formatted string with stock data including current price, change, and market state
    """
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        headers = {'User-Agent': settings.USER_AGENT}
        
        response = requests.get(
            url,
            headers=headers,
            timeout=settings.REQUEST_TIMEOUT
        )
        response.raise_for_status()
        
        data = response.json()
        chart = data['chart']['result'][0]
        meta = chart['meta']
        
        current_price = meta.get('regularMarketPrice', 'N/A')
        previous_close = meta.get('previousClose', 'N/A')
        currency = meta.get('currency', 'USD')
        market_state = meta.get('marketState', 'Unknown')
        exchange = meta.get('exchangeName', 'Unknown')
        
        # Calcula mudanças se dados disponíveis
        if current_price != 'N/A' and previous_close != 'N/A':
            change = current_price - previous_close
            change_percent = (change / previous_close * 100)
            
            result = f"""Stock Data for {symbol}:
Current Price: ${current_price:.2f} {currency}
Previous Close: ${previous_close:.2f}
Change: ${change:.2f} ({change_percent:.2f}%)
Market State: {market_state}
Exchange: {exchange}"""
        else:
            result = f"""Stock Data for {symbol}:
Current Price: ${current_price}
Previous Close: ${previous_close}
Currency: {currency}
Market State: {market_state}"""
        
        logger.info(f"Successfully retrieved data for {symbol}")
        return result
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Error retrieving stock data for {symbol}: {str(e)}"
        logger.error(error_msg)
        return f"Unable to retrieve stock data for {symbol}. Please try again later."
    except (KeyError, IndexError, ValueError) as e:
        error_msg = f"Error parsing stock data for {symbol}: {str(e)}"
        logger.error(error_msg)
        return f"Error processing data for {symbol}. The symbol may be invalid."
    except Exception as e:
        error_msg = f"Unexpected error for {symbol}: {str(e)}"
        logger.error(error_msg)
        return f"An unexpected error occurred while retrieving data for {symbol}."