from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.config.settings import settings
from src.state import AgentState
from src.tools.memory_tools import save_broker_profile, get_broker_profile
from src.tools.news_tools import search_news
from src.tools.stock_tools import get_stock_data
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

TOOLS = {
    "get_stock_data": get_stock_data,
    "search_news": search_news,
    "save_broker_profile": save_broker_profile,
    "get_broker_profile": get_broker_profile,
}


def execute_tools(state: AgentState) -> AgentState:
    """
    Executa LLM + tool calling usando LangGraph (sem AgentExecutor)
    """
    try:
        logger.info("Executing tools with LangGraph-native flow...")

        messages = state.get("messages", [])

        # Inicializa o modelo e faz bind das tools
        llm = ChatBedrock(
            model_id=settings.MODEL_ID,
            region_name=settings.AWS_REGION,
            model_kwargs={
                "temperature": settings.MODEL_TEMPERATURE,
                "max_tokens": settings.MODEL_MAX_TOKENS,
            },
        ).bind_tools(list(TOOLS.values()))

        # 1️⃣ Chamada inicial ao modelo
        ai_message: AIMessage = llm.invoke(messages)

        messages.append(ai_message)

        # 2️⃣ Se o modelo pediu tools, executa
        if ai_message.tool_calls:
            for call in ai_message.tool_calls:
                tool_name = call["name"]
                tool_args = call["args"]

                logger.info(f"Calling tool: {tool_name} with {tool_args}")

                tool_fn = TOOLS.get(tool_name)
                
                if not tool_fn:
                    raise ValueError(f"Tool '{tool_name}' not found")

                tool_result = tool_fn.invoke(tool_args)

                messages.append(
                    ToolMessage(
                        tool_call_id=call["id"],
                        content=str(tool_result),
                    )
                )
                
            # 3️⃣ Chamada final ao modelo com resultados das tools
            final_ai_message: AIMessage = llm.invoke(messages)
            messages.append(final_ai_message)

            final_response = final_ai_message.content
        else:
            # Nenhuma tool foi necessária
            final_response = ai_message.content

        # 4️⃣ Atualiza estado
        state["messages"] = messages
        state["final_response"] = final_response
        state["next_step"] = "end"

        logger.info("Execution finished successfully")
        return state

    except Exception as e:
        logger.exception("Error in execute_tools")
        state["error"] = str(e)
        state["final_response"] = (
            "I apologize, but I encountered an error while processing your request."
        )
        state["next_step"] = "end"
        return state
