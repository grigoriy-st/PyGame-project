import sqlite3

DB_PATH = '../data/db.sql'

class DBManager:
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS scores
                               (id INTEGER PRIMARY KEY, player_name TEXT, score INTEGER)''')
        self.connection.commit()

    def add_score(self, player_name, score):
        self.cursor.execute('INSERT INTO scores (player_name, score) VALUES (?, ?)', (player_name, score))
        self.connection.commit()

    def get_scores(self):
        self.cursor.execute('SELECT * FROM scores ORDER BY score DESC')
        return self.cursor.fetchall()

    def update_score(self, player_name, new_score):
        self.cursor.execute('UPDATE scores SET score = ? WHERE player_name = ?', (new_score, player_name))
        self.connection.commit()


    def get_last_score(self, player_name):
        ...

    def get_best_score(self):
        ...

    def close(self):
        self.connection.close()