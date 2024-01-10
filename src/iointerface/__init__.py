from abc import ABC, abstractmethod
from simulator.enums import SimulatorMode, SimulatorCommand

__all__ = [
    "InputMessage",
    "OutputMessage",
    "AbstractIOInterface",
]


class InputMessage:
    text_content: str | None
    new_simulator_mode: SimulatorMode | None
    command: SimulatorCommand | None

    def __init__(
            self,
            *,
            text_content: str | None = None,
            new_simulator_mode: SimulatorMode | None = None,
            command: SimulatorCommand | None = None
    ):
        self.text_content = text_content
        self.new_simulator_mode = new_simulator_mode
        self.command = command


class OutputMessage:
    text_content: str

    def __init__(
            self,
            *,
            text_content: str | None = None
    ):
        self.text_content = text_content


class AbstractIOInterface(ABC):
    """
    Абстрактный класс ввода-вывода
    """
    @abstractmethod
    async def input(self) -> InputMessage:
        """
        Получение от пользователя входящего сообщения (InputMessage)
        Это могут быть текст, новый режим работы симулятора, команды симулятора
        """
        ...

    @abstractmethod
    async def output(self, message: OutputMessage) -> None:
        """
        Отправка пользователю исходящего сообщения
        """
        ...

