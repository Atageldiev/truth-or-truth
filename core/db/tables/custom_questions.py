from core.db.base import DBTable


class CustomQuestionsTable(DBTable):
    table_name = "custom_questions"
    fields = [("question", "TEXT"), ]

    def add(self, value: str):
        with self._connection:
            command = self.table.insert(value)
            self._cursor.execute(command.get_sql())

    def exists(self, value: str):
        with self._connection:
            command = self.table.select("question").where(getattr(self.table, "question") == value)
            self._cursor.execute(command.get_sql())
            return self._cursor.fetchone() is not None
