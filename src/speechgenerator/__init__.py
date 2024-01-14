from abc import ABC, abstractmethod
from enum import Enum


class SpeechGeneratorLang(Enum):
    SPANISH = "es-ES"
    RUSSIAN = "ru-RU"
    ENGLISH = "en-US"


class SpeechGenerator(ABC):

    @abstractmethod
    async def text_to_speech(self, text: str, lang: SpeechGeneratorLang):
        ...
