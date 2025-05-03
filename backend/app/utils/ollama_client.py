# backend/app/utils/ollama_client.py
import requests
from backend.app.core.config import settings # Import settings from core config using absolute path

def generate_text_with_ollama(prompt: str, model: str = "llama2"):
    """
    Sends a prompt to the Ollama AI service to generate text.

    Args:
        prompt: The text prompt for the AI.
        model: The Ollama model to use (default is 'llama2').

    Returns:
        The JSON response from Ollama, or None if the request fails.
    """
    url = f"{settings.OLLAMA_ENDPOINT}/api/generate"
    payload = {"model": model, "prompt": prompt}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response
    except requests.exceptions.RequestException as e:
        # Log the error or handle it appropriately
        print(f"Error calling Ollama at {url}: {e}")
        return None
