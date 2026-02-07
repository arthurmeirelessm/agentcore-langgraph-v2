from fastapi import FastAPI
from pydantic import BaseModel
from runtime_market_agent import get_agent

app = FastAPI()
agent = get_agent()


class AgentRequest(BaseModel):
    prompt: str
    actor_id: str
    session_id: str


@app.post("/agent")
def run_agent(req: AgentRequest):
    response = agent.process_request(
        user_input=req.prompt,
        actor_id=req.actor_id,
        session_id=req.session_id
    )

    return {
        "response": response,
        "actor_id": req.actor_id,
        "session_id": req.session_id
    }
