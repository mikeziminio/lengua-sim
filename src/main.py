import asyncio
import dotenv
from simulator import Simulator, SimulatorMode
from aichat.openaichat import OpenAIChat
from iointerface.stdio import StdIO
from iointerface.telegram import TelegramBotIO
from speechgenerator.google import GoogleSpeechGenerator

target_language = "Spanish"
native_language = "Russian"
partner = "Albert Einstein"

dotenv.load_dotenv("../.env")


async def main():
    simulator = Simulator(
        ai_chat_class=OpenAIChat,
        io_interface_class=TelegramBotIO,  # StdIO,
        speech_generator_class=GoogleSpeechGenerator,
        target_language=target_language,
        native_language=native_language,
        partner=partner,
        mode=SimulatorMode.ANSWER
    )
    await simulator.run()


asyncio.run(main())
