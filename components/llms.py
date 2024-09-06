from typing import Dict
from llama_index.core.llms import LLM
from llama_index.llms.openai import OpenAI

_llm_token_limits: Dict[str, int] = {
    'gpt-4o': 4096,
    'gpt-4o-mini': 4096,
}


def load_llm(model: str = 'gpt-4o-mini', temperature: float = 0.2, **kwargs) -> LLM:
    """
    Load and configure an LLM model.

    Args:
        model (str): The name of the model to load. Defaults to 'gpt-4o-mini'.
        temperature (float): The temperature setting for the model. Defaults to 0.2.
        **kwargs: Additional keyword arguments to pass to the OpenAI constructor.

    Returns:
        LLM: The configured LLM instance.

    Raises:
        ValueError: If the model is not configured or if invalid parameters are provided.
        RequestException: If there's an issue with the API request.
        Exception: For any other unexpected errors.
    """
    try:
        if model not in _llm_token_limits:
            raise ValueError(
                f"Model '{model}' is not configured. "
                f"Please use one of the following: {', '.join(_llm_token_limits.keys())}"
            )

        if not 0 <= temperature <= 1:
            raise ValueError("Temperature must be between 0 and 1.")

        llm = OpenAI(
            model=model,
            temperature=temperature,
            max_tokens=_llm_token_limits[model],
            request_timeout=120,
            seed=42,
            **kwargs
        )
        return llm

    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}") from e
