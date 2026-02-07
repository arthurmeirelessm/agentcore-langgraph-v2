from runtime_market_agent import get_agent

def main():
    agent = get_agent()

    print("🧠 Market Trends Agent (local)")
    print("Digite 'exit' para sair")

    user_input = "Algo sobre AAPL?"
    
    response = agent.process_request(
        user_input=user_input,
        actor_id="user_sl_001",
        session_id="local_session_343434"
    )

    print("\nAgent >", response)


if __name__ == "__main__":
    main()
