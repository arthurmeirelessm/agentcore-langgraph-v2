import os
import uuid
from dotenv import load_dotenv
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager
from strands import Agent
from strands.models.openai import OpenAIModel


load_dotenv()

secret_key = os.getenv("OPENAI_API_KEY")

DEFAULT_CONFIG = {
    'default_headers': {
        'Content-Type': 'application/json',
    }
}

MEMORY_ID = "<memory_id>"
REGION = "us-east-1"


def get_retrieval(top_k: int, relevance_score: float) -> RetrievalConfig:
    return RetrievalConfig(
        top_k=top_k,
        relevance_score=relevance_score
    )


config_mem = AgentCoreMemoryConfig(
    memory_id=MEMORY_ID,
    actor_id="hugo",
    session_id=uuid.uuid4().hex,
    retrieval_config={
        '/preferences/{actorId}': get_retrieval(top_k=5, relevance_score=0.7),
        '/facts/{actorId}': get_retrieval(top_k=10, relevance_score=0.5),
        '/summaries/{actorId}/{sessionId}': get_retrieval(top_k=10, relevance_score=0.5)
    }
)

session_manager = AgentCoreMemorySessionManager(agentcore_memory_config=config_mem)

llm = OpenAIModel(
    model_id="gpt-4o-mini",
    client_args={
        "api_key": secret_key,
    }
)

agent = Agent(
    model='anthropic.claude-2',
    session_manager=session_manager,
    system_prompt="Você é um assistente conciso."
)

while True:
    try:        
        text = input("Você: ")
        response = agent(text)

        print(f"Agent: {response}")
    except KeyboardInterrupt:
        print("\nEncerrando o assistente. Até logo!")
        break