import sqlite3

class Sqlighter():
    def __init__(self, database="server.db"):
        self.connection = sqlite3.connect(database=database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_table(self):
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS chats(
                chat_id INTEGER,
                rate_question BOOL,
                got_answer_pressed  BOOL,
                next_question_chosen  BOOL,
                previous_question_chosen  BOOL,
                player_whose_turn  STRING,
                player_whose_turn_id INTEGER,
                satisfied_players  INTEGER,
                not_satisfied_players  INTEGER,
                current_question  STRING,
                pressed_satisfied_users  STRING,
                pressed_not_satisfied_users  STRING,
                gamers  STRING,
                gamers_user_id STRING,
                i INTEGER
            )""")

    def create_table_of_questions(self):
        """Создаст таблицу для пользовательских вопросов"""
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS custom_questions(
                question STRING)""")
            
    def create_rating_table(self):
        """Создает таблицу рейтинга"""
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS rating(
                chat_id INTEGER,
                user_id INTEGER,
                name STRING,
                added_questions_number INTEGER,
                likes INTEGER,
                dislikes INTEGER)""")

    def chat_exists(self, chat_id):
        """Проверяем есть ли такой chat_id в базе данных"""
        with self.connection:
            self.cursor.execute(
                f"SELECT chat_id FROM chats WHERE chat_id = {chat_id}")
            if self.cursor.fetchone() is None:
                self.cursor.execute(f"INSERT INTO chats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                    chat_id,  True, False, False, False, "", 0, 0, 0, "", "", "", "", "", 0))
            else:
                pass

    def user_id_exists(self, chat_id, user_id, name):
        """Проверит есть ли такой юзер в базе, если нет - добавит"""
        with self.connection:
            self.cursor.execute(
                f"SELECT user_id FROM rating WHERE chat_id={chat_id} and user_id={user_id}")
            if self.cursor.fetchone() is None:
                self.cursor.execute(
                    f"INSERT INTO rating VALUES (?, ?, ?, ?, ?, ?)", (chat_id, user_id, name, 0, 0, 0))
            else:
                pass

    def custom_question_exists(self, question):
        with self.connection:
            self.cursor.execute(f"SELECT question FROM custom_questions WHERE question='{question}'")
            if self.cursor.fetchone() is None:
                self.cursor.execute(f"INSERT INTO custom_questions VALUES (?)", (question,))
                return False
            else:
                return True

    
    def get_value(self, name, table, chat_id=0, user_id=0):
        """Получаем значение какой-либо переменной в таблице"""
        with self.connection:
            if table == "chats":
                for i in self.cursor.execute(f"SELECT {name} FROM chats WHERE chat_id = {chat_id}"):
                    return i[0]

            elif table == "rating":
                for i in self.cursor.execute(f"SELECT {name} FROM rating WHERE chat_id={chat_id} and user_id = {user_id}"):
                    return i[0]

    def get_user_ids(self, chat_id):
        """Берем все user_id в базе"""
        with self.connection:
            return self.cursor.execute(f"SELECT user_id FROM rating WHERE chat_id={chat_id}").fetchall()

    def update_value(self, name, value, table, chat_id=0, user_id=0):
        with self.connection:
            if table == "chats":
                try:
                    self.cursor.execute(f"UPDATE chats SET {name}={value} WHERE chat_id = {chat_id}")
                except:
                    self.cursor.execute(f"UPDATE chats SET {name}='{value}' WHERE chat_id = {chat_id}")

            elif table == "rating":
                self.cursor.execute(f"UPDATE rating SET {name}={value} WHERE chat_id={chat_id} and user_id={user_id}")

            elif table == "num_of_q": # Обновляет количество добавленных вопросов в таблицу rating
                self.cursor.execute(f"UPDATE rating SET {name}={value} WHERE user_id={user_id}")
    
    def get_list(self, name, chat_id):
        """Преобразует элементы строчного типа в список"""
        with self.connection:
            for i in self.cursor.execute(f"SELECT {name} FROM chats WHERE chat_id = {chat_id}"):
                i = i[0].split(";")
                i.remove("")
            return i
