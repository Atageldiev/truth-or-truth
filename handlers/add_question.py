from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from core.conf import dp, bot, db, ADMIN_ID
from core.states import AddQuestionStates
from utils.decorators import check_existance, Chats
from utils.filters import get_command_filter

command_add_question_filter = get_command_filter("add_question")


@dp.message_handler(command_add_question_filter)
@check_existance("rating")
@Chats.only_private_chat
async def handle_add_question(message: Message, state: FSMContext, *args, **kwargs):
    await message.answer("Напишите вопрос который хотите добавить")
    await state.set_state(AddQuestionStates.SEND_QUESTION)


async def question_exists(question):
    return db.custom_questions.exists(question)


async def add_question_to_db(question):
    db.custom_questions.add(question)


async def tell_successfull_addition(message: Message):
    await message.answer(
        "Твой вопрос успешно добавлен в базу данных пользовательских вопросов\n\n"
        "Мой отец в ближайшем времени проведет его через модерацию и добавит в основную базу\n\n"
        "(C) Отец бота @t2elzeth: <em> Благодарю </em>")


async def notify_admin():
    await bot.send_message(chat_id=ADMIN_ID, text="Батя, у тебя там новый вопрос в базе на модерацию")


@dp.message_handler(state=AddQuestionStates.SEND_QUESTION)
async def handle_add_question(message: Message, state: FSMContext):
    question = message.text
    if not await question_exists(question):
        await add_question_to_db(question)
        await notify_admin()

    await tell_successfull_addition(message)
    await state.reset_state()
