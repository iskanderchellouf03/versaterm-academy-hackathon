_client = None


def get_client():
    global _client
    if _client is not None:
        return _client

    from openai import AzureOpenAI
    from src.config import (
        AZURE_OPENAI_ENDPOINT,
        AZURE_OPENAI_API_KEY,
        AZURE_OPENAI_API_VERSION,
        OPENAI_TIMEOUT,
    )

    if not AZURE_OPENAI_API_KEY:
        raise ValueError("AZURE_OPENAI_API_KEY is not set. Please configure it in your .env file.")
    _client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        timeout=OPENAI_TIMEOUT,
    )
    return _client
