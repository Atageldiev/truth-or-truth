import asyncio

from aiogram.types import CallbackQuery

from core.conf import dp, db, VOTE_TIME
from utils import filters
from utils.decorators import check_existance
from utils.game import give_question
from .buttons import InlineKeyboards


@dp.callback_query_handler(text='join_game')
@check_existance("rating")
async def join_game(call, *args, **kwargs):
    if filters.has_joined_game(call):
        return await call.answer("Ты уже в игре")

    db.chats["gamers"] += call.from_user.first_name + ";"
    db.chats["gamers_user_id"] += str(call.from_user.id) + ";"

    await call.answer("Ты успешно присоединился к игре")
    await call.message.edit_text(call.message.text + ', '.join(db.chats.get_list('gamers')),
                                 reply_markup=InlineKeyboards.JOIN_GAME)


@dp.callback_query_handler(filters.is_player_whose_turn)
async def not_for_you(call: CallbackQuery):
    return await call.answer("Эта кнопка предназначена не для тебя!")


@dp.callback_query_handler(text="got_answer")
async def got_answer(call: CallbackQuery):
    db.chats["got_answer_pressed"] = True

    await call.message.answer(f"Оцени ответ игрока: {db.chats['player_whose_turn']}",
                              reply_markup=InlineKeyboards.satisfaction())
    await call.message.answer(f"Результаты голосования будут через {VOTE_TIME} секунд")
    await asyncio.sleep(VOTE_TIME)

    satisfied_players = db.chats["satisfied_players"]
    not_satisfied_players = db.chats["not_satisfied_players"]

    db.chats["rate_question"] = True
    db.rating["likes"] += satisfied_players
    db.rating["dislikes"] += satisfied_players
    await call.message.answer(f"Результаты:\n❤️ - {satisfied_players}\n💔 - {not_satisfied_players}")

    if satisfied_players >= not_satisfied_players:
        return await call.message.answer(f"Ответ прошел голосование\n\nЖду команду /new_round")
    await call.message.answer(f"Ответ не прошел голосование\n\nЧто делать дальше?",
                              reply_markup=InlineKeyboards.CHOOSE_WHAT_NEXT)


@dp.callback_query_handler(lambda call: filters.shared_satisfaction(call))
async def handle_already_shared_satisfaction(call: CallbackQuery):
    await call.answer("Вы уже проголосовали!")


@dp.callback_query_handler(text="satisfied")
@dp.callback_query_handler(text="not_satisfied")
async def rate_answer(call):
    players_key = "{}_players".format(call.data)
    pressed_players_key = "pressed_{}_players".format(call.data)

    db.chats[players_key] += 1
    db.chats[pressed_players_key] += call.from_user.first_name + ";"
    await call.message.edit_reply_markup(reply_markup=InlineKeyboards.satisfaction())


@dp.callback_query_handler(lambda: db.chats["next_question_chosen"] or db.chats["previous_question_chosen"])
async def next_or_prev_question_chosen(call: CallbackQuery):
    await call.answer("Вариант уже был выбран")


@dp.callback_query_handler(text="next_question")
async def next_question(call):
    db.chats["next_question_chosen"] = True
    await call.message.answer("Было выбрано продолжать\n\nЖду команду /new_round")


@dp.callback_query_handler(text="prev_question")
async def prev_question(call):
    db.chats["previous_question_chosen"] = True
    await give_question(call.message)
