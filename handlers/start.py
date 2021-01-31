from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from core.conf import dp, db
from utils import filters
from utils.buttons import get_ikb
from utils.decorators import check_existance
from utils.filters import get_command_filter

command_filter = get_command_filter("start")


@dp.message_handler(command_filter, filters.is_supergroup, state="*")
@check_existance("chats")
async def handle_start(message: Message, state: FSMContext, *args, **kwargs):
    db.chats.reset()
    await message.reply("Привет, я бот-ведущий для игры в 'Правда или правда'")
    await message.reply("Начат набор в новую игру\n\n"
                        "/new_round для начала нового раунда\n\n"
                        "В игре: ",
                        reply_markup=get_ikb({"text": "Присоединиться", "callback_data": "join_game"}))


@dp.message_handler(command_filter, filters.is_not_supergroup)
async def handle_start(message: Message):
    await message.reply("Команда работает только в группах")
