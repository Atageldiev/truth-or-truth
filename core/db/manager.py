from .base import Database as BaseDatabase
from .tables import CustomQuestionsTable, RatingTable

_db = BaseDatabase("db")

custom_questions = CustomQuestionsTable(_db.get_connection())
rating = RatingTable(_db.get_connection())
