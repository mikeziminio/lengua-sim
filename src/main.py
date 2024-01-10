import asyncio
import dotenv
from chatai import ChatAI, ChatAIMessageMode

target_language = "Español"
native_language = "Русский"

dotenv.load_dotenv("../.env")

chatai = ChatAI(target_language, native_language)


async def main():
    while True:
        request = input()
        if request == "exit":
            break
        response = await chatai.send_message(request, ChatAIMessageMode.CORRECT_ME)
        print(response)


asyncio.run(main())
