import logging

from aiogram import executor
from core.conf import dp

import handlers

logging.basicConfig(level=logging.INFO)
print(handlers.IMPORTED)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
