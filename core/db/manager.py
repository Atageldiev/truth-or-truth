from .base import DBManager, Database as BaseDatabase
from .tables import CustomQuestionsTable, RatingTable


class Database(DBManager):
    _db = BaseDatabase("db")

    custom_questions = CustomQuestionsTable(_db.get_connection())
    rating = RatingTable(_db.get_connection())
