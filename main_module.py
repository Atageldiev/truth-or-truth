# import from aiogram
from aiogram import Bot, Dispatcher, types

# import from my custom files
from config import TOKEN, questions
from myclass import Sqlighter

# import from other libraries
from random import choice
from time import sleep

# Initialize bot and dispatcher
bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot)

# Create object for data base
db = Sqlighter()

def buttons(text, call):
    button = types.InlineKeyboardMarkup()
    text = text.split(";")
    call = call.split(";")
    for text, call in zip(text, call):
        button.add(types.InlineKeyboardButton(text=text, callback_data=call))
    return button

def random_q(chat_id):
    random_question = choice(questions)
    db.update_value(
                    name="current_question", 
                    value=random_question,
                    table="chats", 
                    chat_id=chat_id
    )
    return random_question

def turn(chat_id):
    i = db.get_value(name="i", value="chats", chat_id=chat_id)

    try:
        player_whose_turn = db.get_list("gamers", chat_id)[i]
    except:
        db.update_value(name="i", value=0, table="chats", chat_id=chat_id)

    i = db.get_value("i", "chats", chat_id=chat_id)

    player_whose_turn = db.get_list("gamers", chat_id)[i]
    player_whose_turn_id = db.get_list("gamers_user_id", chat_id)[i]

    db.update_value(name="player_whose_turn",
                    value=player_whose_turn, 
                    table="chats", 
                    chat_id=chat_id)
    db.update_value(name="player_whose_turn_id",
                    value=player_whose_turn_id, 
                    table="chats", 
                    chat_id=chat_id)
    db.update_value(name="i", 
                    value=i+1, 
                    table="chats", 
                    chat_id=chat_id)

    return player_whose_turn

def on_startup():
    """Функции, которые будут вызваны при старте бота"""
    db.create_table()
    db.create_rating_table()
    db.create_table_questions()

async def game(message):
    await message.reply("Начат набор в новую игру\n\n/new_round для начала нового раунда", reply_markup = buttons("Присоединиться", "join_game"))
    await message.answer("В игре: ")
    db.update_value(name="gamers", value="", table="chats", chat_id=message.chat.id)

async def give_question(message):
    chat_id = message.chat.id
    await message.answer("Вопрос: " + random_q(chat_id), reply_markup=buttons("Ответ получен!", "got_answer"))
    db.update_value(name="satisfied_players", 
                    value=0,
                    table="chats", 
                    chat_id=chat_id)

    db.update_value(name="not_satisfied_players", 
                    value=0,
                    table="chats", 
                    chat_id=chat_id)

    db.update_value(name="pressed_satisfied_users",
                    value="", 
                    table="chats", 
                    chat_id=chat_id)

    db.update_value(name="pressed_not_satisfied_users",
                    value="", 
                    table="chats", 
                    chat_id=chat_id)

    db.update_value(name="rate_question", 
                    value=False,
                    table="chats", 
                    chat_id=message.chat.id)

    db.update_value(name="got_answer_pressed", 
                    value=False, 
                    table="chats", 
                    chat_id=message.chat.id)


async def rate_question_results(message):
    chat_id = message.chat.id
    satisfied = db.get_value(name="satisfied_players", 
                                table="chats", 
                                chat_id=chat_id)
    not_satisfied = db.get_value(name="not_satisfied_players", 
                                table="chats", 
                                chat_id=chat_id)
    player = db.get_value(name="player_whose_turn", 
                                table="chats", 
                                chat_id=chat_id)

   

    await message.answer("<b>Результаты: </b>" + 
                        "\n❤️ - " + str(
                                        db.get_value(
                                                    name="satisfied_players", 
                                                    table="chats", 
                                                    chat_id=chat_id
                                                    )
                                                    
                                        ) + 
                        "\n💔 - " + str(
                                        db.get_value(
                                                    name="not_satisfied_players", 
                                                    table="chats", 
                                                    chat_id=chat_id
                                                    )
                                        )
    )
    
    if satisfied > not_satisfied:
        await message.answer(player + " твой ответ понравился большинству\n\nЖду команду /new_round")
        db.update_value(name="rate_question", value=True,
                        table="chats", chat_id=message.chat.id)

    elif satisfied == not_satisfied:
        await message.answer(player + " твой ответ понравился большинству\n\nЖду команду /new_round")
        db.update_value(name="rate_question", value=True,
                        table="chats", chat_id=message.chat.id)

    else:
        await message.answer(player + " твой ответ не понравился большинству\n\nЧто делать дальше?", reply_markup=buttons("Следующий вопрос;Перезадать предыдущий", "next_question;prev_question"))

async def new_round(message):
    chat_id = message.chat.id
    # markup = types.InlineKeyboardMarkup()
    # markup.add(types.InlineKeyboardButton(text="Ответить в лс➡️", url="https://t.me/truth_or_truth_bot", callback_data="give_answer"))
    if db.get_list("gamers", chat_id) != []:
        if db.get_value(name="rate_question", table="chats", chat_id=chat_id) == True:
            await message.answer("Сейчас отвечает: " + turn(message.chat.id))

            db.update_value(name="next_question_chosen", value=False, table="chats", chat_id=message.chat.id)
            db.update_value(name="previous_question_chosen", value=False, table="chats", chat_id=message.chat.id)

            await give_question(message)

        else:
            await message.answer("Для начала нужно оценить предыдущий ответ!\nНажмите кнопку 'ответ получен'")
    else:
        await message.answer("Недостаточно игроков!\nНабор в игру по команде /start")


async def got_answer_process(message):
    db.update_value(name="got_answer_pressed", value=True, table="chats", chat_id=message.chat.id)

    await message.answer("Оцени ответ игрока " + db.get_value("player_whose_turn", "chats", message.chat.id), reply_markup=buttons("❤️;💔", "satisfied;not_satisfied"))
    await message.answer("Результаты голосования будут через 15 секунд")

    sleep(15)

    await rate_question_results(message)
    
async def process_next_prev_q(callback_query):
    chat_id = callback_query.message.chat.id
    if db.get_value(name="player_whose_turn", table="chats", chat_id=chat_id) != callback_query.from_user.first_name:

        if db.get_value(name="next_question_chosen", table="chats", chat_id=chat_id) == False and db.get_value(name="previous_question_chosen", table="chats", chat_id=chat_id) == False:
            if callback_query.data == "next_question":
                await callback_query.message.answer("Было выбрано продолжать\n\nЖду команду /new_round")

                db.update_value(name="next_question_chosen", value=True, table="chats")

            else:
                db.update_value(name="previous_question_chosen",value=True, table="chats", chat_id=chat_id)
                await give_question(callback_query.message)

        else:
            await callback_query.answer("Вариант уже был выбран")
    else:
        await callback_query.answer("Эта кнопка предназначена не для тебя")




    
