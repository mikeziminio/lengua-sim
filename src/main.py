import asyncio
import dotenv
from simulator import Simulator, SimulatorMode
from aichat.openaichat import OpenAIChat
from iointerface.stdio import StdIO

target_language = "Ukrainian"
native_language = "Russian"
partner = "украинская жена"

dotenv.load_dotenv("../.env")


async def main():
    simulator = Simulator(
        OpenAIChat,
        StdIO,
        target_language,
        native_language,
        partner,
        SimulatorMode.ANSWER
    )
    await simulator.run()


asyncio.run(main())
