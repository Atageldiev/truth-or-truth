from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, ChatType

from core.conf import db


def is_private(message: Message):
    return message.chat.type == ChatType.PRIVATE


def is_not_private(message: Message):
    return not is_private(message)


def is_group(message: Message):
    return message.chat.type == ChatType.GROUP


def is_not_group(message: Message):
    return not is_group(message)


def is_supergroup(message: Message):
    return message.chat.type == ChatType.SUPERGROUP


def is_not_supergroup(message: Message):
    return not is_supergroup(message)


def is_player_whose_turn(c: CallbackQuery):
    return db.chats["player_whose_turn"] == c.from_user.first_name


def shared_satisfaction(c: CallbackQuery):
    return (c.from_user.first_name in db.chats.get_list("pressed_satisfied_players")
            and c.from_user.first_name in db.chats.get_list("pressed_not_satisfied_players"))


def has_joined_game(c: CallbackQuery):
    return c.from_user.first_name in db.chats.get_list("gamers")


def get_command_filter(command: str):
    return Command(command)
