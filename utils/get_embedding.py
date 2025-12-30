import os
import requests

# Default base URL (keeps previous behavior)
DEFAULT_SILICONFLOW_BASE_URL = "https://api.siliconflow.cn/v1"


def get_embedding(text: str, model: str = "BAAI/bge-m3"):
    """Get embedding from SiliconFlow.

    API key is read from environment variable SILICONFLOW_API_KEY.
    Base URL can be overridden with SILICONFLOW_BASE_URL (defaults to
    https://api.siliconflow.cn/v1).
    """

    url = f"{os.getenv('SILICONFLOW_BASE_URL', DEFAULT_SILICONFLOW_BASE_URL)}/embeddings"
    api_key = os.getenv("SILICONFLOW_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Missing SiliconFlow API key. Please set environment variable SILICONFLOW_API_KEY."
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {"input": text, "model": model}
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    # SiliconFlow returns: {"data": [{"embedding": [...] , ...}], ...}
    return data["data"][0]["embedding"]
