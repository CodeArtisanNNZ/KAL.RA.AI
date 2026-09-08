from memory.database import get_memory, save_memory


def remember(key, value):
    key = key.strip().lower()
    value = value.strip()

    if not key:
        raise ValueError("memory name cannot be empty")

    if not value:
        raise ValueError("memory value cannot be empty")

    save_memory(key, value)

    return f"I will remember that {key} is {value}."


def recall(key):
    key = key.strip().lower()

    if not key:
        raise ValueError("memory name cannot be empty")

    value = get_memory(key)

    if value is None:
        return f"I don't remember anything about {key}."

    return f"{key} is {value}."