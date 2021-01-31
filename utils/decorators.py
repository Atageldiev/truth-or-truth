from aiogram.types import Message

from core.conf import db
from .filters import is_private, is_group, is_supergroup


def check_existance(table_name):
    def check_decorator(fn):
        async def wrapper(*args, **kwargs):
            table = getattr(db, table_name)
            if not table.exists():
                table.add()
            return await fn(*args, **kwargs)

        return wrapper

    return check_decorator


class Chats:
    @staticmethod
    def only_private_chat(fn):
        async def wrapper(message: Message, *args, **kwargs):
            if is_private(message):
                return await fn(message, *args, **kwargs)

            return await message.answer("Эта команда работает только в ЛС")

        return wrapper

    @staticmethod
    def only_group_chat(fn):
        async def wrapper(message: Message, *args, **kwargs):
            if is_group(message) or is_supergroup(message):
                return await fn(message, *args, **kwargs)

            return await message.answer("Эта команда работает только в группах")

        return wrapper
