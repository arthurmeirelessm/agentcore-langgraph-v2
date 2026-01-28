import requests
from langchain.tools import tool


GATEWAY_URL = "https://gateway-quick-test-agent-tools-hzok8pngst.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp"

# ===============================
# Tool: get_user
# ===============================
@tool
def get_user(user_id: str):
    """
    Chama a tool get_user via gateway AgentCore.
    Params:
        user_id (str)
    Returns:
        dict: resultado da tool
    """
    payload = {
        "jsonrpc": "2.0",
        "id": "get_user-request",
        "method": "target-quick-start-27a773___get_user",
        "params": {
            "basePath": f"/delivery-food/user/{user_id}"
        }
    }

    response = requests.post(GATEWAY_URL, json=payload)
    response.raise_for_status()
    return response.json().get("result", {})


# ===============================
# Tool: location
# ===============================
@tool
def location(city: str, neighborhood: str):
    """
    Chama a tool location via gateway AgentCore.
    Params:
        city (str)
        neighborhood (str)
    Returns:
        dict: resultado da tool
    """
    payload = {
        "jsonrpc": "2.0",
        "id": "location-request",
        "method": "target-quick-start-27a773___location",
        "params": {
            "basePath": f"/delivery-food/location",
            "body": {
                "city": city,
                "neighborhood": neighborhood
            }
        }
    }

    response = requests.post(GATEWAY_URL, json=payload)
    response.raise_for_status()
    return response.json().get("result", {})