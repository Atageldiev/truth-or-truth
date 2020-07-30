# import required libraries
import logging

# import from aiogram
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery

# import from my custom files
from config import ADMIN_ID, TOKEN, addQuestion_file_id
from myclass import Sqlighter
from mymodule import game, new_round, on_startup, got_answer_process, choose_wtd_next, buttons

# Configure logging
logging = logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot)

# Create object for data base
db = Sqlighter()

# Create tables in db
on_startup()


@dp.message_handler(content_types=["photo"])
async def myfunc(message: Message):
    await message.answer("Privet iobana")
    print(message.photo[-1].file_id)

@dp.message_handler()
async def myfunc2(message: Message):
    
    await message.answer(message.text)
    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
