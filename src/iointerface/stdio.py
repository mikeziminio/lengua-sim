import sys
import asyncio
from iointerface import AbstractIOInterface, InputMessage, OutputMessage
from simulator import SimulatorMode, SimulatorCommand

__all__ = [
    "StdIO"
]


class StdIO(AbstractIOInterface):

    async def input(self) -> InputMessage:
        s = await (
            asyncio.get_event_loop()
            .run_in_executor(None, sys.stdin.readline)
        )
        match s:
            case "/cm":
                return InputMessage(new_simulator_mode=SimulatorMode.CORRECT_ME)
            case "/cma":
                return InputMessage(new_simulator_mode=SimulatorMode.CORRECT_ME_AND_ANSWER)
            case "/raw":
                return InputMessage(new_simulator_mode=SimulatorMode.RAW)
            case "/exit":
                return InputMessage(command=SimulatorCommand.EXIT)
            case _:
                return InputMessage(text_content=s)

    async def output(self, message: OutputMessage) -> None:
        if message.text_content is not None:
            await (
                asyncio.get_event_loop()
                .run_in_executor(None, lambda s=message.text_content: sys.stdout.write(s))
            )
