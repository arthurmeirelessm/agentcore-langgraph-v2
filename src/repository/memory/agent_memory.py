"""
Infraestrutura unificada de AgentCore Memory
Responsável por:
- recuperar memória (load)
- persistir eventos (save)
"""
import boto3
from src.config.settings import settings
from src.utils.logger import setup_logger
import uuid
from datetime import datetime

logger = setup_logger(__name__)


class AgentMemory:
    """
    Camada de infraestrutura para AgentCore Memory.
    NÃO é tool.
    NÃO depende do LLM.
    """

    def __init__(self):
        self.enabled = bool(settings.MEMORY_ID)

        if not self.enabled:
            logger.warning("🧠 AgentMemory disabled (MEMORY_ID not set)")
            return

        self.client = boto3.client(
        "bedrock-agentcore",
        region_name=settings.AWS_REGION
        )

        logger.info("🧠 AgentMemory initialized")



    # ---------- LOAD ----------
    def load(self, actor_id: str, session_id: str, max_results: int, search_query: str) -> str:
        if not self.enabled:
            return ""

        actor_id = self._normalize_actor_id(actor_id)
        
        namespace = self._build_namespace(
            settings.MEMORY_STRATEGY_ID,
            actor_id,
            session_id
            )

        try:
            response = self.client.retrieve_memory_records(
            memoryId=settings.MEMORY_ID,
            namespace=namespace,
            searchCriteria={
                "searchQuery": search_query,  # pode ser vazio se quiser todos os registros
                "memoryStrategyId": settings.MEMORY_STRATEGY_ID,
                "topK": max_results,
            },
        )

            summaries = response.get("memoryRecordSummaries", [])

            texts = []
            
            for summary in summaries:
                content = summary.get("content", {})
                text = content.get("text")
                if text:
                    texts.append(text)

            return "\n".join(texts)

        except Exception:
            logger.exception("Failed to load AgentCore memory")
            return ""

    # ---------- SAVE ----------
    def save_summary_interaction(self, state) -> None:
        """
        Persiste informações relevantes do estado no AgentCore Memory.
        """
        if not self.enabled:
            return

        if not self._should_persist(state):
            return

        actor_id = self._normalize_actor_id(state["actor_id"])
        session_id = self._build_session_id(state)
        messages = self._build_messages(state)
        event_timestamp = datetime.utcnow()

        if not messages:
            return

        try:
            self.client.create_event(
                memoryId=settings.MEMORY_ID,
                actorId=actor_id,
                sessionId=session_id,
                eventTimestamp=event_timestamp,
                payload=messages
            )
            print("saved")
            logger.info("AgentCore memory saved")
            

        except Exception:
            logger.exception("Failed to save AgentCore memory")
            
    
    
    def save_episode(self, state) -> None:
        if not self.enabled:
            return

        actor_id = self._normalize_actor_id(state["actor_id"])
        session_id = self._build_session_id(state)

        episode_payload = {
            "episode": {
                "goal": state.get("intent", "unknown"),
                "actions": state.get("tools_to_execute", ["direct_answer"]),
                "outcome": (
                    "follow_up"
                    if state.get("follow_up")
                    else "completed"
                ),
                "signals": {
                    "success": not state.get("error", False),
                    "topic": state.get("topic")
                }
            }
        }
        
        try: 
            self.client.create_event(
                memoryId=settings.MEMORY_ID,
                actorId=actor_id,
                sessionId=session_id,
                payload=episode_payload
            )
        except Exception:
            logger.exception("Failed to save AgentCore memory")

            

    # ---------- helpers ----------
    def _should_persist(self, state) -> bool:
        if state.get("error"):
            return False

        if not state.get("final_response"):
            return False

        messages = state.get("messages", [])
        if not messages:
            return False

        return True


    def _build_session_id(self, state) -> str:
        return state.get("session_id") or str(uuid.uuid4())

    def _build_messages(self, state) -> list[dict]:
        """
        Converte o estado em eventos de memória.
        """
        messages = state.get("messages", [])
        
        print("Messages", messages)
    
        user_input = None
        for msg in reversed(messages):
            role = getattr(msg, "role", None) if not isinstance(msg, dict) else msg.get("role")
            if role == "user":
                user_input = getattr(msg, "content", None) if not isinstance(msg, dict) else msg.get("content")
                break
                
        assistant_output = state.get("final_response")

        if not user_input or not assistant_output:
            return []

        return [
            {
                "conversational": {
                    "role": "USER",
                    "content": {"text": user_input}
                }
            },
            {
                "conversational": {
                    "role": "ASSISTANT",
                    "content": {"text": assistant_output}
                }
            }
        ]



    def _normalize_actor_id(self, actor_id: str) -> str:
        return actor_id.lower().replace(" ", "-")
    
    def _build_namespace(
        self,
        memory_strategy_id: str,
        actor_id: str,
        session_id: str,
    ) -> str:
        actor_id = actor_id.lower().replace(" ", "-")
        session_id = session_id.lower().replace(" ", "-")

        return (
            f"/strategies/{memory_strategy_id}"
            f"/actors/{actor_id}"
            f"/sessions/{session_id}"
        )

    
    # ---------- INJECT ----------
    def inject_into_state(self, state, max_results=5) -> None:
        """
        Injeta memória no state do LangGraph como system message
        """
        actor_id = state.get("actor_id")
        session_id = state.get("session_id")

        if not actor_id:
            return

        memory_text = self.load(actor_id, session_id, max_results)

        if not memory_text:
            return

        state["messages"].insert(
            0,
            {
                "role": "system",
                "content": f"User memory context:\n{memory_text}"
            }
        )
