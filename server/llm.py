from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class Annotation(BaseModel):
    command_output: List[str]
    comment: str


class Response(BaseModel):
    description: str
    diff: str
    annotations: List[Annotation]


class Backend(Enum):
    OLLAMA = "ollama"


class Llm:
    backend: Backend

    def __init__(self, backend: Backend):
        self.backend = backend

    def query(self, prompt: str) -> Optional[Response]:
        match self.backend:
            case Backend.OLLAMA:
                print(f"querying ollama with prompt: {prompt}")
                return self._ollama_query(prompt)

    def _ollama_query(self, prompt: str) -> Optional[Response]:
        from ollama import chat

        response = chat(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3.2",
            format=Response.model_json_schema(),
        )

        if response.message.content:
            response = Response.model_validate_json(response.message.content)
            return response
        return None
