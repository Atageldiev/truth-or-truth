from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageNotModified

from core import messages
from core.conf import dp
from core.generators import gamers
from core.storage import storage
from utils import get_ikb
from utils.decorators import check_existance


async def has_joined_the_game(call: CallbackQuery):
    return call.from_user.first_name in await storage.get_or_create("gamers", [])


async def add_new_gamer(first_name):
    gamers_list = await storage.get_or_create("gamers", [])
    gamers_list.append(first_name)
    await storage.update({"gamers": gamers_list})


async def regenerate_generator():
    await gamers.regenerate()


async def tell_successfull_joining(call: CallbackQuery):
    await call.answer("Ты успешно присоединился к игре")


async def stringified_gamers_list():
    return ', '.join(await storage.get_or_create("gamers", []))


async def edit_message(message: Message):
    try:
        await message.edit_text(messages.NEW_GAME.format(await stringified_gamers_list()),
                                reply_markup=get_ikb({"text": "Присоединиться", "callback_data": "join_game"}))
    except MessageNotModified:
        pass


@dp.callback_query_handler(text='join_game')
@check_existance("rating")
async def join_game(call: CallbackQuery, *args, **kwargs):
    if await has_joined_the_game(call):
        return await call.answer("Ты уже в игре")

    await add_new_gamer(call.from_user.first_name)
    await regenerate_generator()
    await tell_successfull_joining(call)
    await edit_message(call.message)
