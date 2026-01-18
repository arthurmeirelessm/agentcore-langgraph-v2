"""
Classe principal do Market Trends Agent usando LangGraph
"""
from typing import Dict, Any
from src.graph import compile_graph
from src.state import AgentState
from src.utils.logger import setup_logger
from src.repository.memory.agent_memory import AgentMemory
from src.utils.episode_memory import infer_outcome
from src.repository.dynamodb.dynamodb_service import DynamoDbService
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
        self.agent_memory = AgentMemory()
        self.dynamodb_service = DynamoDbService()

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
        actor_id: str,
        session_id: str
    ) -> str:
        """
        Processa uma requisição do usuário
        """
        if self.graph is None:
            logger.error("Graph not initialized")
            return "Error: Agent not initialized"

        try:
            logger.info(f"Processing request from {actor_id}: {user_input[:100]}...")
            
            
            last_episode = self.dynamodb_service.load_last_episode(actor_id, session_id)

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
                "topic": None,
                "goal": None,
                "error": None,
                "signals": None,
                "last_episode": last_episode
            }

            # Executa o grafo
            result = self.graph.invoke(initial_state)
            
            outcome = infer_outcome(result)
            result["outcome"] = outcome
            
            # Detectar continuidade de tópico
            if last_episode and last_episode.get("topic"):
                previous_topic = last_episode["topic"]
                current_topic = result.get("topic")

                # lógica simples de similaridade
                if previous_topic and current_topic:
                    if previous_topic.lower() == current_topic.lower():
                        # garante que signals seja um dict
                        if result.get("signals") is None:
                            result["signals"] = {}
                        
                        result["signals"]["same_topic"] = True
                        
            self.dynamodb_service.save_episode_in_dynamo(
                actor_id=actor_id,
                session_id=session_id,
                goal=result.get("goal"),
                outcome=outcome,
                topic=result.get("topic"),
                signals=result.get("signals")
            )

            # 4️⃣ opcional: salva no AgentMemory (snapshot semântico)
            self.agent_memory.save_episode_in_agentcore_memory(result)
            
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
        actor_id: str ,
        session_id: str
    ) -> str:
        """
        Permite chamar a instância diretamente
        """
        return self.process_request(user_input, actor_id, session_id)
