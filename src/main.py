import asyncio
import dotenv
from simulator import Simulator, SimulatorMode
from aichat.openaichat import OpenAIChat
from iointerface.stdio import StdIO

target_language = "Spanish"
native_language = "Russian"
partner = "human"

dotenv.load_dotenv("../.env")


async def main():
    simulator = Simulator(
        OpenAIChat,
        StdIO,
        target_language,
        native_language,
        partner,
        SimulatorMode.CORRECT_AND_ANSWER
    )
    await simulator.run()


asyncio.run(main())
