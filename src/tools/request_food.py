import requests
import json
from langchain.tools import tool
import random
import uuid



GATEWAY_URL = "https://gateway-quick-test-agent-tools-hzok8pngst.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp"
GATEWAY_TARGET = "target-quick-start-gl068n"

# ===============================
# Tool: get_user
# ===============================
@tool
def get_user(user_id: str):
    """Busca informações de um usuário via tool do AgentCore"""

    payload = {
        "jsonrpc": "2.0",
        "id": "call-tool-request",
        "method": "tools/call",
        "params": {
            "name": f"{GATEWAY_TARGET}___get-user",
            "arguments": {
                "user_id": user_id
            }
        }
    }

    print(f"📤 Buscando usuário: {user_id}...")

    response = requests.post(
        GATEWAY_URL,
        headers={"Content-Type": "application/json"},
        json=payload
    )
    response.raise_for_status()

    result = response.json()

    if "error" in result:
        raise Exception(f"JSON-RPC error: {result['error']}")

    if result.get("result", {}).get("isError"):
        error_msg = result["result"]["content"][0]["text"]
        raise Exception(f"Tool error: {error_msg}")

    raw_text = result["result"]["content"][0]["text"]

    user_data = json.loads(raw_text)

    return user_data



# ===============================
# Tool: location
# ===============================
@tool
def location(city: str, neighborhood: str):
    """Busca restaurantes e monta resposta dinâmica com menu completo"""

    payload = {
        "jsonrpc": "2.0",
        "id": "call-tool-request",
        "method": "tools/call",
        "params": {
            "name": f"{GATEWAY_TARGET}___location",
            "arguments": {
                "city": city,
                "neighborhood": neighborhood
            }
        }
    }

    response = requests.post(
        GATEWAY_URL,
        headers={"Content-Type": "application/json"},
        json=payload
    )

    response.raise_for_status()
    result = response.json()

    if "error" in result:
        raise Exception(f"JSON-RPC error: {result['error']}")

    if result.get("result", {}).get("isError"):
        error_msg = result["result"]["content"][0]["text"]
        raise Exception(f"Tool error: {error_msg}")

    raw_text = result["result"]["content"][0]["text"]
    data = json.loads(raw_text)
    
    return data


@tool
def simulate_order_price():
    """Chama a tool de simulação de preço e formata o resumo do pedido"""

    random_items = [
        {
            "item_id": str(uuid.uuid4())[:8],
            "name": random.choice(["Hamburguer", "Pizza", "Refrigerante", "Batata Frita"]),
            "unit_price": round(random.uniform(12, 45), 2),
            "quantity": random.randint(1, 3)
        }
        for _ in range(random.randint(1, 4))
    ]

    payload = {
        "jsonrpc": "2.0",
        "id": "call-tool-request",
        "method": "tools/call",
        "params": {
            "name": f"{GATEWAY_TARGET}___order",
            "arguments": {
                "restaurant_id": "rest_12345",
                "items": random_items
            }
        }
    }

    response = requests.post(
        GATEWAY_URL,
        headers={"Content-Type": "application/json"},
        json=payload
    )

    response.raise_for_status()
    result = response.json()

    if "error" in result:
        raise Exception(f"JSON-RPC error: {result['error']}")

    if result.get("result", {}).get("isError"):
        error_msg = result["result"]["content"][0]["text"]
        raise Exception(f"Tool error: {error_msg}")

    raw_text = result["result"]["content"][0]["text"]
    data = json.loads(raw_text)

    return data