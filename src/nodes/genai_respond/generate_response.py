import json
from langchain_aws import ChatBedrock
from langchain_core.messages import AIMessage, HumanMessage
from src.repository.semantic_cache.redis import save_to_semantic_cache
from src.config.settings import settings
from src.state import AgentState
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def generate_generic_response(state: AgentState) -> dict:
    logger.info("Generating final response (universal renderer)...")

    payload = state.get("response_payload")
    data = payload.get("data")

    if payload is None:
        return {"messages": [AIMessage(content="Erro interno: resposta vazia.")]}

    # -------------------------
    # 📜 Já é texto pronto
    # -------------------------
    if isinstance(payload, str):
        return {"messages": [AIMessage(content=payload)]}

    # -------------------------
    # 🤖 Dado estruturado → LLM formata
    # -------------------------
    llm = ChatBedrock(
        model_id=settings.MODEL_ID,
        region_name=settings.AWS_REGION,
        model_kwargs={
            "temperature": 0.3,
            "max_tokens": 500,
        },
    )

    prompt = f"""
        Você é um assistente inteligente.

        Transforme os dados estruturados abaixo em uma resposta clara, natural e útil para o usuário.

        Dados:
        {data}

        Regras:
        - Não mencione JSON
        - Seja direto e amigável
        - Se for lista, organize visualmente
        - Se envolver valores monetários, destaque totais
        - Se envolver restaurantes, ajude o usuário a decidir o próximo passo
        """

    response = llm.invoke([HumanMessage(content=prompt)])

    final_text = response.content

    return {
            "messages": [AIMessage(content=final_text)],
            "final_response": final_text
        }



def finance_flow_generate_response(state: AgentState) -> dict:
    logger.info("Generating final response (universal renderer)...")

    payload = state.get("response_payload")
    data = payload.get("data")
    user_input = state.get("user_input")

    if payload is None:
        return {"messages": [AIMessage(content="Erro interno: resposta vazia.")]}

    # -------------------------
    # 📜 Já é texto pronto
    # -------------------------
    if isinstance(payload, str):
        return {"messages": [AIMessage(content=payload)]}

    # -------------------------
    # 🤖 Dado estruturado → LLM formata
    # -------------------------
    llm = ChatBedrock(
        model_id=settings.MODEL_ID,
        region_name=settings.AWS_REGION,
        model_kwargs={
            "temperature": 0.3,
            "max_tokens": 500,
        },
    )

    prompt = f"""
        Você é um assistente inteligente.

        Transforme os dados estruturados abaixo em uma resposta clara, natural e útil para o usuário.

        Dados:
        {data}

        Regras:
        - Não mencione JSON
        - Seja direto e amigável
        - Se for lista, organize visualmente
        - Se envolver valores monetários, destaque totais
        - Se envolver restaurantes, ajude o usuário a decidir o próximo passo
        """

    response = llm.invoke([HumanMessage(content=prompt)])

    final_text = response.content
    
    save_to_semantic_cache(user_input, final_text)

    return {
            "messages": [AIMessage(content=final_text)],
            "final_response": final_text
        }



def food_flow_generate_response(state: AgentState) -> dict:
    logger.info("Generating final response (universal renderer)...")

    payload = state.get("response_payload")
    data = payload.get("data")

    if payload is None:
        return {"messages": [AIMessage(content="Erro interno: resposta vazia.")]}

    # -------------------------
    # 📜 Já é texto pronto
    # -------------------------
    if isinstance(payload, str):
        return {"messages": [AIMessage(content=payload)]}

    # -------------------------
    # 🤖 Dado estruturado → LLM formata
    # -------------------------
    llm = ChatBedrock(
        model_id=settings.MODEL_ID,
        region_name=settings.AWS_REGION,
        model_kwargs={
            "temperature": 0.3,
            "max_tokens": 500,
        },
    )

    prompt = f"""
        Você é um assistente inteligente.

        Transforme os dados estruturados abaixo em uma resposta clara, natural e útil para o usuário.

        Dados:
        {data}

        Regras:
        - Não mencione JSON
        - Seja direto e amigável
        - Se for lista, organize visualmente
        - Se envolver valores monetários, destaque totais
        - Se envolver restaurantes, ajude o usuário a decidir o próximo passo
        """

    response = llm.invoke([HumanMessage(content=prompt)])

    final_text = response.content
    
    return {
            "messages": [AIMessage(content=final_text)],
            "final_response": final_text
        }




def football_flow_generate_response(state: AgentState) -> dict:
    logger.info("Generating final response (universal renderer)...")

    payload = state.get("response_payload")
    data = payload.get("data")

    if payload is None:
        return {"messages": [AIMessage(content="Erro interno: resposta vazia.")]}

    # -------------------------
    # 📜 Já é texto pronto
    # -------------------------
    if isinstance(payload, str):
        return {"messages": [AIMessage(content=payload)]}

    # -------------------------
    # 🤖 Dado estruturado → LLM formata
    # -------------------------
    llm = ChatBedrock(
        model_id=settings.MODEL_ID,
        region_name=settings.AWS_REGION,
        model_kwargs={
            "temperature": 0.3,
            "max_tokens": 500,
        },
    )

    prompt = f"""
        Você é um assistente inteligente.

        Transforme os dados estruturados abaixo em uma resposta clara, natural e útil para o usuário.

        Dados:
        {data}

        Regras:
        - Não mencione JSON
        - Seja direto e amigável
        - Se for lista, organize visualmente
        - Se envolver valores monetários, destaque totais
        - Se envolver restaurantes, ajude o usuário a decidir o próximo passo
        """

    response = llm.invoke([HumanMessage(content=prompt)])

    final_text = response.content

    return {
            "messages": [AIMessage(content=final_text)],
            "final_response": final_text
        }

