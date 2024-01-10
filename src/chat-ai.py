import asyncio
import os
from openai import (
    AsyncOpenAI,
    RateLimitError,
)
import dotenv

dotenv.load_dotenv("../.env")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


client = AsyncOpenAI(
    api_key=OPENAI_API_KEY
)


async def main():
    try:
        request = "Ты умеешь писать на испанском?"
        print(request)
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": request,
                }
            ],
            model="gpt-3.5-turbo",
        )
        response = chat_completion.choices[0].message.content
        print(response)

    except RateLimitError as e:
        print(e.message)

asyncio.run(main())
