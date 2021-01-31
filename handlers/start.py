from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from core import messages
from core.conf import dp
from core.storage import storage
from utils import get_ikb
from utils.decorators import Chats


async def clear_storage():
    await storage.clear()


async def greet_user(message: Message):
    await message.reply("Привет, я бот-ведущий для игры в 'Правда или правда'")


async def start_collecting_for_new_game(message: Message):
    await message.reply(messages.NEW_GAME.format(0),
                        reply_markup=get_ikb({"text": "Присоединиться", "callback_data": "join_game"}))


@dp.message_handler(CommandStart())
@Chats.only_group_chat
async def handle_start(message: Message, *args, **kwargs):
    await clear_storage()
    await greet_user(message)
    await start_collecting_for_new_game(message)
