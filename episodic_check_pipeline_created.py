from bedrock_agentcore.memory import MemoryClient
from datetime import datetime

client = MemoryClient(region_name="us-east-1")
MEMORY_ID = "memory_0l8tc-yybn7WEnWj"
STRATEGY_ID = "episodic_override_3olwc-ELGZBf7fd9"
ACTOR_ID = "customer-456"

print("=" * 70)
print("🔬 DIAGNÓSTICO COMPLETO - EPISODIC MEMORY")
print("=" * 70)
print(f"Timestamp: {datetime.now()}")
print(f"Memory ID: {MEMORY_ID}")
print(f"Strategy ID: {STRATEGY_ID}")
print(f"Actor ID: {ACTOR_ID}\n")

# ==========================================
# 1. VERIFICAR EVENTOS CRIADOS
# ==========================================

print("1️⃣ EVENTOS CRIADOS (SHORT-TERM MEMORY)")
print("-" * 70)



events_found = []
sessions_to_check = ["ticket-789", "ticket-790"]

for session_id in sessions_to_check:
    try:
        print(f"Buscando eventos da session {session_id}...")
        events = client.list_events(
            memory_id=MEMORY_ID,
            actor_id=ACTOR_ID,
            session_id=session_id
        )
        
        if isinstance(events, dict):
            session_events = events.get('events', [])
        elif isinstance(events, list):
            session_events = events
        else:
            session_events = []
        
        if session_events:
            print(f"✅ Encontrados {len(session_events)} evento(s) na session {session_id}\n")
            events_found.extend(session_events)
            
            for idx, event in enumerate(session_events, 1):
                print(f"   Evento {idx}:")
                print(f"      Event ID: {event.get('eventId', 'N/A')}")
                print(f"      Timestamp: {event.get('eventTimestamp', event.get('timestamp', 'N/A'))}")
                
                payload = event.get('payload', [])
                if isinstance(payload, list):
                    print(f"      Total de turnos: {len(payload)}")
                    if payload:
                        first = payload[0]
                        last = payload[-1]
                        
                        first_text = first.get('text', {}).get('text', 'N/A')[:60]
                        first_role = first.get('roleType', 'N/A')
                        print(f"      Primeira msg: [{first_role}] {first_text}...")
                        
                        last_text = last.get('text', {}).get('text', 'N/A')[:60]
                        last_role = last.get('roleType', 'N/A')
                        print(f"      Última msg: [{last_role}] {last_text}...")
                print()
        else:
            print(f"⚠️  Nenhum evento encontrado na session {session_id}\n")
            
    except Exception as e:
        print(f"⚠️  Erro ao listar eventos da session {session_id}: {e}\n")

# ==========================================
# 2. BUSCAR EPISÓDIOS
# ==========================================

print("\n2️⃣ BUSCANDO EPISÓDIOS GERADOS")
print("-" * 70)

searches = [
    {
        "name": "Session ticket-789",
        "namespace": f"/strategies/{STRATEGY_ID}/actors/{ACTOR_ID}/sessions/ticket-789",
        "query": "website downtime disk space"
    },
    {
        "name": "Session ticket-790",
        "namespace": f"/strategies/{STRATEGY_ID}/actors/{ACTOR_ID}/sessions/ticket-790",
        "query": "application crashing memory"
    },
    {
        "name": "Todas as sessions do actor",
        "namespace": f"/strategies/{STRATEGY_ID}/actors/{ACTOR_ID}",
        "query": "server troubleshooting resources"
    }
]

total_found = 0
all_records = []

for search in searches:
    print(f"\n🔍 {search['name']}")
    print(f"   Namespace: {search['namespace']}")
    print(f"   Query: '{search['query']}'")
    
    try:
        result = client.retrieve_memories(
            memory_id=MEMORY_ID,
            namespace=search['namespace'],
            query=search['query'],
            top_k=10
        )
        
        records = result if isinstance(result, list) else result.get('memoryRecords', [])
        
        if records:
            print(f"   ✅ Encontrados {len(records)} registro(s)")
            total_found += len(records)
            
            # Evitar duplicatas
            for rec in records:
                rec_id = rec.get('id') or str(rec.get('content', ''))[:50]
                if not any(r.get('id') == rec_id for r in all_records):
                    all_records.append(rec)
            
            by_type = {}
            for rec in records:
                rec_type = rec.get('type', 'UNKNOWN')
                by_type[rec_type] = by_type.get(rec_type, 0) + 1
            
            for rec_type, count in by_type.items():
                print(f"      • {rec_type}: {count}")
        else:
            print(f"   ⚠️  Nenhum registro encontrado")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")

# ==========================================
# 3. EXIBIR EPISÓDIOS ENCONTRADOS
# ==========================================

if all_records:
    print(f"\n\n3️⃣ DETALHES DOS REGISTROS ENCONTRADOS")
    print("=" * 70)
    
    # Agrupar por tipo
    episodes = [r for r in all_records if r.get('type') == 'EPISODE']
    reflections = [r for r in all_records if r.get('type') == 'REFLECTION']
    unknown = [r for r in all_records if r.get('type') not in ['EPISODE', 'REFLECTION']]
    
    # Exibir EPISÓDIOS
    if episodes:
        print(f"\n📖 EPISÓDIOS ({len(episodes)}):\n")
        for idx, ep in enumerate(episodes, 1):
            print(f"{'─' * 70}")
            print(f"EPISÓDIO {idx}")
            print(f"{'─' * 70}")
            print(f"Session ID: {ep.get('sessionId', 'N/A')}")
            print(f"Namespace: {ep.get('namespace', 'N/A')}")
            print(f"Relevance Score: {ep.get('relevanceScore', 'N/A')}")
            print(f"\nConteúdo:\n")
            print(ep.get('content', 'N/A'))
            print("\n")
    
    # Exibir REFLECTIONS
    if reflections:
        print(f"\n🧠 REFLECTIONS ({len(reflections)}):\n")
        for idx, ref in enumerate(reflections, 1):
            print(f"{'─' * 70}")
            print(f"REFLECTION {idx}")
            print(f"{'─' * 70}")
            print(f"Namespace: {ref.get('namespace', 'N/A')}")
            print(f"Relevance Score: {ref.get('relevanceScore', 'N/A')}")
            print(f"\nConteúdo:\n")
            print(ref.get('content', 'N/A'))
            print("\n")
    
    # Exibir UNKNOWN (podem ser episódios sem type definido)
    if unknown:
        print(f"\n❓ REGISTROS SEM TIPO DEFINIDO ({len(unknown)}):\n")
        for idx, rec in enumerate(unknown, 1):
            print(f"{'─' * 70}")
            print(f"REGISTRO {idx}")
            print(f"{'─' * 70}")
            print(f"Type: {rec.get('type', 'N/A')}")
            print(f"Session ID: {rec.get('sessionId', 'N/A')}")
            print(f"Namespace: {rec.get('namespace', 'N/A')}")
            print(f"Relevance Score: {rec.get('relevanceScore', 'N/A')}")
            print(f"\nConteúdo completo:\n")
            content = rec.get('content', 'N/A')
            print(content)
            print("\n")

# ==========================================
# 4. RESUMO E DIAGNÓSTICO
# ==========================================

print("\n" + "=" * 70)
print("📊 RESUMO DO DIAGNÓSTICO")
print("=" * 70)

print(f"\n📝 Eventos (Short-term):")
if events_found:
    print(f"   ✅ {len(events_found)} evento(s) criado(s)")
    sessions = list(set(e.get('sessionId') for e in events_found))
    print(f"   Sessions: {', '.join(sessions)}")
else:
    print(f"   ⚠️  Nenhum evento listado (pode ser limitação da API)")

print(f"\n🧠 Registros de Longo Prazo:")
print(f"   Total encontrado: {len(all_records)} registro(s) único(s)")

if all_records:
    episodes = [r for r in all_records if r.get('type') == 'EPISODE']
    reflections = [r for r in all_records if r.get('type') == 'REFLECTION']
    unknown = [r for r in all_records if r.get('type') not in ['EPISODE', 'REFLECTION']]
    
    print(f"   📖 Episódios: {len(episodes)}")
    print(f"   🧠 Reflections: {len(reflections)}")
    print(f"   ❓ Sem tipo: {len(unknown)}")
    
    print(f"\n✅ SUCESSO! O sistema gerou memórias episódicas!")
    
    if unknown:
        print(f"\n💡 OBSERVAÇÃO:")
        print(f"   Os {len(unknown)} registros sem tipo provavelmente SÃO episódios,")
        print(f"   mas o campo 'type' não foi retornado pela API.")
        print(f"   Verifique o conteúdo XML acima - se tem <situation>, <intent>,")
        print(f"   <assessment>, então é um episódio válido!")
else:
    print(f"\n❌ Nenhuma memória de longo prazo encontrada")

print("\n" + "=" * 70)



