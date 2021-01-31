from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from core.conf import dp, bot, db, ADMIN_ID
from core.states import AddQuestionStates
from utils.buttons import get_ikb
from utils.decorators import check_existance
from utils.filters import get_command_filter
from utils.filters import is_private, is_not_private

command_filter = get_command_filter("add_question")


@dp.message_handler(command_filter, is_private)
@check_existance("rating")
async def handle_add_question(message: Message, state: FSMContext, *args, **kwargs):
    await message.answer("Напишите вопрос который хотите добавить")
    await state.set_state(AddQuestionStates.SEND_QUESTION)


@dp.message_handler(command_filter, is_not_private)
async def handle_add_question(message: Message):
    await message.answer("Эта команда работает только в ЛС",
                         reply_markup=get_ikb({"text": "ЛС с ботом тут", "url": "https://t.me/truth_or_truth_bot"}))


@dp.message_handler(state=AddQuestionStates.SEND_QUESTION)
async def handle_add_question(message: Message, state: FSMContext):
    if not db.custom_questions.exists(message.text):
        db.custom_questions.add(message.text)
        await message.answer(
            "Твой вопрос успешно добавлен в базу данных пользовательских вопросов\n\n"
            "Мой отец в ближайшем времени проведет его через модерацию и добавит в основную базу\n\n"
            "(C) Отец бота @t2elzeth: <em> Благодарю </em>")
        await bot.send_message(chat_id=ADMIN_ID, text="Батя, у тебя там новый вопрос в базе на модерацию")
    else:
        await message.answer(
            "Спасибо что стараешься помочь мне развиваться\n"
            "/add_my_question чтобы добавить еще")
    await state.reset_state()
