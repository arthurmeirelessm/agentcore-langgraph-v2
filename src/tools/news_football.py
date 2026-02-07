"""
Ferramenta para buscar notícias de futebol via Google News RSS
Suporta escopo brasileiro ou global
"""

import requests
import urllib.parse
from bs4 import BeautifulSoup
from langchain.tools import tool
import certifi

from src.config.settings import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@tool
def search_football_news(
    query: str,
    scope: str = "br",
    limit: int = 5
) -> str:
    """
    Busca notícias de futebol usando Google News RSS.
    
    Args:
        query: termo livre de busca (ex: Flamengo, Real Madrid, Champions League)
        scope: 
            - "br"     -> futebol brasileiro (pt-BR / BR)
            - "global" -> futebol internacional (en-US / US)
        limit: quantidade máxima de notícias retornadas
    
    Returns:
        String com headlines encontradas
    """
    try:
        # Define escopo
        if scope.lower() == "br":
            final_query = f"{query} futebol"
            hl = "pt-BR"
            gl = "BR"
            ceid = "BR:pt-419"
        elif scope.lower() == "global":
            final_query = f"{query} football"
            hl = "en-US"
            gl = "US"
            ceid = "US:en"
        else:
            return (
                "Escopo inválido. "
                "Use 'br' para futebol brasileiro ou 'global' para futebol internacional."
            )

        # Encode da query
        encoded_query = urllib.parse.quote_plus(final_query)

        # Monta URL RSS
        url = (
            "https://news.google.com/rss/search"
            f"?q={encoded_query}"
            f"&hl={hl}&gl={gl}&ceid={ceid}"
        )

        logger.info(f"Buscando notícias de futebol: query='{final_query}', scope='{scope}'")

        # Request
        response = requests.get(
            url,
            headers={"User-Agent": settings.USER_AGENT},
            timeout=settings.REQUEST_TIMEOUT,
            verify=certifi.where()
        )

        if response.status_code != 200:
            logger.error(f"Erro HTTP {response.status_code} ao acessar Google News RSS")
            return "Erro ao acessar serviço de notícias."

        # Parse RSS
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")[:limit]

        if not items:
            return f"Nenhuma notícia encontrada para '{query}'."

        # Monta saída melhorada
        headlines = []
        for idx, item in enumerate(items, 1):
            title = item.find("title")
            pub_date = item.find("pubDate")
            source_tag = item.find("source")
            
            title_text = title.text if title else "Sem título"
            
            # Formata data de forma mais legível
            date_text = ""
            if pub_date:
                try:
                    from datetime import datetime
                    dt = datetime.strptime(pub_date.text, "%a, %d %b %Y %H:%M:%S %Z")
                    date_text = dt.strftime("%d/%m/%Y às %H:%M")
                except:
                    date_text = pub_date.text
            
            source_text = source_tag.text if source_tag else ""
            
            # Formato mais limpo
            headline = f"{idx}. {title_text}"
            if source_text:
                headline += f" ({source_text})"
            if date_text:
                headline += f"\n   📅 {date_text}"
            
            headlines.append(headline)

        result = f"🔍 Últimas notícias sobre '{query}':\n\n" + "\n\n".join(headlines)
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de rede ao buscar notícias de futebol: {e}")
        return "Erro de rede ao buscar notícias de futebol."
    except Exception as e:
        logger.exception("Erro inesperado ao buscar notícias de futebol")
        return "Erro inesperado ao buscar notícias de futebol."