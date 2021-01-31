from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from core.conf import dp
from utils.filters import get_command_filter

command_filter = get_command_filter("help")


@dp.message_handler(command_filter)
async def handle_help(message: Message, state: FSMContext):
    await message.answer("В разработке...")
