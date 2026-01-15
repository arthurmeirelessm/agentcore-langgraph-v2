from src.repository.memory.agent_memory import AgentMemory
from src.state import AgentState

class MemoryLoader:
    def __init__(self):
        self.memory = AgentMemory()

    def __call__(self, state: AgentState) -> dict:
        actor_id = state.get("actor_id")
        session_id = state.get("session_id")
        messages = state.get("messages", [])
        

        if not actor_id:
            return {}


        user_messages = [m for m in messages if m.get("role") == "user"]
        
        if user_messages:
            user_input = user_messages[-1].get("content", "")
        else:
            user_input = ""

        # Busca na memória usando o input do usuário como searchQuery
        memory_text = self.memory.load(actor_id, session_id, max_results=5, search_query=user_input)
        
        if not memory_text:
            return {}  # 🔑 NÃO retorna messages vazias

        return {
            "messages": [
                {
                    "role": "system",
                    "content": f"User memory context:\n{memory_text}"
                }
            ]
        }
