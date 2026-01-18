from bedrock_agentcore.memory import MemoryClient
import time
from datetime import datetime

# ==========================================
# CONFIGURAÇÃO
# ==========================================

client = MemoryClient(region_name="us-east-1")

# Substitua pelo memoryId que você recebeu ao criar a memory
MEMORY_ID = "memory_0l8tc-yybn7WEnWj"  # Ex: "mem-abc123xyz789"
ACTOR_ID = "customer-456"
SESSION_ID = "ticket-789"

print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando teste de Episodic Memory")
print(f"Memory ID: {MEMORY_ID}")
print(f"Actor ID: {ACTOR_ID}")
print(f"Session ID: {SESSION_ID}")
print("=" * 60)

# ==========================================
# PROCESSAMENTO ASSÍNCRONO
# ==========================================


print(f"\n[{datetime.now().strftime('%H:%M:%S')}] TURNO 1: Usuário reporta problema")
print("-" * 60)

try:
    event1 = client.create_event(
    memory_id=MEMORY_ID,
    actor_id=ACTOR_ID,
    session_id=SESSION_ID,
    messages=[
        ("Obrigado, deu certo!", "USER"),
        (
            "Fico feliz em ajudar! Se precisar de algo mais, é só me chamar.",
            "ASSISTANT"
        )
    ]
)

    print("✅ Evento 1 salvo na SHORT-TERM MEMORY")
    print(f"   Event ID: {event1.get('eventId')}")
    print("❌ Episódio NÃO gerado ainda (conversa não terminou)")
except Exception as e:
    print(f"❌ Erro ao salvar Evento 1: {e}")
    exit(1)

time.sleep(2)  # Pequena pausa para simular tempo real

