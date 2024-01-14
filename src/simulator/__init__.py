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
                      f"considering they and my previous remarks"
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

    async def main_loop(self):
        while True:
            input_message = await self.io_interface.input()
            print(vars(input_message))
            if input_message.command is not None:
                match input_message.command:
                    case SimulatorCommand.CHANGE_TARGET_LANGUAGE:
                        self.target_language = input_message.command_param
                    case SimulatorCommand.CHANGE_NATIVE_LANGUAGE:
                        self.native_language = input_message.command_param
                    case SimulatorCommand.CHANGE_PARTNER:
                        self.partner = input_message.command_param
                    case SimulatorCommand.OUTPUT_PARAMS:
                        simulator_params = {
                            "target_language": self.target_language,
                            "native_language": self.native_language,
                            "partner": self.partner,
                            "mode": self.mode.name
                        }.__repr__()
                        output_message = OutputMessage(
                            text_content=simulator_params,
                            context=input_message.context,
                        )
                        await self.io_interface.output(output_message)
                    case SimulatorCommand.OUTPUT_HELP:
                        output_message = OutputMessage(
                            command=SimulatorCommand.OUTPUT_HELP,
                            context=input_message.context,
                        )
                        await self.io_interface.output(output_message)
                    case SimulatorCommand.EXIT:
                        break
            elif input_message.simulator_mode is not None:
                self.mode = input_message.simulator_mode
            elif input_message.text_content is not None:
                text_request = self.generate_ai_text_request(input_message.text_content)
                ai_response = await self.ai_chat.send_text_message(text_request)
                text_response = self.ai_response_to_text(ai_response)
                # text_response = text_request
                output_message = OutputMessage(
                    text_content=text_response,
                    context=input_message.context,
                )
                await self.io_interface.output(output_message)
            else:
                raise Exception("Неизвестный ответ")

    async def run(self):
        tasks = set()
        main_task = asyncio.create_task(self.main_loop())
        print("after main task")
        tasks.add(main_task)
        io_interface_task = self.io_interface.get_inner_task()
        if io_interface_task is not None:
            tasks.add(io_interface_task)
        await asyncio.gather(*tasks)
