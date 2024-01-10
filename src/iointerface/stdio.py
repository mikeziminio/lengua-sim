import sys
import asyncio
from iointerface import AbstractIOInterface, InputMessage, OutputMessage
from simulator.enums import SimulatorMode, SimulatorCommand

__all__ = [
    "StdIO"
]


class StdIO(AbstractIOInterface):

    def __async_std_input(self):
        return (asyncio.get_event_loop()
                .run_in_executor(None, sys.stdin.readline))

    async def input(self) -> InputMessage:
        s = (await self.__async_std_input()).strip()
        match s:
            case "/c":
                return InputMessage(new_simulator_mode=SimulatorMode.CORRECT)
            case "/cn":
                return InputMessage(new_simulator_mode=SimulatorMode.CORRECT_WITH_NATIVE)
            case "/ca":
                return InputMessage(new_simulator_mode=SimulatorMode.CORRECT_AND_ANSWER)
            case "/can":
                return InputMessage(new_simulator_mode=SimulatorMode.CORRECT_AND_ANSWER_WITH_NATIVE)
            case "/a":
                return InputMessage(new_simulator_mode=SimulatorMode.ANSWER)
            case "/an":
                return InputMessage(new_simulator_mode=SimulatorMode.ANSWER_WITH_NATIVE)
            case "/raw":
                return InputMessage(new_simulator_mode=SimulatorMode.RAW)
            case "/help":
                return InputMessage(command=SimulatorCommand.OUTPUT_HELP)
            case "/exit":
                return InputMessage(command=SimulatorCommand.EXIT)
            case _:
                return InputMessage(text_content=s)

    def __async_std_output(self, output_s: str):
        return (asyncio.get_event_loop()
                .run_in_executor(None, lambda s=output_s: sys.stdout.write(s)))

    async def output(self, message: OutputMessage) -> None:
        if message.command is not None:
            if message.command == SimulatorCommand.OUTPUT_HELP:
                await self.__async_std_output(
                    "/c       correct your phrase\n"
                    "/cn      correct your phrase, add a translation\n"
                    "/ca      correct your phrase and answer it\n"
                    "/can     correct your phrase and answer it, add a translation\n"
                    "/a       answer to raw request to AI without correction\n"
                    "/an      answer to raw request to AI without correction, add a translation\n"
                    "/target <lan>    change target language\n"
                    "/native <lan>    change native language\n"
                    "/help    print this help message\n"
                    "/exit    end the session of LenguaSim\n\n"
                )
        elif message.text_content is not None:
            await self.__async_std_output(message.text_content + "\n")
