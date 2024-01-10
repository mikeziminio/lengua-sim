import sys
import asyncio
from iointerface.abstract import AbstractIOInterface, SimulatorMode


class StdIO(AbstractIOInterface):

    async def input(self) -> str | SimulatorMode:
        s = await (
            asyncio.get_event_loop()
            .run_in_executor(None, sys.stdin.readline)
        )
        match s:
            case "/cm":
                return SimulatorMode.CORRECT_ME
            case "/cma":
                return SimulatorMode.CORRECT_ME_AND_ANSWER
            case "/raw":
                return SimulatorMode.RAW
            case _:
                return s

    async def text_output(self, content: str) -> None:
        await (
            asyncio.get_event_loop()
            .run_in_executor(None, lambda s=content: sys.stdout.write(s))
        )
