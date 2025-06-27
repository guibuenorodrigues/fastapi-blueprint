def slugify(text: str) -> str:
    """
    Converts a string into a URL-friendly slug.
    Example: "My New Project" -> "my-new-project".
    """
    import re

    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)  # Remove non-word chars
    text = re.sub(r"[\s_-]+", "-", text)  # Replace spaces/underscores with single dash
    text = text.strip("-")  # Remove leading/trailing dashes
    return text
