"""String helpers."""


def slugify(text):
    """Turn arbitrary text into a URL-safe slug."""
    # split() drops leading/trailing separators and collapses runs, so joining
    # yields exactly one hyphen between tokens and none at the edges.
    return "-".join(text.lower().split())


def truncate(text, limit):
    """Shorten text to limit characters, appending an ellipsis when cut."""
    if len(text) <= limit:
        return text
    return text[:limit] + "..."
