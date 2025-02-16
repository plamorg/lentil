from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class Annotation(BaseModel):
    command_output: List[str]
    comment: str


class Response(BaseModel):
    summary: str
    description: str
    diff: str
    annotations: List[Annotation]


class Backend(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"


class Llm:
    backend: Backend

    def __init__(self, backend: Backend):
        self.backend = backend

    def query(self, prompt: str) -> Optional[Response]:
        match self.backend:
            case Backend.OLLAMA:
                return self._ollama_query(prompt)
            case Backend.OPENAI:
                return self._openai_query(prompt)

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

    def _openai_query(self, prompt: str) -> Optional[Response]:
        from openai import OpenAI

        client = OpenAI()

        response = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[{"role": "user", "content": prompt}],
            response_format=Response,
        )

        return response.choices[0].message.parsed
