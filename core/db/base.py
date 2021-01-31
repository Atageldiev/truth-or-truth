import psycopg2
from aiogram.types import User, Chat

from pypika import Table, Query, Column


class Database:
    def __init__(self, db_name):
        self.connection = psycopg2.connect(database=db_name, user="postgres", password="postgres", host="localhost")


class DBTable:
    table_name: str = NotImplemented
    fields: list[tuple] or tuple[tuple] = NotImplemented
    table: Table = NotImplemented

    def __init__(self, connection):
        self._connection = connection
        self._cursor = self._connection.cursor()
        self.__create_table()

    def __init_subclass__(cls, **kwargs):
        if cls.table == NotImplemented:
            cls.table = Table(cls.table_name)

    def __getitem__(self, item: str):
        """Получаем значение"""
        with self._connection:
            command = self.table.select(item) \
                .where(self.table.chat_id == self.chat.id) \
                .where(self.table.user_id == self.user.id)
            self._cursor.execute(command.get_sql())
            return self._cursor.fetchone()[0]

    def __setitem__(self, key, value):
        """Изменяем значение"""
        with self._connection:
            command = self.table.update().set(key, value) \
                .where(self.table.chat_id == self.chat.id) \
                .where(self.table.user_id == self.user.id)
            self._cursor.execute(command.get_sql())

    def __create_table(self):
        with self._connection:
            command = (Query().create_table(self.table_name).if_not_exists()
                       .columns(*[Column(*column_data) for column_data in self.fields]))
            self._cursor.execute(command.get_sql())

    def reset(self):
        """Reset all defaults"""
        for field_name, field_type in filter(lambda field: field[1].__contains__("DEFAULT"), self.fields):
            self[field_name] = field_type.split("DEFAULT")[1].strip().removesuffix("'").removeprefix("'")

    @property
    def user(self):
        return User().get_current()

    @property
    def chat(self):
        return Chat().get_current()


class DBManager:
    _db: Database = NotImplemented
