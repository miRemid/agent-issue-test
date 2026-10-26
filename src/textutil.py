"""String helpers."""


def slugify(text):
    """Turn arbitrary text into a URL-safe slug.

    Consecutive whitespace collapses to a single hyphen; leading and
    trailing whitespace never becomes a hyphen (#20).
    """
    return "-".join(text.lower().split())


def truncate(text, limit):
    """Shorten text to limit characters, appending an ellipsis when cut."""
    if len(text) <= limit:
        return text
    return text[:limit] + "..."
