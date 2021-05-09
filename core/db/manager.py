from .base import Database
from .tables import CustomQuestionsTable, RatingTable

_db = Database("db")

custom_questions = CustomQuestionsTable(_db.get_connection())
rating = RatingTable(_db.get_connection())
