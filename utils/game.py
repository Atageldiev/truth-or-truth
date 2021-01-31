from random import choice

from core.conf import questions, db
from utils.buttons import get_ikb


def pass_the_turn():
    """Passes the turn to the next player"""
    i = db.chats["i"]
    if i > len(db.chats.get_list("gamers")):
        i = 0

    db.chats["i"] = i + 1
    db.chats["player_whose_turn"] = db.chats.get_list("gamers")[i]
    db.chats["player_whose_turn_id"] = db.chats.get_list("gamers_user_id")[i]


async def give_question(message):
    db.chats["satisfied_players"] = 0
    db.chats["not_satisfied_players"] = 0
    db.chats["pressed_satisfied_players"] = ""
    db.chats["pressed_not_satisfied_players"] = ""
    db.chats["rate_question"] = False
    db.chats["got_answer_pressed"] = False

    question = choice(questions)
    db.chats["current_question"] = question

    await message.answer(f"Вопрос: {question}",
                         reply_markup=get_ikb({"text": "Ответ получен!", "callback_data": "got_answer"}))
