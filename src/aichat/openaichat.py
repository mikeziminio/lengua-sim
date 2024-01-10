import os
from openai import (
    AsyncOpenAI,
    RateLimitError,
)
from aichat.abstract import AbstractAIChat

__all__ = [
    "OpenAIChat"
]


class OpenAIChat(AbstractAIChat):
    """
    Имплементация ИИ чата - ChatGPT.
    Для успешной работы в переменной среды OPENAI_API_KEY должен находиться API ключ.
    """

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )

    async def send_text_message(self, content: str) -> str:
        try:
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": content,
                    }
                ],
                model="gpt-3.5-turbo",
            )
            response = chat_completion.choices[0].message.content
            return response

        except RateLimitError as e:
            print(e.message)
            raise
            # TODO: обработать по другому
