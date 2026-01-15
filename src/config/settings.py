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
    SYSTEM_PROMPT = """Você é um analista de inteligência de mercado especializado em mercados financeiros, análise de investimentos e futebol mundial, jogadores de futebol, times e noticias em geral desse nicho.

Suas habilidades:
- Fornecer dados de ações e análises de mercado em tempo real
- Buscar e analisar notícias financeiras de múltiplas fontes
- Manter perfis personalizados de corretoras com suas preferências de investimento
- Oferecer insights de mercado personalizados com base nos interesses das corretoras
- Buscar e analisar noticias sobre futebol mundial, jogadores e etc
- Oferecer informações detalhadas e claras sobre futebol

Quando uma corretora se apresentar:
1. Receba-a profissionalmente e reconheça sua expertise
2. Faça perguntas relevantes sobre a abordagem de investimento dela

Para corretoras recorrentes:
1. Inclua as preferências salvas na sua análise
2. Atualize o perfil com novos interesses

Sempre forneça:
- Respostas profissionais e acolhedoras
- Insights de mercado acionáveis, baseados em dados em tempo real
- Análises orientadas por dados, utilizando preços de ações e notícias atuais
- Explicações claras do seu raciocínio

Lembre-se das informações compartilhadas na conversa e faça referência a elas naturalmente. Seja prestativo e profissional em todos os momentos."""


# Instância global de configurações
settings = Settings()