from memory.database import delete_memory, get_all_memories, get_memory, save_memory


def normalize_key(key):
    key = key.strip().lower()
    return key[3:] if key.startswith("my ") else key


def remember(key, value):
    key, value = normalize_key(key), value.strip()
    if not key or not value:
        raise ValueError("memory name and value cannot be empty")
    save_memory(key, value)
    return f"I will remember that your {key} is {value}."


def recall(key):
    key = normalize_key(key)
    value = get_memory(key)
    return f"Your {key} is {value}." if value is not None else f"I don't remember anything about your {key}."


def list_memories():
    memories = get_all_memories()
    if not memories:
        return "I have no saved memories."
    return "Saved memories:\n" + "\n".join(f"- {key}: {value}" for key, value in memories)


def forget(key):
    key = normalize_key(key)
    return f"I forgot your {key}." if delete_memory(key) else f"I don't have a memory called {key}."
