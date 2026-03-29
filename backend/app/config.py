import os
from dotenv import load_dotenv

load_dotenv()


def get_api_key(header_key: str | None = None) -> str:
    """Return the Gemini API key from the request header, falling back to .env."""
    key = header_key or os.getenv("GEMINI_API_KEY", "")
    if not key:
        raise ValueError(
            "GEMINI_API_KEY not provided. Pass it via the X-API-Key header or set it in .env."
        )
    return key
