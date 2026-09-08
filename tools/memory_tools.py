from memory.database import (
    delete_memory,
    get_all_memories,
    get_memory,
    save_memory,
)


def normalize_key(key):
    key = key.strip().lower()

    if key.startswith("my "):
        key = key[3:]

    return key


def remember(key, value):
    key = normalize_key(key)
    value = value.strip()

    if not key:
        raise ValueError("memory name cannot be empty")

    if not value:
        raise ValueError("memory value cannot be empty")

    save_memory(key, value)

    return f"I will remember that your {key} is {value}."


def recall(key):
    key = normalize_key(key)

    if not key:
        raise ValueError("memory name cannot be empty")

    value = get_memory(key)

    if value is None:
        return f"I don't remember anything about your {key}."

    return f"Your {key} is {value}."


def list_memories():
    memories = get_all_memories()

    if not memories:
        return "I have no saved memories."

    lines = ["Saved memories:"]

    for key, value in memories:
        lines.append(f"- {key}: {value}")

    return "\n".join(lines)


def forget(key):
    key = normalize_key(key)

    if not key:
        raise ValueError("memory name cannot be empty")

    deleted = delete_memory(key)

    if not deleted:
        return f"I don't have a memory called {key}."

    return f"I forgot your {key}."
