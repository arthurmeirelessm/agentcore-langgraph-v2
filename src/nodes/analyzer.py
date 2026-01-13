import json
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate

from src.config.settings import settings
from src.state import AgentState
from src.utils.logger import setup_logger

logger = setup_logger(__name__)



def analyze_request(state: AgentState) -> AgentState:
    """
    Analisa a requisição do usuário e decide próximos passos
    
    Args:
        state: Estado atual do grafo
    
    Returns:
        Estado atualizado
    """
    try:
        logger.info("Analyzing user request...")
        
        # Pega última mensagem do usuário
        messages = state.get("messages", [])
        if not messages:
            state["error"] = "No messages to process"
            state["next_step"] = "end"
            return state
        
        last_message = messages[-1]
        user_input = last_message.get("content", "")
        
        # Inicializa modelo Bedrock
        llm = ChatBedrock(
            model_id=settings.MODEL_ID,
            region_name=settings.AWS_REGION,
            model_kwargs={
                "temperature": settings.MODEL_TEMPERATURE,
                "max_tokens": settings.MODEL_MAX_TOKENS
            }
        )
        
        # Prompt para decidir ferramentas
        analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", settings.SYSTEM_PROMPT),
            ("system", """Considerando a mensagem do usuário, determine quais ferramentas (se houver) devem ser chamadas.

Ferramentas disponíveis:
- get_stock_data: Obter dados de preços de ações em tempo real para um determinado símbolo
- search_news: Pesquisar notícias financeiras
- save_broker_profile: Salvar informações do perfil da corretora
- get_broker_profile: Recuperar informações do perfil da corretora

Responda com um objeto JSON contendo:
{{
    "tools_needed": ["tool1", "tool2"],
    "tool_params": {{"tool1": {{"param": "value"}}}},
    "reasoning": "Por que essas ferramentas são necessárias?",
    "needs_tools": true/false
}}

Caso não sejam necessárias ferramentas, defina needs_tools como false e forneça uma resposta direta."""),
            ("human", "{input}")
        ])
        
        # Analisa requisição
        chain = analysis_prompt | llm
        response = chain.invoke({"input": user_input})
        
        # Parse resposta
        content = response.content
        
        # Tenta extrair JSON da resposta
        try:
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "{" in content:
                json_str = content[content.find("{"):content.rfind("}")+1]
            else:
                json_str = content
            
            analysis = json.loads(json_str)
        except:
            # Se não conseguir parsear, assume que não precisa de tools
            analysis = {
                "needs_tools": False,
                "tools_needed": [],
                "direct_response": content
            }
        
        # Atualiza estado
        if analysis.get("needs_tools", False):
            state["tools_to_execute"] = analysis.get("tools_needed", [])
            state["next_step"] = "execute_tools"
            logger.info(f"Tools to execute: {state['tools_to_execute']}")
        else:
            # Resposta direta sem ferramentas
            state["final_response"] = analysis.get("direct_response", content)
            state["next_step"] = "end"
            logger.info("Direct response without tools")
        
        return state
        
    except Exception as e:
        logger.error(f"Error in analyze_request: {e}")
        state["error"] = str(e)
        state["next_step"] = "end"
        return state