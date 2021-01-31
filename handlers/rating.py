from aiogram.types import Message

from core.conf import dp, db
from utils.filters import get_command_filter

command_rating_filter = get_command_filter("rating")


@dp.message_handler(command_rating_filter, lambda message: db.rating.all())
async def handle_rating(message: Message):
    await message.reply(f"{message.from_user.first_name}:\n "
                        f"    добавлено вопросов: {db.rating['added_questions_number']}\n\n")


@dp.message_handler(command_rating_filter, lambda message: not db.rating.all())
async def handle_rating(message: Message):
    await message.reply("В таблице рейтинга еще нет ни одного игрока\n\n"
                        "Для того чтобы туда добавиться, нужно хоть раз нажать кнопку 'Присоединиться' "
                        "или же добавить свой вопрос через команду /add_my_question")
