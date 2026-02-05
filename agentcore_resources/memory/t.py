# ==========================================
# TURNO 1: Mensagens iniciais
# ==========================================
print("Turno 1: Usuário reporta problema")
client.create_event(
    memory_id=memory['id'],
    actor_id="customer-456",
    session_id="ticket-789",
    messages=[
        ("Meu site está fora do ar", "USER"),
        ("Vou verificar o status do seu servidor", "ASSISTANT")
    ]
)

time.sleep(2)

# ==========================================
# TURNO 2: APENAS as mensagens NOVAS
# ==========================================
print("Turno 2: Diagnóstico em andamento")
client.create_event(
    memory_id=memory['id'],
    actor_id="customer-456",
    session_id="ticket-789",  # MESMO session_id
    messages=[
        # ✅ APENAS o que é NOVO neste turno
        ("check_server_health(domain='example.com')", "TOOL"),
        ("O servidor está em execução, mas o disco está 100% cheio", "TOOL"),
        ("Preciso liberar espaço em disco", "ASSISTANT")
    ]
)

time.sleep(2)

# ==========================================
# TURNO 3: APENAS as mensagens NOVAS
# ==========================================
print("Turno 3: Resolução")
client.create_event(
    memory_id=memory['id'],
    actor_id="customer-456",
    session_id="ticket-789",  # MESMO session_id
    messages=[
        # ✅ APENAS o que é NOVO neste turno
        ("clean_disk_space(path='/var/log')", "TOOL"),
        ("5GB liberados, disco agora em 80%", "TOOL"),
        ("Seu site deve estar online novamente agora", "ASSISTANT"),
        ("Sim! Está funcionando. Obrigado!", "USER")  # ⬅️ SINAL DE CONCLUSÃO
    ]
)

time.sleep(60)
