from .base import DBManager, Database as BaseDatabase
from .tables import ChatsTable, CustomQuestionsTable, RatingTable


class Database(DBManager):
    _db = BaseDatabase("db")

    chats = ChatsTable(_db.connection)
    custom_questions = CustomQuestionsTable(_db.connection)
    rating = RatingTable(_db.connection)
