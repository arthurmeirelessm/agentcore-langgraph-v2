"""
Definição do grafo LangGraph
"""
from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.nodes.analyzer import analyze_request
from src.nodes.tools_executor import execute_tools
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def create_market_agent_graph() -> StateGraph:
    """
    Cria o grafo do Market Trends Agent
    
    Returns:
        StateGraph configurado
    """
    logger.info("Creating market agent graph...")
    
    # Cria grafo
    workflow = StateGraph(AgentState)
    
    # Adiciona nós
    workflow.add_node("analyze", analyze_request)
    workflow.add_node("execute_tools", execute_tools)
    
    # Define ponto de entrada
    workflow.set_entry_point("analyze")
    
    # Define transições condicionais
    def should_execute_tools(state: AgentState) -> str:
        """Decide se deve executar ferramentas ou finalizar"""
        next_step = state.get("next_step", "end")
        if next_step == "execute_tools":
            return "execute_tools"
        return "end"
    
    # Adiciona edges
    workflow.add_conditional_edges(
        "analyze",
        should_execute_tools,
        {
            "execute_tools": "execute_tools",
            "end": END
        }
    )
    
    workflow.add_edge("execute_tools", END)
    
    logger.info("Graph created successfully")
    return workflow


def compile_graph():
    """
    Compila o grafo para uso
    
    Returns:
        Grafo compilado
    """
    workflow = create_market_agent_graph()
    return workflow.compile()