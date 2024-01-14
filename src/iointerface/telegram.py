import sys
import io
import os
import asyncio
import threading
from asyncio import Future, Task
from typing import NamedTuple, Optional
import re
from aiogram import Bot, Dispatcher, Router
from aiogram.types import (
    Message,
    BotCommand,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
)
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.markdown import hbold, hitalic
from aiogram.methods import SetChatMenuButton
from iointerface import AbstractIOInterface, InputMessage, OutputMessage
from simulator.enums import SimulatorMode, SimulatorCommand

__all__ = [
    "TelegramBotIO"
]

dp = Dispatcher()


class MessageContext:
    """
    Контекст сообщения - передается между входящим и исходящим сообщением.
    В телеграм боте - здесь имеет смысл передавать chat_id
    """
    chat_id: int

    def __init__(self, *, chat_id: int):
        self.chat_id = chat_id


input_message_queue: list[InputMessage[MessageContext]] = []
input_future = Future[InputMessage[MessageContext]]()


def put_input_message_to_queue(input_message: InputMessage):
    input_message_queue.append(input_message)

    if not input_future.done():
        print("not input_future.done()")
        input_future.set_result(input_message_queue.pop())
        print(input_future.result())


class CommandTuple(NamedTuple):
    command: str
    param: str

    @classmethod
    def from_text(cls, text: str) -> Optional["CommandTuple"]:
        m = re.match(r"^/(\w*)\s*(.*?)\s*$", text)  # проверяет на шаблон "/команда параметр"
        if m is None:
            return None
        else:
            return CommandTuple(m[1], m[2])

# "target": "change target language",
# "native": "change native language",
# "partner": "change the dialogue partner:\n just enter a description of the character",

# "help": "print this help message",
# "params"


@dp.message(Command(commands=["target", "native", "partner"]))
async def message_handler(message: Message) -> None:
    ct = CommandTuple.from_text(message.text)
    if ct is None:
        Exception("Не команда")
        # TODO: переписать exception
    command, param = ct
    if command not in {"target", "native", "partner"}:
        raise Exception("")
        # TODO: переписать exception
    if not param:
        raise Exception("")
        # TODO: Придумать что сделать
    else:
        input_message = InputMessage(
            command=SimulatorCommand(command),
            command_param=param,
            context=MessageContext(
                chat_id=message.chat.id
            )
        )

    put_input_message_to_queue(input_message)


@dp.message(Command(commands=["n", "c", "cn", "ca", "can", "a", "an"]))
async def message_handler(message: Message) -> None:
    ct = CommandTuple.from_text(message.text)
    if ct is None:
        Exception("Не команда")
        # TODO: переписать exception
    command, param = ct
    if command not in {"n", "c", "cn", "ca", "can", "a", "an"}:
        raise Exception()
        # TODO: переписать exception
    if not param:
        input_message = InputMessage(
            simulator_mode=SimulatorMode(command),
            context=MessageContext(
                chat_id=message.chat.id
            )
        )
    else:
        input_message = InputMessage(
            simulator_mode=SimulatorMode(command),
            is_inline_simulator_mode=True,
            command_param=param,
            context=MessageContext(
                chat_id=message.chat.id
            )
        )

    put_input_message_to_queue(input_message)


@dp.message()
async def message_handler(message: Message) -> None:
    input_message = InputMessage(
        text_content=message.text,
        context=MessageContext(
            chat_id=message.chat.id
        )
    )
    put_input_message_to_queue(input_message)


class TelegramBotIO(AbstractIOInterface[MessageContext]):

    def __init__(self):
        self.bot = Bot(os.environ.get("TELEGRAM_BOT_TOKEN"), parse_mode=ParseMode.HTML)

    async def main_polling(self):
        commands = {
            "n": "translate your phrase to native language",
            "c": "correct your phrase",
            "cn": "correct your phrase, add a translation",
            "ca": "correct your phrase and answer it",
            "can": "correct your phrase and answer it, add a translation",
            "a": "answer to raw request to AI without correction",
            "an": "answer to raw request to AI without correction, add a translation",
            "target": "change target language",
            "native": "change native language",
            "partner": "change the dialogue partner:\n just enter a description of the character",
            "params": "current params",
            "help": "print this help message",
        }
        bot_commands = []
        for key, description in commands.items():
            bot_commands.append(BotCommand(
                command=key,
                description=description
            ))
        await self.bot.set_my_commands(bot_commands)
        await dp.start_polling(self.bot)

    def get_inner_task(self) -> Task | None:
        return asyncio.create_task(self.main_polling())

    def __get_future_input_message(self):
        global input_future
        input_future = Future[InputMessage[MessageContext]]()
        if len(input_message_queue) > 0:
            input_future.set_result(input_message_queue.pop())
        return input_future

    async def input(self) -> InputMessage[MessageContext]:
        print("input")
        return await self.__get_future_input_message()

    async def output(self, message: OutputMessage[MessageContext]) -> None:
        if message.command is not None:
            if message.command == SimulatorCommand.OUTPUT_HELP:
                help_message = (
                    "/n       translate your phrase to native language\n"
                    "/c       correct your phrase\n"
                    "/cn      correct your phrase, add a translation\n"
                    "/ca      correct your phrase and answer it\n"
                    "/can     correct your phrase and answer it, add a translation\n"
                    "/a       answer to raw request to AI without correction\n"
                    "/an      answer to raw request to AI without correction, add a translation\n"
                    "/target <lan>    change target language\n"
                    "/native <lan>    change native language\n"
                    "/partner <description>    change the dialogue partner:\n"
                    "                          just enter a description of the character\n"
                    "                          for example:\n"
                    "                              Albert Einstein\n"
                    "                              the old fisherman\n"
                    "                              ...\n"
                    "/params  print current params\n"
                    "/help    print this help message\n"
                    "/exit    end the session of LenguaSim\n\n"
                )
                await self.bot.send_message(
                    chat_id=message.context.chat_id,
                    text=help_message
                )
        elif message.text_content is not None:
            await self.bot.send_message(
                chat_id=message.context.chat_id,
                text=message.text_content
            )
