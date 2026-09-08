from brain import KalraBrain
from memory.database import initialize_database


def main() -> None:
    initialize_database()
    brain = KalraBrain()
    print("KAL.RA AI v0.5 Universal Windows + Local Memory")
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
