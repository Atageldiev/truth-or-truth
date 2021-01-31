from core.db.base import DBTable


class ChatsTable(DBTable):
    table_name = "chats"
    fields = [
        ("chat_id", "BIGINT"),
        ("rate_question", "BOOL DEFAULT 'yes'"),
        ("got_answer_pressed", "BOOL DEFAULT 'no'"),
        ("next_question_chosen", "BOOL DEFAULT 'no'"),
        ("previous_question_chosen", "BOOL DEFAULT 'no'"),
        ("player_whose_turn", "TEXT DEFAULT ''"),
        ("player_whose_turn_id", "INTEGER DEFAULT 0"),
        ("satisfied_players", "INTEGER DEFAULT 0"),
        ("not_satisfied_players", "INTEGER DEFAULT 0"),
        ("current_question", "TEXT DEFAULT ''"),
        ("pressed_satisfied_players", "TEXT DEFAULT ''"),
        ("pressed_not_satisfied_players", "TEXT DEFAULT ''"),
        ("gamers", "TEXT DEFAULT ''"),
        ("gamers_user_id", "TEXT DEFAULT ''"),
        ("i", "INTEGER DEFAULT 0"),
    ]

    def add(self):
        with self._connection:
            sql_command = self.table.insert(self.chat.id)
            self._cursor.execute(sql_command.get_sql())

    def exists(self):
        with self._connection:
            sql_command = self.table.select("chat_id").where(self.table.chat_id == self.chat.id)
            self._cursor.execute(sql_command.get_sql())
            return self._cursor.fetchone() is not None

    def get_list(self, name):
        """Преобразует элементы строчного типа в список"""
        with self._connection:
            sql_command = self.table.select(name).where(self.table.chat_id == self.chat.id)
            self._cursor.execute(sql_command.get_sql())

            i = self._cursor.fetchone()
            if i is None:
                return []
            i = i[0].split(";")
            i.remove("")
            return i

    def __getitem__(self, item: str):
        """Получаем значение"""
        with self._connection:
            command = (self.table.select(item)
                       .where(self.table.chat_id == self.chat.id))
            self._cursor.execute(command.get_sql())
        return self._cursor.fetchone()[0]

    def __setitem__(self, key, value):
        """Изменяем значение"""
        with self._connection:
            command = (self.table.update().set(key, value)
                       .where(self.table.chat_id == self.chat.id))
            self._cursor.execute(command.get_sql())
