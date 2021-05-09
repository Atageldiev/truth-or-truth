import os
from pathlib import Path

import yaml
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from utils import get_current_dir

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

ADMIN_ID = 399344900
VOTE_TIME = 15

with open(os.path.join(get_current_dir(__file__), "questions.yml")) as f:
    questions = yaml.safe_load(f).get("questions")

easter_eggs = {
    '!ктоАида': 'Его destiny❤️',
    '!ктоСалли': 'МИЛКВИЗТУ!!!',
    '!ктоАлибек': 'Его лав ки💖',
    '!лучшаягруппа': 'ГРУППА DOUBLEFAM!',
    '!ктобатя': 'ТЭЙЛОР!',
    '!ктоАтагелдиев': 'ДА ОН ПРОСТО ПУЩКА!!!',
    '!лучшаяигра': 'ПРАВДА ИЛИ ПРАВДА - ЭТО ПРОСТО ПУЩЩЩКААААА!',
    '!ктогот': 'БЕЗУСЛОВНО АИДА!',
    '!дестинейшн': 'Бать, это слова Аиды😂❤️❤',
    '!промисс❤️': 'Бать, это слова Аиды😂❤️❤',
    '!слово': 'лав ки❤️',
    '!позовиУ': 'УЛАНБЕКОВЫ ВЫ ГДЕЕЕЕЕЕЕ??????',
    '!позовиА': 'АТАГЕЛДИЕВЫ ВЫ ГДЕЕЕЕЕЕЕ??????',
    '!пропусти': 'Хорошо, пропускаю, бать :)',
    '!состав': 'Атагелдиевы: Улук, Аида\nУланбековы: Алибек, Салли',
    '!хелп': 'Доступные команды: !слово, !позовиУ, !позовиА, !лучшаягруппа, !лучшаяигра',
    '!коннект': 'ВОТ ЭТО КОННЕКТ!',
    '!allGroups': 'Бать, надо в лс зайти чтобы сработало :)',
    '!addQuestion': 'Бать, надо в лс зайти чтобы сработало :)',
    '!addquestion': 'Бать, надо в лс зайти чтобы сработало :)',
}
