from aiogram.types import InlineKeyboardMarkup

from core.conf import db
from utils.buttons import get_ikb


class InlineKeyboards:
    JOIN_GAME = get_ikb({"text": "Присоединиться", "callback_data": "join_game"})

    CHOOSE_WHAT_NEXT = get_ikb([{"text": "Следующий вопрос", "callback_data": "next_question"},
                                {"text": "Перезадать предыдущий", "callback_data": "prev_question"}])

    @staticmethod
    def satisfaction() -> InlineKeyboardMarkup:
        return get_ikb([{"text": f"{db.chats['satisfied_players']}❤", "callback_data": "satisfied"},
                        {"text": f"{db.chats['not_satisfied_players']}💔", "callback_data": "not_satisfied"}])
