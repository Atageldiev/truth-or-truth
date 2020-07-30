# import from aiogram
from aiogram import Bot, Dispatcher, types

# import from my custom files
from config import TOKEN
from myclass import Sqlighter
from mymodule import buttons, turn, give_question

# import from other libraries
from time import sleep

# Initialize bot and dispatcher
bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot)

# Create object for data base
db = Sqlighter()

async def send_welcome(message):
    if message.chat.type != "private":
        await message.reply("Привет, я бот-ведущий для игры в 'Правда или правда'")
        await game(message)
        db.chat_exists(message.chat.id)
    else:
        await message.reply("Команда работает только в группах")


async def game(message):
    await message.reply("Начат набор в новую игру\n\n/new_round для начала нового раунда", reply_markup = buttons("Присоединиться", "join_game"))
    await message.answer("В игре: ")
    db.update_value(name="gamers", value="", table="chats", chat_id=message.chat.id)
    db.update_value(name="gamers_user_id", value="", table="chats", chat_id=message.chat.id)

async def new_round(message):
    chat_id = message.chat.id
    # markup = types.InlineKeyboardMarkup()
    # markup.add(types.InlineKeyboardButton(text="Ответить в лс➡️", url="https://t.me/truth_or_truth_bot", callback_data="give_answer"))
    if db.get_list("gamers", chat_id) != []:
        if db.get_value(name="rate_question", table="chats", chat_id=chat_id) == True:
            await message.answer("Сейчас отвечает: " + turn(message.chat.id))

            db.update_value(name="next_question_chosen", value=False, table="chats", chat_id=message.chat.id)
            db.update_value(name="previous_question_chosen", value=False, table="chats", chat_id=message.chat.id)

            await give_question(message)

        else:
            await message.answer("Для начала нужно оценить предыдущий ответ!\nНажмите кнопку 'ответ получен'")
    else:
        await message.answer("Недостаточно игроков!\nНабор в игру по команде /start")



    



    
