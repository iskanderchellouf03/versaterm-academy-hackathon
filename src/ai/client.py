import streamlit as st

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


def stream_completion(messages, model=None):
    """Stream a chat completion, showing tokens live in st.write_stream. Returns full text."""
    from src.config import AZURE_OPENAI_DEPLOYMENT
    client = get_client()
    deployment = model or AZURE_OPENAI_DEPLOYMENT

    stream = client.chat.completions.create(
        model=deployment,
        messages=messages,
        stream=True,
    )

    def _token_gen():
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    result = st.write_stream(_token_gen())
    return result
