"""
Classe principal do Market Trends Agent usando LangGraph
"""
from typing import Dict, Any
from src.graph import compile_graph
from src.state import AgentState
from src.utils.logger import setup_logger
import traceback

logger = setup_logger(__name__)


class MarketTrendsAgent:
    """
    Agente de análise de tendências de mercado com memória persistente
    usando LangGraph para orquestração
    """

    def __init__(self):
        """Inicializa o agente"""
        self.graph = None
        self._initialize_agent()

    def _initialize_agent(self):
        """Configura e inicializa o grafo do agente"""
        try:
            logger.info("Initializing Market Trends Agent with LangGraph...")

            # Compila o grafo
            self.graph = compile_graph()

            logger.info("✅ Market Trends Agent initialized successfully")

        except Exception as e:
            tb = traceback.format_exc()
            logger.error("Error initializing agent:\n%s", tb)
            raise

    def process_request(
        self,
        user_input: str,
        actor_id: str = "default_user",
        session_id: str = "default_session"
    ) -> str:
        """
        Processa uma requisição do usuário
        """
        if self.graph is None:
            logger.error("Graph not initialized")
            return "Error: Agent not initialized"

        try:
            logger.info(f"Processing request from {actor_id}: {user_input[:100]}...")

            # Cria estado inicial
            initial_state: AgentState = {
                "messages": [{"role": "user", "content": user_input}],
                "actor_id": actor_id,
                "session_id": session_id,
                "user_profile": None,
                "conversation_history": [],
                "tools_to_execute": [],
                "tools_results": {},
                "final_response": None,
                "next_step": "analyze",
                "error": None
            }

            # Executa o grafo
            result = self.graph.invoke(initial_state)

            # Extrai resposta final
            response_text = result.get("final_response")

            if not response_text:
                response_text = "I apologize, but I couldn't generate a response. Please try again."

            if result.get("error"):
                logger.error(f"Error in graph execution: {result['error']}")

            logger.info(f"✅ Generated response: {response_text[:100]}...")
            return response_text

        except Exception as e:
            tb = traceback.format_exc()
            logger.error("Error processing request:\n%s", tb)
            return "I apologize, but I encountered an error processing your request. Please try again."

    def __call__(
        self,
        user_input: str,
        actor_id: str = "default_user",
        session_id: str = "default_session"
    ) -> str:
        """
        Permite chamar a instância diretamente
        """
        return self.process_request(user_input, actor_id, session_id)
