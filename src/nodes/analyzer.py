import json
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate

from src.config.settings import settings
from src.state import AgentState
from src.utils.logger import setup_logger

logger = setup_logger(__name__)



def analyze_request(state: AgentState) -> dict:
    """
    Analisa a requisição do usuário e decide próximos passos.
    Retorna APENAS o delta do estado (patch).
    """
    try:
        logger.info("Analyzing user request...")

        messages = state.get("messages", [])
        user_messages = [m for m in messages if m.get("role") == "user"]

        if not user_messages:
            return {
                "error": "No user messages to process",
                "next_step": "end",
            }

        # Pega a última mensagem do usuário
        last_user_message = user_messages[-1]
        user_input = last_user_message.get("content", "")

        llm = ChatBedrock(
            model_id=settings.MODEL_ID,
            region_name=settings.AWS_REGION,
            model_kwargs={
                "temperature": settings.MODEL_TEMPERATURE,
                "max_tokens": settings.MODEL_MAX_TOKENS,
            },
        )
        
        
        analysis_prompt = ChatPromptTemplate.from_messages([
                    ("system", settings.SYSTEM_PROMPT),
                    ("system", """Considerando a mensagem do usuário, determine quais ferramentas (se houver) devem ser chamadas.

        Ferramentas disponíveis:
        - get_stock_data: Obter dados de preços de ações em tempo real para um determinado símbolo
        - search_news: Pesquisar notícias financeiras
        - search_football_news: Pesquisar notícias do futebol mundial
        - get_user_for_request_food_action: Ação que envolve pegar informações do user para prosseguir com pedido de comida
        - get_restaurants: Pega localização que veio do resultado da tool get_user_for_request_food_action() e busca restaurantes perto dessal ocalização
        - request_order: Faz pedido de itens ao restaurante escolhido
 
        Responda com um objeto JSON contendo:
        {{
            "tools_needed": ["tool1", "tool2"],
            "tool_params": {{"tool1": {{"param": "value"}}}},
            "reasoning": "Por que essas ferramentas são necessárias?",
            "goal" "Intenção real do input do usuário",
            "topic": "Tópico raiz da intenção. Exemplo: Futebol, Finanças"
            "needs_tools": true/false
        }}

        Caso não sejam necessárias ferramentas, defina needs_tools como false e forneça uma resposta direta."""),
                    ("human", "{input}")
                ])

        chain = analysis_prompt | llm
        response = chain.invoke({"input": user_input})
        content = response.content

        # Parse defensivo
        try:
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            else:
                json_str = content[content.find("{"): content.rfind("}") + 1]
            analysis = json.loads(json_str)
        except Exception:
            analysis = {
                "needs_tools": False,
                "direct_response": content,
            }

        if analysis.get("needs_tools"):
            return {
                "tools_to_execute": analysis.get("tools_needed", []),
                "next_step": "execute_tools",
                "goal": analysis.get("goal"),
                "topic": analysis.get("topic"),
                "error": False
            }

        return {
            "final_response": analysis.get("direct_response", content),
            "next_step": "end",
            "goal": analysis.get("goal"),
            "topic": analysis.get("topic"),
            "error": False
        }

    except Exception as e:
        logger.exception("Error in analyze_request")
        return {
            "next_step": "end",
            "goal": analysis.get("goal"),
            "topic": analysis.get("topic"),
            "error": True
        }
