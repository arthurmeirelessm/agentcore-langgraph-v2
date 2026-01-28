"""
Definição do grafo LangGraph – Market Trends Agent
"""

from langgraph.graph import StateGraph, END

from src.state import AgentState
from src.nodes.analyzer import analyze_request
from src.nodes.tools_executor import execute_tools
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# -------------------------------------------------------------------
# Constantes de estados do grafo
# -------------------------------------------------------------------

ANALYZE = "analyze"
EXECUTE_TOOLS = "execute_tools"
END_STATE = "end"


# -------------------------------------------------------------------
# Funções de decisão (roteamento condicional)
# -------------------------------------------------------------------

def should_execute_tools(state: AgentState) -> str:
    """
    Decide se o fluxo deve executar ferramentas ou finalizar.

    Retorna:
        - EXECUTE_TOOLS: quando ferramentas devem ser executadas
        - END_STATE: quando o fluxo deve encerrar
    """
    return EXECUTE_TOOLS if state.get("next_step") == EXECUTE_TOOLS else END_STATE


# -------------------------------------------------------------------
# Builder do grafo
# -------------------------------------------------------------------

def create_market_agent_graph() -> StateGraph:
    """
    Cria e configura o grafo do Market Trends Agent.

    Fluxo:
        analyze -> (condicional) -> execute_tools -> END
                          └────> END

    Returns:
        StateGraph configurado
    """
    logger.info("Creating market agent graph...")

    workflow = StateGraph(AgentState)

    # ---------------------------
    # Nós
    # ---------------------------
    workflow.add_node(ANALYZE, analyze_request)
    workflow.add_node(EXECUTE_TOOLS, execute_tools)

    # ---------------------------
    # Ponto de entrada
    # ---------------------------
    workflow.set_entry_point(ANALYZE)

    # ---------------------------
    # Transições
    # ---------------------------
    workflow.add_conditional_edges(
        ANALYZE,
        should_execute_tools,
        {
            EXECUTE_TOOLS: EXECUTE_TOOLS,
            END_STATE: END
        }
    )
    
    # Conecta dois nós sequencias se necessário
    # EX: workflow.add_edge("step_1", "step_2")
    #     workflow.add_edge("step_2", "step_3")
    workflow.add_edge(EXECUTE_TOOLS, END)

    logger.info("Graph created successfully")
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
