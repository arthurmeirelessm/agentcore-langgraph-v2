import boto3
import json

client = boto3.client('bedrock-agentcore', region_name='us-east-1')

# Payload atualizado
payload_dict = {
    "prompt": "Qual o valroes atual da NVIDIA?",
    "actor_id": "12345",
    "session_id": "3456789",
    "identity_id": "1234r-defgh-4e56dfh-34te5yh",
    "context": {
        "timezone": "Asia/Tokyo",
        "language": "en"
    }
}

# Converter para JSON em bytes (requisito do invoke_agent_runtime)
payload_bytes = json.dumps(payload_dict).encode("utf-8")

# Invocação do AgentCore Runtime
response = client.invoke_agent_runtime(
    agentRuntimeArn="arn:aws:bedrock-agentcore:us-east-1:828416928234:runtime/MarketAgent-sHNbMyEWMH",
    runtimeSessionId="session123456789012345678901234567890123",  # Deve ter 33+ caracteres
    payload=payload_bytes
)

# Ler resposta e decodificar
response_body = response["response"].read()
response_data = json.loads(response_body)

# Mostrar resposta formatada
print("Agent Response:", json.dumps(response_data, indent=2))
