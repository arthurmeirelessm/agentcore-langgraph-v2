from bedrock_agentcore.memory import MemoryClient

client = MemoryClient(region_name="us-east-1")

# Criar memória com episodic strategy
memory = client.create_memory_and_wait(
    name="agentcoreepisodicmemoryincrementall_pt",
    strategies=[  # ← LISTA, não dict
        {
            "episodicMemoryStrategy": {
                # Configuração principal
                "name": "episodic_strategy",
                "description": "Stores independent episodic interactions",

                # ✅ LISTA de namespaces (não string)
                "namespaces": [
                    "/strategies/{memoryStrategyId}/actors/{actorId}/sessions/{sessionId}"
                ],

                # Configuração de reflections
                "reflectionConfiguration": {
                    # ✅ LISTA de namespaces (não string)
                    "namespaces": [
                        "/strategies/{memoryStrategyId}/actors/{actorId}"
                    ]
                }
            }
        }
    ]
)

print(f"✅ Memory criada com sucesso!")
print(f"Memory ID: {memory['id']}")
print(f"Memory Name: {memory['name']}")
print(f"Status: {memory['status']}")

# Extrair strategy ID
for strategy in memory.get('strategies', []):
    if 'episodicMemoryStrategy' in strategy:
        strat = strategy['episodicMemoryStrategy']
        print(f"\n📋 Episodic Strategy:")
        print(f"   ID: {strat['id']}")
        print(f"   Name: {strat['name']}")
        print(f"   Namespaces: {strat['namespaces']}")