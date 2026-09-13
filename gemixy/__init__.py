import os
import sys
import json
from typing import List, Iterator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini.core import chat_with_gemini, messages_to_prompt


class GeminiClient:
    def __init__(self, base_url: str = None, api_key: str = "any"):
        self.base_url = base_url
        self.api_key = api_key

    def chat(self, message: str, model: str = "gemini", **kwargs) -> str:
        result = chat_with_gemini(message)
        if not result:
            raise RuntimeError("Gemini did not respond")
        return result

    def chat_stream(self, message: str, model: str = "gemini", **kwargs) -> Iterator[str]:
        result = chat_with_gemini(message)
        if not result:
            raise RuntimeError("Gemini did not respond")
        for word in result.split():
            yield word + " "

    def messages(self, messages: List[dict], model: str = "gemini", **kwargs) -> str:
        prompt = messages_to_prompt(messages)
        result = chat_with_gemini(prompt)
        if not result:
            raise RuntimeError("Gemini did not respond")
        return result

    def messages_stream(self, messages: List[dict], model: str = "gemini", **kwargs) -> Iterator[str]:
        prompt = messages_to_prompt(messages)
        result = chat_with_gemini(prompt)
        if not result:
            raise RuntimeError("Gemini did not respond")
        for word in result.split():
            yield word + " "

    def models(self) -> dict:
        return {
            "object": "list",
            "data": [
                {
                    "id": "gemini",
                    "object": "model",
                    "created": 1686935002,
                    "owned_by": "google"
                }
            ]
        }


client = GeminiClient()
