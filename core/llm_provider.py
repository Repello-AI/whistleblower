import os
import json
from typing import Optional, Tuple
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def chat_completion(self, messages: list, model: str, max_tokens: int = 512) -> str:
        pass

class OpenAIProvider(LLMProvider):
    """OpenAI provider implementation"""
    
    def __init__(self, api_key: str):
        from openai import OpenAI
        os.environ['OPENAI_API_KEY'] = api_key
        self.client = OpenAI()
    
    def chat_completion(self, messages: list, model: str, max_tokens: int = 512) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

class LiteLLMProvider(LLMProvider):
    """LiteLLM provider implementation"""
    
    def __init__(self, api_key: str = None):
        import litellm
        self.litellm = litellm
        if api_key:
            # Set API key for the specific provider
            # LiteLLM will automatically detect the provider from model name
            os.environ['OPENAI_API_KEY'] = api_key  # For OpenAI models
            # Add other provider keys as needed
            # os.environ['ANTHROPIC_API_KEY'] = api_key  # For Claude models
            # os.environ['GOOGLE_API_KEY'] = api_key     # For Gemini models
    
    def chat_completion(self, messages: list, model: str, max_tokens: int = 512) -> str:
        response = self.litellm.completion(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
        )
        # LiteLLM returns an OpenAI-compatible dict-like response
        return response["choices"][0]["message"]["content"]

def get_llm_provider(provider_type: str, api_key: str) -> LLMProvider:
    """Factory function to get the appropriate LLM provider"""
    if provider_type.lower() == "openai":
        return OpenAIProvider(api_key)
    elif provider_type.lower() == "litellm":
        return LiteLLMProvider(api_key)
    else:
        raise ValueError(f"Unsupported provider type: {provider_type}")