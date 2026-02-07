"""
Estado do agente LangGraph
"""
from typing import TypedDict, List, Optional, Annotated, Dict, Any
from operator import add


class AgentState(TypedDict, total=False):
    """
    Estado compartilhado entre os nós do grafo
    """

    messages: Annotated[List[dict], add]

    actor_id: str
    session_id: str

    domain: Optional[str]             
    conversation_mode: Optional[str]   

    goal: Optional[str]
    topic: Optional[str]
    
    symbol: Optional[str]

    food_flow_stage: Optional[str]     
    selected_restaurant: Optional[str]
    cart: Optional[List[Dict[str, Any]]]  

    next_step: Optional[str]          
    last_action: Optional[str]
    
    user_input: Optional[str]     

    response_payload: Optional[Any]   
    final_response: Optional[str]     

    error: Optional[str]
