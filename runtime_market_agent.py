"""
Market Trends Agent - AgentCore Runtime Deployment
Ponto de entrada para deployment na AWS
"""
import sys
import os
import json
import traceback

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Tenta importar de diferentes localizações possíveis
    try:
        from bedrock_agentcore.runtime import BedrockAgentCoreApp
    except ImportError:
        from bedrock_agentcore import BedrockAgentCoreApp
    AGENTCORE_AVAILABLE = True
except ImportError:
    # Fallback para desenvolvimento local
    AGENTCORE_AVAILABLE = False
    BedrockAgentCoreApp = None
    print("Warning: bedrock_agentcore not available (local development mode)")

from src.agent import MarketTrendsAgent
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Inicializa a aplicação AgentCore apenas se disponível
if AGENTCORE_AVAILABLE and BedrockAgentCoreApp:
    app = BedrockAgentCoreApp()
else:
    app = None
    logger.warning("Running without BedrockAgentCoreApp (local mode)")

# Instância global do agente
agent_instance = None


def get_agent() -> MarketTrendsAgent:
    """
    Obtém ou cria a instância do agente (singleton)
    """
    global agent_instance

    if agent_instance is None:
        logger.info("Creating new agent instance...")
        agent_instance = MarketTrendsAgent()

    return agent_instance


if app:
    @app.entrypoint
    def market_trends_agent(payload, context):
        """
        Ponto de entrada principal para o AgentCore Runtime
        """
        try:
            logger.info(f"Received payload: {payload}")

            # Decodifica bytes em dict, se necessário
            if isinstance(payload, (bytes, bytearray)):
                payload = json.loads(payload.decode("utf-8"))

            logger.info(f"Decoded payload: {payload}")

            # Extrai campos do payload
            user_input = payload.get("prompt")
            actor_id = payload.get("actor_id", "default_user")

            if not user_input:
                logger.error("Missing prompt in payload")
                return {"error": "Missing prompt in payload"}

            agent = get_agent()
            logger.info(f"Processing request for actor: {actor_id}")
            response_text = agent.process_request(user_input, actor_id, getattr(context, "session_id", "unknown"))

            return {
                "response": [response_text],
                "actor_id": actor_id,
                "session_id": getattr(context, "session_id", "unknown")
            }

        except Exception as e:
            tb = traceback.format_exc()
            logger.error("Exception occurred while processing request:\n%s", tb)
            return {"error": str(e) or "Unknown error", "trace": tb}


if __name__ == "__main__":
    if app:
        logger.info("Starting Market Trends Agent on AgentCore Runtime")
        app.run()
    else:
        # Modo de teste local
        logger.info("Running in local test mode")
        agent = get_agent()

        # Exemplos de teste
        test_queries = ["What's the current price for NVDA?"]

        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"Query: {query}")
            print(f"{'='*60}")
            response = agent(query)
            print(f"Response: {response}\n")
