"""
Estado do agente LangGraph
"""
from typing import TypedDict, List, Optional, Annotated
from operator import add


class AgentState(TypedDict):
    """
    Estado compartilhado entre os nós do grafo
    """
    # Mensagens do usuário e assistente
    messages: Annotated[List[dict], add]
    
    # Informações do usuário
    actor_id: str
    session_id: str
    
    # Contexto da conversa
    user_profile: Optional[dict]
    conversation_history: Annotated[List[dict], add]
    
    # Ferramentas e análise
    tools_to_execute: List[str]
    tools_results: dict
    
    # Resposta final
    final_response: Optional[str]
    
    # Controle de fluxo
    next_step: str
    error: Optional[str]
    
    goal: Optional[str]
    topic: Optional[str]
    
    last_episode: Optional[dict]
    signals: Optional[dict]
    outcome: Optional[str]