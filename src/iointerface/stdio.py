import sys
import io
import asyncio
import re
from asyncio import Task
from typing import TypeAlias
from iointerface import AbstractIOInterface, InputMessage, OutputMessage
from simulator.enums import SimulatorMode, SimulatorCommand

__all__ = [
    "StdIO"
]


MessageContext: TypeAlias = None


class StdIO(AbstractIOInterface[MessageContext]):

    def __init__(self):
        """
        Долго переписывал логику ввода-вывода в терминал, т.к. периодически валились ошибки.
        UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd0 in position 0: invalid continuation byte
        В итоге оказалось, что баг не в коде, а в терминале PyCharm.
        В обычном терминале ubuntu бага не наблюдается.
        Поэтому оставил крайнюю асинхронную реализацию. В PyCharm ошибка всё равно периодически валится.
        """
        self.__std_in = open(sys.stdin.fileno(), "r")
        self.__std_out = open(sys.stdout.fileno(), "w")

    def get_inner_task(self) -> Task | None:
        pass

    def __async_std_input(self):
        return (asyncio.get_event_loop()
                .run_in_executor(None, self.__std_in.readline))

    def __async_std_output(self, output_s: str):
        return (asyncio.get_event_loop()
                .run_in_executor(None, lambda s=output_s: self.__std_out.write(s)))

    async def input(self) -> InputMessage[MessageContext]:
        s = await self.__async_std_input()
        m = re.match(r"^/(\w*)\s*(.*?)\s*$", s)  # проверяет на шаблон "/команда параметр"
        if m is None:
            m = re.match(r"^(.*?)\s*$", s)
            return InputMessage(text_content=m[1])
        command, param = m[1], m[2]
        if command in {"n", "c", "cn", "ca", "can", "a", "an"}:
            return InputMessage(simulator_mode=SimulatorMode(command))
        else:
            match command:
                case "target":
                    return InputMessage(command=SimulatorCommand.CHANGE_TARGET_LANGUAGE, command_param=param)
                case "native":
                    return InputMessage(command=SimulatorCommand.CHANGE_NATIVE_LANGUAGE, command_param=param)
                case "partner":
                    return InputMessage(command=SimulatorCommand.CHANGE_PARTNER, command_param=param)
                case "params":
                    return InputMessage(command=SimulatorCommand.OUTPUT_PARAMS)
                case "help":
                    return InputMessage(command=SimulatorCommand.OUTPUT_HELP)
                case "exit":
                    return InputMessage(command=SimulatorCommand.EXIT)
                case _:
                    raise Exception("Неизвестная команда")
                    # TODO: переделать позднее

    async def output(self, message: OutputMessage) -> None:
        if message.command is not None:
            if message.command == SimulatorCommand.OUTPUT_HELP:
                await self.__async_std_output(
                    "/n       translate your phrase to native language\n"
                    "/c       correct your phrase\n"
                    "/cn      correct your phrase, add a translation\n"
                    "/ca      correct your phrase and answer it\n"
                    "/can     correct your phrase and answer it, add a translation\n"
                    "/a       answer to raw request to AI without correction\n"
                    "/an      answer to raw request to AI without correction, add a translation\n"
                    "/target <lan>    change target language\n"
                    "/native <lan>    change native language\n"
                    "/partner <description>    change the dialogue partner:\n"
                    "                          just enter a description of the character\n"
                    "                          for example:\n"
                    "                              Albert Einstein\n"
                    "                              the old fisherman\n"
                    "                              ...\n"
                    "/params  print current params\n"
                    "/help    print this help message\n"
                    "/exit    end the session of LenguaSim\n\n"
                )
        elif message.text_content is not None:
            await self.__async_std_output(message.text_content + "\n")
