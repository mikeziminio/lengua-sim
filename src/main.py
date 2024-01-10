import asyncio
import dotenv
from simulator import Simulator, SimulatorMode
from aichat.openaichat import OpenAIChat
from iointerface.stdio import StdIO

target_language = "Español"
native_language = "Русский"

dotenv.load_dotenv("../.env")


async def main():
    simulator = Simulator(
        OpenAIChat,
        StdIO,
        target_language,
        native_language,
        SimulatorMode.CORRECT_ME_AND_ANSWER
    )
    await simulator.run()


asyncio.run(main())
