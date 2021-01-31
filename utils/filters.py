from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ChatType


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


def get_command_filter(command: str):
    return Command(command)
