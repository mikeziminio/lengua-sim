import asyncio
from typing import Type
from aichat import AbstractAIChat
from iointerface import AbstractIOInterface, OutputMessage
from simulator.enums import SimulatorMode, SimulatorCommand

__all__ = [
    "Simulator",
]


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

    def generate_ai_text_request(self, request: str) -> str:
        """
        Из фразы пользователя создает запрос в ИИ чат
        (в зависимости от текущего режима симулятора).
        :param request: запрос пользователя
        :return: сгенерированный запрос в ИИ чат
        """
        result_json_head = (
            f"Phrase I want to say in {self.target_language} language: \"{request}\". "
            f"Give me back json with variables:\n"
        )
        result_json_items = {
            "correction": f"corrected phrase on {self.target_language} language",
            "correction_native": f"the same on {self.native_language} language",
            "answer": f"the text of the response to this phrase (from 1 to 30 words), if a human answered",
            "answer_native": f"the same on {self.native_language} language",
        }

        def make_result(*keys) -> str:
            result = result_json_head
            for key in keys:
                result += f"\"{key}\": {result_json_items[key]}.\n"
            return result

        match self.mode:
            case SimulatorMode.RAW:
                return request
            case SimulatorMode.CORRECT:
                return make_result("correction")
            case SimulatorMode.CORRECT_WITH_NATIVE:
                return make_result("correction", "correction_native")
            case SimulatorMode.CORRECT_AND_ANSWER:
                return make_result("correction", "answer")
            case SimulatorMode.CORRECT_AND_ANSWER_WITH_NATIVE:
                return make_result("correction", "correction_native", "answer", "answer_native")
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
                text_request = self.generate_ai_text_request(request.text_content)
                text_response = await self.ai_chat.send_text_message(text_request)
                # text_response = text_request
                output_message = OutputMessage(text_content=text_response)
                await self.io_interface.output(output_message)
            else:
                raise Exception("Неизвестный ответ")
