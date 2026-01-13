from runtime_market_agent import get_agent

def main():
    agent = get_agent()

    print("🧠 Market Trends Agent (local)")
    print("Digite 'exit' para sair")

    while True:
        user_input = input("\nUser > ")
        if user_input.lower() == "exit":
            break

        response = agent.process_request(
            user_input=user_input,
            actor_id="local_user",
            session_id="local_session"
        )

        print("\nAgent >", response)


if __name__ == "__main__":
    main()
