from bedrock_agentcore.memory import MemoryClient
import time
from datetime import datetime

# ==========================================
# CONFIGURAÇÃO
# ==========================================

client = MemoryClient(region_name="us-east-1")

# Substitua pelo memoryId que você recebeu ao criar a memory
MEMORY_ID = "SupportBot-5Ogsns78Z2"  # Ex: "mem-abc123xyz789"
ACTOR_ID = "customer-456"
SESSION_ID = "ticket-789"

print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando teste de Episodic Memory")
print(f"Memory ID: {MEMORY_ID}")
print(f"Actor ID: {ACTOR_ID}")
print(f"Session ID: {SESSION_ID}")
print("=" * 60)

# ==========================================
# TURNO 1: Usuário reporta problema
# ==========================================

print(f"\n[{datetime.now().strftime('%H:%M:%S')}] TURNO 1: Usuário reporta problema")
print("-" * 60)

try:
    event1 = client.create_event(
    memory_id=MEMORY_ID,
    actor_id=ACTOR_ID,
    session_id=SESSION_ID,
    messages=[
        ("Meu site está fora do ar", "USER"),
        ("Vou investigar", "ASSISTANT")
    ]
)

    print("✅ Evento 1 salvo na SHORT-TERM MEMORY")
    print(f"   Event ID: {event1.get('eventId')}")
    print("❌ Episódio NÃO gerado ainda (conversa não terminou)")
except Exception as e:
    print(f"❌ Erro ao salvar Evento 1: {e}")
    exit(1)

time.sleep(2)  # Pequena pausa para simular tempo real

# ==========================================
# TURNO 2: Diagnóstico em andamento
# ==========================================

print(f"\n[{datetime.now().strftime('%H:%M:%S')}] TURNO 2: Diagnóstico em andamento")
print("-" * 60)

try:
    event2 = client.create_event(
        memory_id=MEMORY_ID,
        actor_id=ACTOR_ID,
        session_id=SESSION_ID,
        messages=[
            ("check_server_health(domain='example.com')", "TOOL"),
            ("status=RUNNING, disk_usage=100%", "TOOL"),
            ("Disco cheio. Vou liberar espaço", "ASSISTANT") 
        ]
    )
    print("✅ Evento 2 salvo na SHORT-TERM MEMORY")
    print(f"   Event ID: {event2.get('eventId')}")
    print("ℹ️  Diagnóstico em progresso — episódio ainda não fechado")
except Exception as e:
    print(f"❌ Erro ao salvar Evento 2: {e}")

time.sleep(2)


# ==========================================
# TURNO 3: Resolução do problema
# ==========================================

print(f"\n[{datetime.now().strftime('%H:%M:%S')}] TURNO 3: Resolução do problema")
print("-" * 60)

try:
    event3 = client.create_event(
        memory_id=MEMORY_ID,
        actor_id=ACTOR_ID,
        session_id=SESSION_ID,  # MESMO session_id
        messages=[
            ("clean_disk_space(path='/var/log')", "TOOL"),
            ("5GB freed, 80% usage", "TOOL"),
            ("Espaço liberado, site voltou", "ASSISTANT")
        ]
    )
    print("✅ Evento 3 salvo na SHORT-TERM MEMORY")
    print(f"   Event ID: {event3.get('eventId')}")
    print("⏳ Sistema detecta conclusão → iniciando processamento assíncrono")
except Exception as e:
    print(f"❌ Erro ao salvar Evento 3: {e}")
    
    
## Evento 4 

print("\nEVENTO 4 — Encerramento")
print("-" * 60)

try:
    event4 = client.create_event(
        memory_id=MEMORY_ID,
        actor_id=ACTOR_ID,
        session_id=SESSION_ID,
        messages=[
            ("O que causou isso?", "USER"),
            ("Vou investigar os logs para identificar a causa raiz", "ASSISTANT"),
            ("inspect_log_growth(...)", "TOOL"),
            ("log_rotation=DISABLED, 42GB", "TOOL"),
            ("A causa foi rotação de logs desativada", "ASSISTANT")
        ]
    )

    print("✅ Evento 4 salvo na SHORT-TERM MEMORY")
    print(f"   Event ID: {event4.get('eventId')}")
except Exception as e:
    print(f"❌ Erro ao salvar Evento 3: {e}")
    
    

print("\nEVENTO 5 — Encerramento")
print("-" * 60)

try:
    event4 = client.create_event(
        memory_id=MEMORY_ID,
        actor_id=ACTOR_ID,
        session_id=SESSION_ID,
        messages=[
            ("Perfeito, obrigado! Agora ficou claro.", "USER")
     ]
    )

    print("✅ Evento 5 salvo na SHORT-TERM MEMORY")
    print(f"   Event ID: {event4.get('eventId')}")
except Exception as e:
    print(f"❌ Erro ao salvar Evento 3: {e}")
    

# ==========================================
# PROCESSAMENTO ASSÍNCRONO
# ==========================================

print(f"\n{'=' * 60}")
print("⏰ AGUARDANDO PROCESSAMENTO DO EPISÓDIO")
print("=" * 60)
print("O sistema está aplicando internamente:")
print("  1. Episode Extraction Prompt → analisa cada turno")
print("  2. Episode Consolidation Prompt → cria episódio único")
print("\nEste processo leva aproximadamente 60-90 segundos...")

# Aguardar com progresso visual
for i in range(12):
    time.sleep(5)
    print(f"  [{i*5 + 5}s] Processando...", end="\r")

print("\n✅ Tempo de espera concluído!")


# ==========================================
# CRIAR SEGUNDO EPISÓDIO (para testar Reflections)
# ==========================================

print(f"\n\n{'=' * 60}")
print("🔄 CRIANDO SEGUNDO EPISÓDIO SIMILAR")
print("=" * 60)
print("Para gerar Reflections, precisamos de múltiplos episódios...")

SESSION_ID_2 = "ticket-790"

try:
    # Episódio 2: Problema similar, solução similar
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Episódio 2 - Problema de memória")
    
    client.create_event(
        memory_id=MEMORY_ID,
        actor_id=ACTOR_ID,
        session_id=SESSION_ID_2,
        messages=[
            ("My application is crashing", "USER"),
            ("Let me check the server resources", "ASSISTANT"),
            ("check_server_health(domain='app.example.com')", "TOOL"),
            ("Memory usage at 98%, only 100MB free", "TOOL"),
            ("I'll clear cache and temporary files", "ASSISTANT"),
            ("clean_memory(clear_cache=True)", "TOOL"),
            ("Freed 2GB, memory now at 65%", "TOOL"),
            ("Your application should be stable now", "ASSISTANT"),
            ("Perfect! It's running smoothly. Thanks!", "USER")
        ]
    )
    
    print("✅ Episódio 2 criado com sucesso")
    print("⏳ Aguardando processamento...")
    
    time.sleep(60)
    
    # Buscar reflections
    print(f"\n{'=' * 60}")
    print("🧠 BUSCANDO REFLECTIONS GERADAS")
    print("=" * 60)
    
    reflections = client.retrieve_memories(
        memory_id=MEMORY_ID,
        namespace=f"/strategies/{{memoryStrategyId}}/actors/{ACTOR_ID}",
        query="resource management patterns troubleshooting",
        top_k=5
    )
    
    reflection_records = [r for r in reflections.get('memoryRecords', []) 
                         if r.get('type') == 'REFLECTION']
    
    if reflection_records:
        print(f"✅ Encontradas {len(reflection_records)} Reflections!")
        for idx, ref in enumerate(reflection_records, 1):
            print(f"\n{'─' * 60}")
            print(f"REFLECTION {idx}")
            print("─" * 60)
            print(f"Relevance Score: {ref.get('relevanceScore', 'N/A')}")
            print(f"\nConteúdo:")
            print(ref.get('content', 'N/A'))
    else:
        print("⚠️  Reflections ainda não foram geradas")
        print("   Reflections podem levar mais tempo (2-5 minutos após múltiplos episódios)")
        
except Exception as e:
    print(f"❌ Erro: {e}")

# ==========================================
# RESUMO FINAL
# ==========================================

print(f"\n\n{'=' * 60}")
print("📊 RESUMO DO TESTE")
print("=" * 60)
print(f"✅ Episódios criados: 2")
print(f"✅ Actor ID: {ACTOR_ID}")
print(f"✅ Sessions: {SESSION_ID}, {SESSION_ID_2}")
print(f"\n💡 Próximos passos:")
print("   1. Aguarde mais alguns minutos se não viu resultados")
print("   2. Execute retrieve_memories novamente")
print("   3. Crie mais episódios para gerar reflections mais robustas")
print("=" * 60)