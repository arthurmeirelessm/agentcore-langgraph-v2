from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.config.settings import settings
from src.state import AgentState
from src.tools.news_tools import search_news
from src.tools.stock_tools import get_stock_data
from src.tools.news_football import search_football_news
from src.tools.request_food import get_user, location, simulate_order_price
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

TOOLS = {
    "get_stock_data": get_stock_data,
    "search_news": search_news,
    "search_football_news": search_football_news
}


def execute_tools(state: AgentState) -> dict:
    try:
        logger.info("Executing tools with deterministic workflow...")

        stage = state.get("food_flow_stage")
        domain = state.get("domain")
        symbol = state.get("symbol", "")

        if domain == "food":
            if stage == "start":
                user_data = get_user.invoke({"user_id": state["actor_id"]})

                city = user_data.get("city")
                neighborhood = user_data.get("neighborhood")

                if not city or not neighborhood:
                    return {
                        "response_payload": {
                            "data": "Não consegui identificar sua localização."
                        },
                        "next_step": "respond_food"
                    }

                restaurants_data = location.invoke({
                    "city": city,
                    "neighborhood": neighborhood
                })

                if not restaurants_data:
                    return {
                        "response_payload": {
                            "data": "Não consegui identificar sua localização."
                        },
                        "next_step": "respond_food"
                    }

                city = restaurants_data.get("city")
                neighborhood = restaurants_data.get("neighborhood")
                total = restaurants_data.get("total_restaurants", 0)
                restaurants = restaurants_data.get("restaurants", [])

                if total == 0:
                    return {
                        "response_payload": {
                            "data": f"Não encontrei restaurantes em {neighborhood}, {city}."
                        },
                        "next_step": "respond_food"
                    }

                header = f"Encontrei **{total} restaurantes** em {neighborhood}, {city}:\n\n"
                restaurant_blocks = []

                for i, r in enumerate(restaurants, start=1):
                    name = r.get("name")
                    category = r.get("category")
                    rating = r.get("rating")
                    price_level = r.get("price_level")

                    block = (
                        f"{i}. **{name}**\n"
                        f"Categoria: {category}\n"
                        f"Avaliação: ⭐ {rating} | Faixa de preço: {price_level}\n"
                    )

                    menu = r.get("menu", [])
                    if menu:
                        block += f"Menu do {name}:\n"
                        for item in menu:
                            item_name = item.get("name")
                            item_price = item.get("price")
                            block += f"   • {item_name} — R${item_price}\n"
                    else:
                        block += "Menu não disponível.\n"

                    restaurant_blocks.append(block)

                formatted_response = header + "\n".join(restaurant_blocks)

                return {
                    "response_payload": {
                        "data": formatted_response
                    },
                    "last_action": "fetched_restaurants",
                    "next_step": "respond_food"
                }

            if stage == "select":
                order_data = simulate_order_price.invoke({})

                return {
                    "response_payload": {
                        "data": order_data
                    },
                    "last_action": "calculated_order",
                    "next_step": "respond_food"
                }

        if domain == "finance":
            stock_data = get_stock_data.invoke(symbol)
            return {
                "response_payload": {"data": stock_data},
                "last_action": "stock_lookup",
                "next_step": "respond_finance"
            }

        if domain == "football":
            news = search_football_news.invoke({"query": state["goal"]})
            return {
                "response_payload": {"data": news},
                "last_action": "football_news",
                "next_step": "respond_football"
            }

        return {
            "response_payload": {"data": state.get("goal")},
            "next_step": "respond"
        }

    except Exception as e:
        logger.exception("Tool execution error")
        return {
            "error": str(e),
            "next_step": "respond"
        }
