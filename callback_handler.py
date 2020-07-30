# import from loader
from loader import db

# import from my custom files
from mymodule import give_question, rate_answer_results, buttons

# import from other libraries
from time import sleep


async def join_game(callback_query):
    chat_id = callback_query.message.chat.id
    name = callback_query.from_user.first_name
    user_id = callback_query.from_user.id

    gamers = db.get_value(name="gamers", table="chats", chat_id=chat_id)
    gamers_user_id = db.get_value(name="gamers_user_id", table="chats", chat_id=chat_id)

    db.user_id_exists(chat_id=chat_id, user_id=user_id, name=name)

    if name not in db.get_list("gamers", chat_id):

        db.update_value(name="gamers", value=gamers + name +
                        ";", table='chats', chat_id=chat_id)
        db.update_value(name="gamers_user_id", value=gamers_user_id +
                        str(user_id) + ";", table='chats', chat_id=chat_id)

        await callback_query.answer("Ты успешно присоединился к игре")
    else:
        await callback_query.answer("Ты уже в игре")

    players = ""
    for name in db.get_list("gamers", chat_id):
        players += name + ", "

    try:
        await callback_query.message.edit_text(f"<b>Начат набор в новую игру</b>\n\n<em>/new_round</em> для начала нового раунда\n\n<u><b>В игре</b></u>:   <b><em>{players}</em></b>", reply_markup=buttons("Присоединиться", "join_game"))
    except:
        pass


async def got_answer(callback_query):
    chat_id = callback_query.message.chat.id
    name = callback_query.from_user.first_name
    message = callback_query.message
    player = db.get_value("player_whose_turn", "chats", message.chat.id)
    if name != db.get_value("player_whose_turn", table='chats', chat_id=chat_id):
        if db.get_value(name="got_answer_pressed", table="chats", chat_id=chat_id) == False:
            db.update_value(name="got_answer_pressed", value=True,
                            table="chats", chat_id=chat_id)

            await message.answer(f"<b>Оцени ответ игрока </b><em><u>{player}</u></em>", reply_markup=buttons("❤️;💔", "satisfied;not_satisfied"))
            await message.answer("<em>Результаты голосования будут через 15 секунд</em>")

            sleep(15)

            await rate_answer_results(message)
        else:
            await callback_query.answer("Я уже была нажата!")
    else:
        await callback_query.answer("Эта кнопка предназначена не для тебя")


async def rate_answer(callback_query):
    chat_id = callback_query.message.chat.id
    name = callback_query.from_user.first_name

    satisfied_players = db.get_value(name="satisfied_players", table="chats", chat_id=chat_id)
    not_satisfied_players = db.get_value(name="not_satisfied_players", table="chats", chat_id=chat_id)
    pressed_satisfied_users = db.get_value(name="pressed_satisfied_users", table="chats", chat_id=chat_id)
    pressed_not_satisfied_users = db.get_value(name="pressed_not_satisfied_users", table="chats", chat_id=chat_id)

    if name != db.get_value(name="player_whose_turn", table="chats", chat_id=chat_id):
        if name not in db.get_list("pressed_satisfied_users", chat_id) and name not in db.get_list("pressed_not_satisfied_users", chat_id):
            if callback_query.data == "satisfied":
                db.update_value(name="satisfied_players", value=satisfied_players + 1, table="chats", chat_id=chat_id)
                db.update_value(name="pressed_satisfied_users", value=pressed_satisfied_users + name + ";", table="chats", chat_id=chat_id)
            else:
                db.update_value(name="not_satisfied_players", value=not_satisfied_players + 1, table="chats", chat_id=chat_id)
                db.update_value(name="pressed_not_satisfied_users", value=pressed_not_satisfied_users + name + ";", table="chats", chat_id=chat_id)
        else:
            await callback_query.answer("Вы уже проголосовали!")
    else:
        await callback_query.answer("Эта кнопка предназначена не для тебя!")

    satisfied_players = str(db.get_value(name="satisfied_players", table="chats", chat_id=chat_id))
    not_satisfied_players = str(db.get_value(name="not_satisfied_players", table="chats", chat_id=chat_id))

    await callback_query.message.edit_reply_markup(reply_markup=buttons(text=f"{satisfied_players}❤️;{not_satisfied_players}💔",
                                                                        call="satisfied;not_satisfied"))


async def next_or_prev_q(callback_query):
    chat_id = callback_query.message.chat.id
    if db.get_value(name="player_whose_turn", table="chats", chat_id=chat_id) != callback_query.from_user.first_name:

        if db.get_value(name="next_question_chosen", table="chats", chat_id=chat_id) == False and db.get_value(name="previous_question_chosen", table="chats", chat_id=chat_id) == False:
            if callback_query.data == "next_question":
                await callback_query.message.answer("<b>Было выбрано продолжать</b>\n\nЖду команду <em>/new_round</em>")

                db.update_value(name="next_question_chosen",
                                value=True, table="chats")

            else:
                db.update_value(name="previous_question_chosen",
                                value=True, table="chats", chat_id=chat_id)
                await give_question(callback_query.message)

        else:
            await callback_query.answer("Вариант уже был выбран")
    else:
        await callback_query.answer("Эта кнопка предназначена не для тебя")

