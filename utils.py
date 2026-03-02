import re

def split_long_message(text: str, max_length: int = 4000) -> list:
    """Split a long message into chunks not exceeding max_length."""
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

def extract_code_from_markdown(text: str) -> str:
    """Extract code from markdown code blocks (```python ... ```)."""
    if "```python" in text:
        return text.split("```python")[1].split("```")[0].strip()
    if "```" in text:
        return text.split("```")[1].split("```")[0].strip()
    return text.strip()
