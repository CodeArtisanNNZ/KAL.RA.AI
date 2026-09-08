from memory.database import get_memory, save_memory


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
