from aiogram.dispatcher.filters.state import State, StatesGroup


class AddQuestionStates(StatesGroup):
    SEND_QUESTION = State()
