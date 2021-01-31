from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_ikb(data: list[dict] or dict, row_width: int = 3) -> InlineKeyboardMarkup:
    """Returns InlineKeyboardMarkup, that's ready to use in message"""
    markup = InlineKeyboardMarkup(row_width=row_width)

    if isinstance(data, list):
        for button_data in data:
            markup.insert(InlineKeyboardButton(**button_data))
    elif isinstance(data, dict):
        markup.add(InlineKeyboardButton(**data))
    else:
        raise ValueError(f'Got unexpected type of data: {type(data)}. Should be list of dicts or dict')
    return markup
