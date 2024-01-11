import asyncio
from typing import Type
import json
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
    partner: str

    mode: SimulatorMode

    def __init__(
            self,
            ai_chat_class: type[AbstractAIChat],
            io_interface_class: type[AbstractIOInterface],
            target_language: str,
            native_language: str,
            partner: str,
            mode: SimulatorMode
    ):
        self.ai_chat = ai_chat_class()
        self.io_interface = io_interface_class()
        self.target_language = target_language
        self.native_language = native_language
        self.partner = partner
        self.mode = mode

    def generate_ai_text_request(self, request: str) -> str:
        """
        Из фразы пользователя создает запрос в ИИ чат
        (в зависимости от текущего режима симулятора).
        :param request: запрос пользователя
        :return: сгенерированный запрос в ИИ чат
        """
        result_json_items = {
            "native": (
                      f"translated text of that phrase (from {self.target_language} or other language) "
                      f"to {self.native_language}"
            ),
            "correction": f"corrected text of that phrase in {self.target_language} language",
            "correction_native": f"the same in {self.native_language} language",
            "answer": (
                      f"imagine that the {self.partner} had a dialogue with me, "
                      f"come up with the text of they first-person response to this phrase of mine "
                      f"(from 1 to 20 words in {self.target_language} language)"
            ),
            "answer_native": f"the same in {self.native_language} language",
        }

        def make_result(*keys) -> str:
            result_json_head = (
                f"Phrase: \"{request}\". "
                f"Give me back the json with {len(keys)} {'properties' if len(keys) > 1 else 'property'}:\n"
            )
            result = result_json_head
            for key in keys:
                result += f"\"{key}\": {result_json_items[key]}.\n"
            return result

        match self.mode:
            case SimulatorMode.TO_NATIVE:
                return make_result("native")
            case SimulatorMode.CORRECT:
                return make_result("correction")
            case SimulatorMode.CORRECT_WITH_NATIVE:
                return make_result("correction", "correction_native")
            case SimulatorMode.CORRECT_AND_ANSWER:
                return make_result("correction", "answer")
            case SimulatorMode.CORRECT_AND_ANSWER_WITH_NATIVE:
                return make_result("correction", "correction_native", "answer", "answer_native")
            case SimulatorMode.ANSWER:
                return make_result("answer")
            case SimulatorMode.ANSWER_WITH_NATIVE:
                return make_result("answer", "answer_native")
            case _:
                raise Exception("Неизвестный режим")
                # TODO: добавить исключение

    def ai_response_to_text(self, ai_response: str) -> str:
        s = ""
        d = json.loads(ai_response)
        # TODO: try-except
        for key, value in d.items():
            s += f"{key}: {value}\n"
        return s

    async def run(self):
        while True:
            message = await self.io_interface.input()
            if message.command is not None:
                match message.command:
                    case SimulatorCommand.CHANGE_TARGET_LANGUAGE:
                        self.target_language = message.command_param
                    case SimulatorCommand.CHANGE_NATIVE_LANGUAGE:
                        self.native_language = message.command_param
                    case SimulatorCommand.CHANGE_PARTNER:
                        self.partner = message.command_param
                    case SimulatorCommand.OUTPUT_PARAMS:
                        simulator_params = {
                            "target_language": self.target_language,
                            "native_language": self.native_language,
                            "partner": self.partner,
                            "mode": self.mode.name
                        }.__repr__()
                        output_message = OutputMessage(text_content=simulator_params)
                        await self.io_interface.output(output_message)
                    case SimulatorCommand.OUTPUT_HELP:
                        output_message = OutputMessage(command=SimulatorCommand.OUTPUT_HELP)
                        await self.io_interface.output(output_message)
                    case SimulatorCommand.EXIT:
                        break
            elif message.new_simulator_mode is not None:
                self.mode = message.new_simulator_mode
            elif message.text_content is not None:
                text_request = self.generate_ai_text_request(message.text_content)
                ai_response = await self.ai_chat.send_text_message(text_request)
                text_response = self.ai_response_to_text(ai_response)
                output_message = OutputMessage(text_content=text_response)
                await self.io_interface.output(output_message)
            else:
                raise Exception("Неизвестный ответ")
