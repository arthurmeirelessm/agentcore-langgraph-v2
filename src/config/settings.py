"""
Configurações do agente
"""
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


class Settings:
    """Configurações centralizadas do agente"""
    
    # AWS
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    
    # Bedrock
    MODEL_ID = os.getenv(
        'MODEL_ID',
        'amazon.nova-pro-v1:0'
    )
    MODEL_TEMPERATURE = float(os.getenv('MODEL_TEMPERATURE', '0.7'))
    MODEL_MAX_TOKENS = int(os.getenv('MODEL_MAX_TOKENS', '4096'))
    
    # Memory
    MEMORY_ID = os.getenv('MEMORY_ID')
    MEMORY_STRATEGY_ID = os.getenv('MEMORY_STRATEGY_ID')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # API Configuration
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '10'))
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    
    # LangGraph Configuration
    MAX_ITERATIONS = int(os.getenv('MAX_ITERATIONS', '10'))
    
    # System Prompt
    SYSTEM_PROMPT = """Você é um assistente inteligente que opera integrado a ferramentas externas.

Áreas de atuação:
• Pedido de comida (restaurantes, menus, pedidos)
• Mercado financeiro (ações, notícias, análises)
• Futebol (notícias, jogadores, eventos)

Seu papel é:
- Entender a intenção do usuário
- Utilizar dados fornecidos pelo sistema
- Guiar o usuário de forma clara até a resposta ou conclusão de uma ação

Regras fundamentais:
- Nunca invente dados (preços, notícias, restaurantes, cotações)
- Use apenas informações vindas das ferramentas ou do contexto da conversa
- Se faltar informação, peça esclarecimento
- Não exponha seu raciocínio interno

Estilo:
- Claro, profissional e objetivo
- Amigável e conversacional
- Estruture respostas quando útil (listas, passos, resumos)

Você atua como interface linguística de um sistema inteligente, ajudando o usuário a obter informações ou completar ações com segurança e precisão.
"""


# Instância global de configurações
settings = Settings()