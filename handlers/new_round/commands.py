from aiogram.types import Message

from core.conf import dp, db
from utils import filters
from utils.decorators import check_existance
from utils.filters import get_command_filter
from utils.game import give_question, pass_the_turn

command_filter = get_command_filter("new_round")


@dp.message_handler(command_filter, filters.is_supergroup)
@check_existance("chats")
async def new_round(message: Message, *args, **kwargs):
    if not db.chats.get_list("gamers"):
        return await message.answer("Недостаточно игроков!\nНабор в игру по команде /start")

    if not db.chats["rate_question"]:
        return await message.answer("Для начала нужно оценить предыдущий ответ!\nНажмите кнопку 'ответ получен'")

    db.chats["next_question_chosen"] = False
    db.chats["previous_question_chosen"] = False

    pass_the_turn()
    await message.answer(f"Сейчас отвечает:{db.chats['player_whose_turn']}")
    await give_question(message)


@dp.message_handler(command_filter)
async def handle_new_round_not_group(message: Message):
    await message.reply("Команда работает только в группах")
