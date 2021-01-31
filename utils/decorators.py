from core.conf import db


def check_user_existance(fn):
    async def wrapper(*args, **kwargs):
        if not db.rating.exists():
            db.rating.add()
        return await fn(*args, **kwargs)

    return wrapper


def check_chat_existance(fn):
    async def wrapper(*args, **kwargs):
        if not db.chats.exists():
            db.rating.add()
        return await fn(*args, **kwargs)

    return wrapper


def check_existance(table_name):
    def check_decorator(fn):
        async def wrapper(*args, **kwargs):
            table = getattr(db, table_name)
            if not table.exists():
                table.add()
            return await fn(*args, **kwargs)

        return wrapper

    return check_decorator
