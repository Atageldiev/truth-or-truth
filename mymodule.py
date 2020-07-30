# import from aiogram
from aiogram import types

# import from my custom files
from loader import bot, db
from config import questions

# import from other libraries
from random import choice


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
    i = db.get_value(name="i", table="chats", chat_id=chat_id)

    try:
        player_whose_turn = db.get_list("gamers", chat_id)[i]
    except:
        db.update_value(name="i", value=0, table="chats", chat_id=chat_id)

    i = db.get_value("i", "chats", chat_id=chat_id)

    player_whose_turn = db.get_list("gamers", chat_id)[i]
    player_whose_turn_id = db.get_list("gamers_user_id", chat_id)[i]


    db.update_value(name="player_whose_turn", value=player_whose_turn, table="chats", chat_id=chat_id)

    db.update_value(name="player_whose_turn_id", value=player_whose_turn_id, table="chats", chat_id=chat_id)

    db.update_value(name="i", value=i+1, table="chats", chat_id=chat_id)


    return player_whose_turn


def on_startup():
    """Функции, которые будут вызваны при старте бота"""
    db.create_table()
    db.create_rating_table()
    db.create_table_of_questions()

def reset_db(chat_id):
    db.update_value(name="rate_question", value=True, table="chats", chat_id=chat_id)
    db.update_value(name="got_answer_pressed", value=False, table="chats", chat_id=chat_id)
    db.update_value(name="next_question_chosen", value=False, table="chats", chat_id=chat_id)
    db.update_value(name="previous_question_chosen", value=False, table="chats", chat_id=chat_id)
    db.update_value(name="satisfied_players", value=0, table="chats", chat_id=chat_id)
    db.update_value(name="not_satisfied_players", value=0, table="chats", chat_id=chat_id)
    db.update_value(name="pressed_satisfied_users", value="", table="chats", chat_id=chat_id)
    db.update_value(name="pressed_not_satisfied_users", value="", table="chats", chat_id=chat_id)
    db.update_value(name="gamers", value="", table="chats", chat_id=chat_id)
    db.update_value(name="gamers_user_id", value="", table="chats", chat_id=chat_id)
    db.update_value(name="i", value=0, table="chats", chat_id=chat_id)

async def rate_answer_results(message):
    chat_id = message.chat.id
    player = db.get_value(name="player_whose_turn", table="chats", chat_id=chat_id)
    player_whose_turn_id = db.get_value(name="player_whose_turn_id", table="chats", chat_id=chat_id)

    satisfied_players = str(db.get_value(name="satisfied_players", table="chats", chat_id=chat_id))
    not_satisfied_players = str(db.get_value(name="not_satisfied_players", table="chats", chat_id=chat_id))
    likes = str(db.get_value(name="likes", table="rating", chat_id=chat_id, user_id=player_whose_turn_id))
    dislikes=str(db.get_value(name="dislikes", table="rating", chat_id=chat_id, user_id=player_whose_turn_id))

    db.update_value(name="likes", value=likes + satisfied_players, table="rating", chat_id=chat_id, user_id=player_whose_turn_id)
    db.update_value(name="dislikes", value=dislikes + satisfied_players, table="rating", chat_id=chat_id, user_id=player_whose_turn_id)

    await message.answer(f"<b>Результаты: </b>\n❤️ - {satisfied_players}\n💔 - {not_satisfied_players}")

    if int(satisfied_players) > int(not_satisfied_players):
        await message.answer(f"<u><b>{player}</b></u>, твой ответ понравился большинству\n\nЖду команду /new_round")
        db.update_value(name="rate_question", value=True,
                        table="chats", chat_id=message.chat.id)

    elif int(satisfied_players) == int(not_satisfied_players):
        await message.answer(f"<u><b>{player}</b></u>, твой ответ понравился большинству\n\nЖду команду /new_round")
        db.update_value(name="rate_question", value=True, table="chats", chat_id=message.chat.id)

    else:
        await message.answer(f"<u><b>{player}</b></u>, твой ответ не понравился большинству\n\nЧто делать дальше?", reply_markup=buttons("Следующий вопрос;Перезадать предыдущий", "next_question;prev_question"))


async def give_question(message):
    chat_id = message.chat.id
    await message.answer(f"<b>Вопрос:</b> <em>{random_q(chat_id)}</em> ", reply_markup=buttons("Ответ получен!", "got_answer"))


    db.update_value(name="satisfied_players", value=0, table="chats", chat_id=chat_id)

    db.update_value(name="not_satisfied_players", value=0, table="chats", chat_id=chat_id)

    db.update_value(name="pressed_satisfied_users", value="", table="chats", chat_id=chat_id)

    db.update_value(name="pressed_not_satisfied_users", value="", table="chats", chat_id=chat_id)

    db.update_value(name="rate_question", value=False, table="chats", chat_id=message.chat.id)

    db.update_value(name="got_answer_pressed", value=False, table="chats", chat_id=message.chat.id)


async def game(message):
    await message.reply("<b>Начат набор в новую игру</b>\n\n<em>/new_round</em> для начала нового раунда\n\n<u><b>В игре:</b></u> ", reply_markup=buttons("Присоединиться", "join_game"))
    db.update_value(name="gamers", value="",
                    table="chats", chat_id=message.chat.id)
    db.update_value(name="gamers_user_id", value="",
                    table="chats", chat_id=message.chat.id)


async def answer(chat_id, text):
    return await bot.send_message(chat_id=chat_id, text=text)
