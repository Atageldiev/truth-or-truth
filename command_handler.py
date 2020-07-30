# import from aiogram
from aiogram import types

# import from my custom files
from loader import dp, db
from mymodule import turn, give_question, game, reset_db, answer
from config import ADMIN_ID
from utils import States

async def send_welcome(message):
    if message.chat.type != "private":

        await message.reply("<b>Привет, я бот-ведущий для игры в 'Правда или правда'</b>")
        await game(message)

        db.chat_exists(message.chat.id)
        reset_db(message.chat.id)
    else:
        await message.reply("<u><b>Команда работает только в группах</b></u>")


async def new_round(message):
    chat_id = message.chat.id
    if message.chat.type != "private":
        if db.get_list("gamers", chat_id) != []:
            if db.get_value(name="rate_question", table="chats", chat_id=chat_id) == True:
                await message.answer(f"<b>Сейчас отвечает: </b><em>{turn(message.chat.id)}</em>")

                db.update_value(name="next_question_chosen", value=False, table="chats", chat_id=message.chat.id)
                db.update_value(name="previous_question_chosen", value=False, table="chats", chat_id=message.chat.id)

                await give_question(message)

            else:
                await message.answer("<b>Для начала нужно оценить предыдущий ответ!</b>\nНажмите кнопку <em>'ответ получен'</em>")
        else:
            await message.answer("<b>Недостаточно игроков!</b>\nНабор в игру по команде <em>/start</em>")
    else:
        await message.reply("<u><b>Команда работает только в группах</b></u>")

# Начало функций для обработки команды /add_my_question
async def add_question(message):
    state = dp.current_state(user=message.from_user.id)
    db.user_id_exists(chat_id=message.chat.id, user_id=message.from_user.id, name=message.from_user.first_name)

    await state.set_state(States.all()[0])
    if message.chat.type == "private":

        await message.answer("<b>Напишите вопрос который хотите добавить</b>")

    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="ЛС с ботом тут", url="https://t.me/truth_or_truth_bot"))
        
        await message.answer("<u><b>Уууупс, эта команда работает только в ЛС</b></u>\n\nНу, а зачем всем знать какие вопросы их будут ожидать? :P\n\n<em>ЛС с ботом: </em>", reply_markup=markup)

async def add_into_db(message):
    state = dp.current_state(user=message.from_user.id)
    db.user_id_exists(chat_id=message.chat.id, user_id=message.from_user.id, name=message.from_user.first_name)
    if db.custom_question_exists(message.text) == False:

        await message.answer("<u><b>Твой вопрос успешно добавлен в базу данных пользовательских вопросов</b></u>\n\nМой отец в ближайшем времени проведет его через модерацию и добавит в основную базу\n\n(C) Отец бота @t2elzeth: <em> Благодарю</em>")
        await answer(chat_id=ADMIN_ID, text="<b>Батя, у тебя там новый вопрос в базе на модерацию</b>")
        await state.reset_state()

    else:
        await message.answer("<u><b>Такой вопрос был найден в базе</b></u>\n\nСпасибо что стараешься помочь мне развиваться\n\n/add_my_question чтобы добавить еще")
        await state.reset_state()
# Конец функций для обработки команды /add_my_question

async def send_rating(message):
    chat_id = message.chat.id
    rating_message = ""
    if db.get_user_ids(chat_id) != []:
        for user_id in db.get_user_ids(chat_id):
            user_id = user_id[0]
            name = db.get_value(name="name", table="rating",chat_id=chat_id, user_id=user_id)
            likes = str(db.get_value(name="likes", table="rating", chat_id=chat_id, user_id=user_id))
            dislikes=str(db.get_value(name="dislikes", table="rating", chat_id=chat_id, user_id=user_id))
            added_questions=str(db.get_value(name="added_questions_number", table="rating", chat_id=chat_id, user_id=user_id))

            rating_message += f"<u><b>{name}</b></u>:\n\
    <em>Лайков:</em> {likes}\n\
    <em>Дизлайков:</em> {dislikes}\n\
    <em>Добавлено вопросов:</em> {added_questions}\n\n"

        await message.reply(rating_message)

    else:
        await message.reply("<u><b>В таблице рейтинга еще нет ни одного игрока</b></u>\n\nДля того чтобы туда добавиться, нужно хоть раз нажать кнопку <em>'Присоединиться'</em> \
или же <u>добавить свой вопрос через команду</u> <em>/add_my_question</em>")
