from aiogram.types import Message

from core.conf import dp, db
from utils.filters import get_command_filter

command_filter = get_command_filter("rating")


@dp.message_handler(command_filter, lambda message: db.rating.all())
async def handle_rating(message: Message):
    first_name = message.from_user.first_name
    if db.rating["name"] != first_name:
        db.rating["name"] = first_name
    await message.reply(f"{first_name}:\n "
                        f"    лайков: {db.rating['likes']}\n"
                        f"    дизлайков: {db.rating['dislikes']}\n"
                        f"    добавлено вопросов: {db.rating['added_questions_number']}\n\n")


@dp.message_handler(command_filter, lambda message: not db.rating.all())
async def handle_rating(message: Message):
    await message.reply("В таблице рейтинга еще нет ни одного игрока\n\n"
                        "Для того чтобы туда добавиться, нужно хоть раз нажать кнопку 'Присоединиться' "
                        "или же добавить свой вопрос через команду /add_my_question")
