"""
Definição do grafo LangGraph – Market Trends Agent
"""

from langgraph.graph import StateGraph, END

from src.state import AgentState
from src.nodes.analyzer import analyze_request
from src.nodes.tools_executor import execute_tools
from src.nodes.genai_respond.generate_response import generate_generic_response, food_flow_generate_response, finance_flow_generate_response, football_flow_generate_response
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


# -------------------------------------------------------------------
# Funções de decisão (roteamento condicional)
# -------------------------------------------------------------------

def should_execute_tools(state: AgentState) -> str:
    return "execute_tools" if state.get("next_step") == "execute_tools" else "end"


def route_event_after_analyze(state: AgentState) -> str:
    """
    Decide o próximo nó com base no evento detectado.
    """
    next_step = state.get("next_step")

    if next_step == "execute_tools":
        return "execute_tools"

    if next_step == "respond":
        return "respond"

    return "end"


def route_respond_after_execute_tool(state: AgentState) -> str:
    """
    Decide o próximo nó com base no evento detectado.
    """
    next_step = state.get("next_step")

    if next_step == "respond_football":
        return "respond_football"

    if next_step == "respond_food":
        return "respond_food"
    
    if next_step == "respond_finance": 
        return "respond_finance"

    return "end"


def create_market_agent_graph() -> StateGraph:
    workflow = StateGraph(AgentState)

    # Nós
    workflow.add_node("analyze", analyze_request)
    workflow.add_node("execute_tools", execute_tools)
    workflow.add_node("respond", generate_generic_response)
    workflow.add_node("respond_food", food_flow_generate_response)
    workflow.add_node("respond_finance", finance_flow_generate_response)
    workflow.add_node("respond_football", football_flow_generate_response)


    # Entrada
    workflow.set_entry_point("analyze")

    # analyze → execute_tools ou END
    workflow.add_conditional_edges(
        "analyze",
        route_event_after_analyze,
        {
            "execute_tools": "execute_tools",
            "respond": "respond",
            "end": END
        }
    )

    # execute_tools → respond
    workflow.add_conditional_edges(
        "execute_tools",
        route_respond_after_execute_tool,
        {
            "respond_food": "respond_food",
            "respond_football": "respond_football",
            "respond_finance": "respond_finance"
        }
    )
    # respond → END
    workflow.add_edge("respond", END)

    return workflow



# -------------------------------------------------------------------
# Compile
# -------------------------------------------------------------------

def compile_graph():
    """
    Compila o grafo para uso em runtime.

    Returns:
        Grafo LangGraph compilado
    """
    return create_market_agent_graph().compile()
