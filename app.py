from brain import KalraBrain


def main() -> None:
    brain = KalraBrain()
    print("KAL.RA AI v0.3")
    print("Private. Personal. Local.")
    print("Type 'help' for commands or 'exit' to close.\n")

    while True:
        try:
            message = input("You > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nKAL.RA > Goodbye.")
            break

        if not message:
            continue
        if message.lower() in {"exit", "quit", "bye"}:
            print("KAL.RA > Goodbye.")
            break

        result = brain.handle(message)
        print(f"KAL.RA > {result}\n")


if __name__ == "__main__":
    main()
