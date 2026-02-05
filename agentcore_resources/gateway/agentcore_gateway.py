# Criar Models no API Gateway definindo o JSON Schema dos payloads que as rotas POST irão receber
# Associar o Model ao método em Method Request → Request Body (application/json → selecionar o Model)
# (Opcional) Ativar Request Validator para validar o corpo da requisição contra o Model
# Fazer deploy da API para o stage após configurar o Request Body
# Exportar o OpenAPI do stage já com requestBody gerado a partir do Model
# Usar esse OpenAPI atualizado como base do Target no AgentCore Gateway




import requests
import json

GATEWAY_URL = "https://gateway-quick-test-agent-tools-hzok8pngst.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp"

def get_user(user_id):
    """Busca informações de um usuário"""
    
    payload = {
        "jsonrpc": "2.0",
        "id": "call-tool-request",
        "method": "tools/call",
        "params": {
            "name": "target-quick-start-wzjozy___get_user",
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
    
    # Verificar erros
    if "error" in result:
        raise Exception(f"JSON-RPC error: {result['error']}")
    
    if result.get("result", {}).get("isError"):
        error_msg = result["result"]["content"][0]["text"]
        raise Exception(f"Tool error: {error_msg}")
    
    return result.get("result", {})


def find_restaurants():
    """Busca informações de localização de restaurantes"""
    
    payload = {
        "jsonrpc": "2.0",
        "id": "call-tool-request",
        "method": "tools/call",
        "params": {
            "name": "target-quick-start-wzjozy___location",
            "arguments": {
                "city": "São Luís",
                "neighborhood": "Cohatrac"
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
    
    # Verificar erros
    if "error" in result:
        raise Exception(f"JSON-RPC error: {result['error']}")
    
    if result.get("result", {}).get("isError"):
        error_msg = result["result"]["content"][0]["text"]
        raise Exception(f"Tool error: {error_msg}")
    
    return result.get("result", {})



# TESTE
if __name__ == "__main__":
    try:
         # user_data = get_user("user_sl_001")
         # print(json.dumps(user_data, indent=2))
         location = find_restaurants()
         print(json.dumps(location, indent=2))
    except Exception as e:
        print(f"❌ Erro: {e}")