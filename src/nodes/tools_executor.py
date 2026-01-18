from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.config.settings import settings
from src.state import AgentState
from src.tools.news_tools import search_news
from src.tools.stock_tools import get_stock_data
from src.tools.news_football import search_football_news
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

TOOLS = {
    "get_stock_data": get_stock_data,
    "search_news": search_news,
    "search_football_news": search_football_news
}


def execute_tools(state: AgentState) -> dict:
    """
    Executa tools via Bedrock tool calling.
    Retorna APENAS o delta do estado, evitando duplicar mensagens do usuário.
    """
    try:
        logger.info("Executing tools with LangGraph-native flow...")
        

        messages = state.get("messages", [])

        llm = ChatBedrock(
            model_id=settings.MODEL_ID,
            region_name=settings.AWS_REGION,
            model_kwargs={
                "temperature": settings.MODEL_TEMPERATURE,
                "max_tokens": settings.MODEL_MAX_TOKENS,
            },
        ).bind_tools(list(TOOLS.values()))

        # ⚠️ cria nova lista, NÃO muta state["messages"]
        new_messages = list(messages)

        # Primeira chamada do LLM
        ai_message: AIMessage = llm.invoke(new_messages)
        new_messages.append(ai_message)

        # Lista para acumular apenas mensagens novas (delta)
        delta_messages = [ai_message]

        # Se houver tool calls
        if ai_message.tool_calls:
            for call in ai_message.tool_calls:
                tool_name = call["name"]
                tool_args = call["args"]

                logger.info(f"Calling tool: {tool_name} {tool_args}")

                tool_fn = TOOLS.get(tool_name)
                if not tool_fn:
                    raise ValueError(f"Tool '{tool_name}' not found")

                tool_result = tool_fn.invoke(tool_args)

                tool_message = ToolMessage(
                    tool_call_id=call["id"],
                    content=str(tool_result),
                )

                new_messages.append(tool_message)
                delta_messages.append(tool_message)

            # Segunda chamada com resultado das tools
            final_ai_message: AIMessage = llm.invoke(new_messages)
            new_messages.append(final_ai_message)
            delta_messages.append(final_ai_message)

            final_response = final_ai_message.content
        else:
            final_response = ai_message.content

        return {
            "messages": delta_messages,  
            "final_response": final_response,
            "next_step": "end",
        }

    except Exception as e:
        logger.exception("Error in execute_tools")
        return {
            "error": str(e),
            "final_response": "I encountered an error while processing your request.",
            "next_step": "end",
        }
