# Criar Models no API Gateway definindo o JSON Schema dos payloads que as rotas POST irão receber
# Associar o Model ao método em Method Request → Request Body (application/json → selecionar o Model)
# (Opcional) Ativar Request Validator para validar o corpo da requisição contra o Model
# Fazer deploy da API para o stage após configurar o Request Body
# Exportar o OpenAPI do stage já com requestBody gerado a partir do Model
# Usar esse OpenAPI atualizado como base do Target no AgentCore Gateway pelo CLI

# Comando que atualiza OpenAPI do Stage API gateway
# aws apigateway put-rest-api \
#  --rest-api-id b5sfekwebl \
# --mode overwrite \
# --body file://openapi_apigateway_export.json \
#  --cli-binary-format raw-in-base64-out





import requests
import json
import random
import uuid


GATEWAY_URL = "https://gateway-quick-test-agent-tools-hzok8pngst.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp"
GATEWAY_TARGET = "target-quick-start-gl068n"


def get_user(user_id):
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

    # montar frase amigável
    formatted = (
        f"O usuário {user_data.get('user_id')} mora em "
        f"{user_data.get('city')} - {user_data.get('state')}, "
        f"no bairro {user_data.get('neighborhood')}. "
        f"Coordenadas aproximadas: "
        f"({user_data.get('lat')}, {user_data.get('lng')})."
    )

    return formatted



def find_restaurants():
    """Busca restaurantes e monta resposta dinâmica com menu completo"""

    payload = {
        "jsonrpc": "2.0",
        "id": "call-tool-request",
        "method": "tools/call",
        "params": {
            "name": f"{GATEWAY_TARGET}___location",
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

    if "error" in result:
        raise Exception(f"JSON-RPC error: {result['error']}")

    if result.get("result", {}).get("isError"):
        error_msg = result["result"]["content"][0]["text"]
        raise Exception(f"Tool error: {error_msg}")

    raw_text = result["result"]["content"][0]["text"]
    data = json.loads(raw_text)

    city = data.get("city")
    neighborhood = data.get("neighborhood")
    total = data.get("total_restaurants", 0)
    restaurants = data.get("restaurants", [])

    if total == 0:
        return f"Não encontrei restaurantes em {neighborhood}, {city}."

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

        # 🔹 MENU COMPLETO
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
    return formatted_response



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

    restaurant_id = data.get("restaurant_id")
    items = data.get("items", [])
    subtotal = data.get("subtotal", 0)
    delivery_fee = data.get("delivery_fee", 0)
    service_fee = data.get("service_fee", 0)
    total = data.get("total", 0)
    currency = data.get("currency", "BRL")
    eta = data.get("estimated_delivery_minutes")

    # 🔹 Cabeçalho
    header = f"🧾 **Resumo do pedido — Restaurante {restaurant_id}**\n\n"

    # 🔹 Itens
    item_lines = []
    for i, item in enumerate(items, start=1):
        name = item.get("name")
        qty = item.get("quantity")
        unit = item.get("unit_price")
        line_total = item.get("line_total")

        line = f"{i}. {name} — {qty}x R${unit:.2f} = R${line_total:.2f}"
        item_lines.append(line)

    items_block = "\n".join(item_lines)

    # 🔹 Totais
    totals_block = (
        f"\n\nSubtotal: R${subtotal:.2f}\n"
        f"Taxa de entrega: R${delivery_fee:.2f}\n"
        f"Taxa de serviço: R${service_fee:.2f}\n"
        f"---------------------------\n"
        f"**Total: R${total:.2f} {currency}**\n"
    )

    # 🔹 Entrega
    delivery_info = f"\n⏱️ Tempo estimado de entrega: {eta} minutos"
    
    final_text_result = header + items_block + totals_block + delivery_info

    return final_text_result

# TESTE
if __name__ == "__main__":
    try:
         # user_data = get_user("user_sl_001")
         # print(json.dumps(user_data, indent=2))
         #location = find_restaurants()
         # print(json.dumps(user_data, indent=2))
         simulate_order = simulate_order_price()
         print(json.dumps(simulate_order, indent=2))
    except Exception as e:
        print(f"❌ Erro: {e}")