from bedrock_agentcore.memory import MemoryClient
from datetime import datetime

client = MemoryClient(region_name="us-east-1")
MEMORY_ID = "memory_0l8tc-yybn7WEnWj"
STRATEGY_ID = "episodic_override_3olwc-ELGZBf7fd9"
ACTOR_ID = "customer-456"

total_found = 0
all_records = []

print("=" * 70)
print("🔬 DIAGNÓSTICO COMPLETO - EPISODIC MEMORY")
print("=" * 70)
print(f"Timestamp: {datetime.now()}")
print(f"Memory ID: {MEMORY_ID}")
print(f"Strategy ID: {STRATEGY_ID}")
print(f"Actor ID: {ACTOR_ID}\n")

episodic_namespace = f"/strategies/{STRATEGY_ID}/actors/{ACTOR_ID}/sessions/ticket-789"
episodic_query = "application crashing memory"

reflection_namespace = f"/strategies/{STRATEGY_ID}/actors/{ACTOR_ID}"
reflection_query = "server troubleshooting resources"

try:
    result = client.retrieve_memories(
        memory_id=MEMORY_ID,
        namespace=reflection_namespace,
        query=reflection_query,
        top_k=10
    )

    records = result if isinstance(result, list) else result.get("memoryRecords", [])

    if records:
        print(f"   ✅ Encontrados {len(records)} registro(s)")
        total_found += len(records)

        # Evitar duplicatas
        for rec in records:
            rec_id = rec.get("id") or str(rec.get("content", ""))[:50]
            if not any(r.get("id") == rec_id for r in all_records):
                all_records.append(rec)

        by_type = {}
        for rec in records:
            rec_type = rec.get("type", "UNKNOWN")
            by_type[rec_type] = by_type.get(rec_type, 0) + 1

        for rec_type, count in by_type.items():
            print(f"      • {rec_type}: {count}")
    else:
        print("   ⚠️  Nenhum registro encontrado")

except Exception as e:
    print(f"   ❌ Erro: {e}")

# ==========================================
# 3. EXIBIR EPISÓDIOS ENCONTRADOS
# ==========================================

if all_records:
    print("\n\n3️⃣ DETALHES DOS REGISTROS ENCONTRADOS")
    print("=" * 70)
