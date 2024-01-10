from enum import Enum, auto
import asyncio
from typing import Type
from aichat import AbstractAIChat
from iointerface import AbstractIOInterface, OutputMessage

__all__ = [
    "SimulatorMode",
    "SimulatorCommand",
    "Simulator",
]


class SimulatorMode(Enum):
    RAW = auto()
    CORRECT_ME = auto()
    CORRECT_ME_AND_ANSWER = auto()


class SimulatorCommand(Enum):
    EXIT = auto()


class Simulator:

    ai_chat: AbstractAIChat
    io_interface: AbstractIOInterface

    target_language: str
    native_language: str
    mode: SimulatorMode

    def __init__(
            self,
            ai_chat_class: type[AbstractAIChat],
            io_interface_class: type[AbstractIOInterface],
            target_language: str,
            native_language: str,
            mode: SimulatorMode
    ):
        self.ai_chat = ai_chat_class()
        self.io_interface = io_interface_class()
        self.target_language = target_language
        self.native_language = native_language
        self.mode = mode

    def process_request(self, request: str, mode: SimulatorMode = SimulatorMode.RAW):
        match mode:
            case SimulatorMode.RAW:
                return request
            case SimulatorMode.CORRECT_ME:
                result = (f"Correct the phrase in {self.target_language} language: \"{request}\". " +
                          f"In the response, just write the corrected phrase on {self.target_language}")
                return result
            case _:
                raise Exception("Неизвестный режим")
                # TODO: добавить исключение

    async def run(self):
        while True:
            request = await self.io_interface.input()
            if request.command is not None:
                if request.command == SimulatorCommand.EXIT:
                    break
            elif request.new_simulator_mode is not None:
                self.mode = request.new_simulator_mode
            elif request.text_content is not None:
                text_response = await self.ai_chat.send_text_message(request.text_content)
                output_message = OutputMessage(text_content=text_response)
                await self.io_interface.output(output_message)
            else:
                raise Exception("Неизвестный ответ")
