"""
Файл bot.py - каркасс из разных функций, собранных их разных модулей


Все функции для обработки команд в файле command_handler.py
Все функции для обработки callback'ов в файле callback_handler.py
Все функции по работе с БД прописаны в классе Sqlighter в файле myclass.py
Все дополнительные/вспомогательные функции в файле mymodule.py

Все классы в файле myclass.py

Все нужные константы в config.py

Инициализация необходимых переменных в loader
"""

# import required libraries
import logging

# import from aiogram
from aiogram import executor
from aiogram.types import Message, CallbackQuery

# import from my files
from loader import dp 
from command_handler import send_welcome, new_round, add_question, add_into_db, send_rating
from callback_handler import join_game, got_answer, rate_answer, next_or_prev_q
from mymodule import on_startup
from utils import States

# Configure logging
logging = logging.basicConfig(level=logging.INFO)

# Create tables in db
on_startup()

# Handle all commands
@dp.message_handler(commands=['start'])
async def process_command_start(message: Message):
    await send_welcome(message)

@dp.message_handler(commands=['new_round'])
async def start_new_round(message: Message):
    await new_round(message)

@dp.message_handler(commands=['rating'])
async def process_send_rating(message: Message):
    await send_rating(message)

@dp.message_handler(commands=['add_my_question'])
async def process_add_question(message: Message):
    await add_question(message)

@dp.message_handler(state=States.STATE_0)
async def process_state_0(message: Message):
    await add_into_db(message)

@dp.message_handler(commands=['help'])
async def process_send_help(message: Message):
    await message.answer("В разработке...")


# Handle all inline-buttons
@dp.callback_query_handler(lambda c: c.data=='join_game')
async def process_join_game(callback_query: CallbackQuery):
    await join_game(callback_query)

@dp.callback_query_handler(lambda c: c.data=="got_answer")
async def process_got_answer(callback_query: CallbackQuery):
    await got_answer(callback_query)

@dp.callback_query_handler(lambda c: c.data=="satisfied")
@dp.callback_query_handler(lambda c: c.data=="not_satisfied")
async def process_rate_answer(callback_query: CallbackQuery):
    await rate_answer(callback_query)

@dp.callback_query_handler(lambda c: c.data=="next_question")
@dp.callback_query_handler(lambda c: c.data=="prev_question")
async def process_choose_wtd_next(callback_query: CallbackQuery):
    await next_or_prev_q(callback_query)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
