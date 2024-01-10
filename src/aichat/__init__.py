from abc import ABC, abstractmethod

__all__ = [
    "AbstractAIChat",
]

class AbstractAIChat(ABC):
    """
    Абстрактный класс чата ИИ, который может отвечать на вопросы, работать как ассистент.
    Важно, чтобы имплементация поддерживала изучаемые языки.
    """
    @abstractmethod
    async def send_text_message(self, content: str) -> str:
        """
        Отправка текстового сообщения в ИИ чат и получение текстового ответа
        """
        ...
