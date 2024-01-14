from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from simulator.enums import SimulatorMode, SimulatorCommand
from asyncio.tasks import Task

__all__ = [
    "InputMessage",
    "OutputMessage",
    "AbstractIOInterface",
]

MessageContext = TypeVar("MessageContext")


class InputMessage(Generic[MessageContext]):
    text_content: str | None
    simulator_mode: SimulatorMode | None
    is_inline_simulator_mode: bool
    command: SimulatorCommand | None
    command_param: str | None
    context: MessageContext | None

    def __init__(
            self,
            *,
            text_content: str | None = None,
            simulator_mode: SimulatorMode | None = None,
            is_inline_simulator_mode: bool = False,
            command: SimulatorCommand | None = None,
            command_param: str | None = None,
            context: MessageContext | None = None,
    ):
        super().__init__()
        self.text_content = text_content
        self.simulator_mode = simulator_mode
        self.is_inline_simulator_mode = is_inline_simulator_mode
        self.command = command
        self.command_param = command_param
        self.context = context


class OutputMessage(Generic[MessageContext]):
    text_content: str
    command: SimulatorCommand | None
    context: MessageContext

    def __init__(
            self,
            *,
            text_content: str | None = None,
            command: SimulatorCommand | None = None,
            context: MessageContext = None,
    ):
        super().__init__()
        self.text_content = text_content
        self.command = command
        self.context = context


class AbstractIOInterface(ABC, Generic[MessageContext]):
    """
    Абстрактный класс ввода-вывода
    """

    @abstractmethod
    def get_inner_task(self) -> Task | None:
        """
        Выполняется асинхронно сразу же после создания экземпляра класса
        :return:
        """
        ...

    @abstractmethod
    async def input(self) -> InputMessage[MessageContext]:
        """
        Получение от пользователя входящего сообщения (InputMessage)
        Это могут быть текст, новый режим работы симулятора, команды симулятора
        """
        ...

    @abstractmethod
    async def output(self, message: OutputMessage[MessageContext]) -> None:
        """
        Отправка пользователю исходящего сообщения
        """
        ...
