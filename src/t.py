import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import (
    Message,
    BotCommand,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.markdown import hbold, hitalic
from aiogram.methods import SetChatMenuButton

TELEGRAM_BOT_TOKEN = ""

dp = Dispatcher()


@dp.message(Command("c"))
async def message_handler(message: Message) -> None:
    t = message.text
    await message.answer(
        text=f"{hbold('answer:')} Hola! Tu escribiste '{t}' with command 'c'",
    )


async def main() -> None:
    bot = Bot(TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
    await bot.set_my_commands([
        BotCommand(
            command="n",
            description="translate your phrase to native language"
        ),
        BotCommand(
            command="c",
            description="correct your phrase"
        ),
    ])

    await dp.start_polling(bot)

asyncio.run(main())




# await self.bot.send_message(
#     text="r",
#     chat_id=94211624,
#     reply_markup=ReplyKeyboardRemove()
# )

