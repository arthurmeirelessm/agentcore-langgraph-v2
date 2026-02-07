import json
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate

from src.config.settings import settings
from src.state import AgentState
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def analyze_request(state: AgentState) -> dict:
    """
    Analisa a mensagem do usuário como EVENTO conversacional
    e decide a transição de estado.
    """
    try:
        logger.info("Analyzing conversational event...")

        messages = state.get("messages", [])
        user_messages = [m for m in messages if m.get("role") == "user"]

        if not user_messages:
            return {"next_step": "end"}

        user_input = user_messages[-1]["content"]
        current_domain = state.get("domain")
        current_stage = state.get("food_flow_stage")

        llm = ChatBedrock(
            model_id=settings.MODEL_ID,
            region_name=settings.AWS_REGION,
            model_kwargs={"temperature": 0, "max_tokens": 300},
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", settings.SYSTEM_PROMPT),
            ("system", """
                Você é um classificador de INTENÇÃO e EVENTO DE CONVERSA.

                Classifique a mensagem do usuário:

                INTENT (domínio principal):
                FOOD | FINANCE | FOOTBALL | GENERAL

                EVENT (tipo de evento):
                NEW_TASK → iniciar algo novo
                PROVIDE_INFO → respondeu algo pedido
                CHANGE_STEP → quer voltar etapa/menu
                CANCEL → cancelar fluxo atual
                CORRECTION → corrigir escolha
                HELP → não sabe o que fazer
                SMALLTALK → conversa casual
                CONFIRM → confirmar ação
                OTHER → nenhum dos acima
                
                EXTRAIA também entidades quando existirem:

                Para FINANCE:
                - symbol → ticker da ação (ex: AAPL, NVDA, TSLA)

                Responda SOMENTE JSON:

                {{
                "intent": "...",
                "event": "...",
                "goal": "objetivo do usuário",
                "symbol: "..."
                """),
            ("human", "{input}")
        ])

        chain = prompt | llm
        response = chain.invoke({"input": user_input})
        content = response.content

        try:
            json_str = content[content.find("{"): content.rfind("}") + 1]
            analysis = json.loads(json_str)
        except Exception:
            return {"next_step": "end"}

        intent = analysis.get("intent")
        event = analysis.get("event")
        goal = analysis.get("goal")
        symbol = analysis.get("symbol")


        if event == "CANCEL":
            return {
                "domain": "general",
                "food_flow_stage": None,
                "response_payload": { "data": "Fluxo cancelado." },
                "next_step": "respond"
            }


        if event == "CHANGE_STEP" and current_domain == "food":
            return {
                "food_flow_stage": "start",
                "next_step": "execute_tools"
            }


        if event == "SMALLTALK":
            return {
                "response_payload": "😄",
                "next_step": "respond"
            }

 
        if intent == "FOOD":

            if current_stage is None or event == "NEW_TASK":
                return {
                    "domain": "food",
                    "food_flow_stage": "start",
                    "goal": goal,
                    "next_step": "execute_tools"
                }

            if current_stage == "start" and event in ["PROVIDE_INFO", "CORRECTION"]:
                return {
                    "food_flow_stage": "select",
                    "next_step": "execute_tools"
                }

            if event == "CONFIRM":
                return {
                    "food_flow_stage": "confirm",
                    "next_step": "execute_tools"
                }


        if intent in ["FINANCE", "FOOTBALL"]:
            return {
                "domain": intent.lower(),
                "goal": goal,
                "next_step": "execute_tools",
                "symbol": symbol,
                "user_input": user_input
            }


        if event == "HELP":
            return {
                "response_payload": "Você pode pedir comida, ver notícias financeiras ou falar sobre futebol.",
                "next_step": "respond"
            }

        return {
            "response_payload": "Posso te ajudar com algo específico?",
            "next_step": "respond"
        }

    except Exception:
        logger.exception("Analyzer failure")
        return {"next_step": "end"}
