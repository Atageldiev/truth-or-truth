from random import choice

from aiogram.types import Message

from core.conf import dp, questions
from core.generators import gamers
from core.storage import storage
from utils.decorators import Chats
from utils.filters import get_command_filter

command_new_round_filter = get_command_filter("new_round")


async def pass_the_turn():
    """Passes the turn to the next player"""
    await storage.update({"player_whose_turn": await gamers.next()})


async def tell_whose_turn(message: Message):
    """Tells users whose turn is now"""
    await message.answer(f"Сейчас отвечает:{await storage.get('player_whose_turn')}")


async def send_question(message: Message):
    """Sends the randomly generated question"""
    await message.answer(f"Вопрос: {choice(questions)}\n\n/new_round для начла нового раунда")


async def not_enough_gamers() -> bool:
    """Checks if there are enough gamers to start new round"""
    return not await storage.get_or_create("gamers", [])


async def tell_not_enough_gamers(message: Message):
    await message.answer("Недостаточно игроков!\nНабор в игру по команде /start")


@dp.message_handler(command_new_round_filter)
@Chats.only_group_chat
async def handle_new_round(message: Message, *args, **kwargs):
    if await not_enough_gamers():
        return await tell_not_enough_gamers(message)

    await pass_the_turn()
    await tell_whose_turn(message)
    await send_question(message)


@dp.message_handler(command_new_round_filter)
async def handle_new_round(message: Message):
    await message.reply("Команда работает только в группах")
