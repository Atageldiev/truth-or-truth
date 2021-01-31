from core.db.base import DBTable


class RatingTable(DBTable):
    table_name = "rating"
    fields = [
        ("chat_id", "BIGINT"),
        ("user_id", "BIGINT"),
        ("name", "TEXT"),
        ("added_questions_number", "INTEGER DEFAULT 0"),
        ("likes", "INTEGER DEFAULT 0"),
        ("dislikes", "INTEGER DEFAULT 0"),
    ]

    def all(self):
        """Берем все содержимое базы"""
        with self._connection:
            sql = self.table.select("user_id").where(self.table.chat_id == self.chat.id)
            self._cursor.execute(sql.get_sql())
            return self._cursor.fetchall()

    def add(self):
        """Добавить новые данные в базу"""
        with self._connection:
            sql_command = self.table.insert(self.chat.id, self.user.id, self.user.first_name)
            self._cursor.execute(sql_command.get_sql())

    def exists(self):
        """Проверить существуют ли данные в базе"""
        with self._connection:
            sql_command = (self.table.select("user_id")
                           .where(self.table.chat_id == self.chat.id)
                           .where(self.table.user_id == self.user.id))
            self._cursor.execute(sql_command.get_sql())
            return self._cursor.fetchone() is not None
