import sqlite3

from typing import Tuple

DB_PATH = '../data/db.sql'


class DBManager:
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()


    def add_record(self, player_name, score, coins):
        """ Запись результата игры. """
        if self.get_last_score(player_name)[1]:  # Существует ли уже запись?
            self.update_score(player_name, score, coins)
        else:
            self.cursor.execute('''
                                insert into
                                    scores
                                (name, score, coins)
                                VALUES
                                    (?, ?, ?)''', (player_name, score, coins))
            self.connection.commit()

    def get_scores(self) -> Tuple[str, int]:
        """ Получение результатов игры. """
        self.cursor.execute('''
                            select
                                name, score
                            from scores \
                            sort by \
                                score
                            order by
                                desc''')
        return self.connection.commit()

    def update_score(self, player_name, new_score, coins):
        """  Обновление данных пользователя. """
        self.cursor.execute('''
                            update
                                scores
                            set score = ?, coins = ?
                            WHERE
                                name = ?''',
                            (new_score, coins, player_name))
        self.connection.commit()

    def get_last_score(self, player_name) -> Tuple[int, bool]:
        """ Получение данных о рекорде текущего пользователя. """
        self.cursor.execute(f'''
                            select
                                score
                            from scores
                            where
                                name = '{player_name}'
                            ''')
        last_player_score = self.cursor.fetchall()
        if last_player_score:
            return last_player_score[0][0], True
        else:
            return None, False
        ...

    def get_best_score(self) -> Tuple[str, int]:
        """ Получение данных о лучше пользователе среди всех. """
        self.cursor.execute('''
                            select
                                name, score
                            from scores
                            order by
                                score desc
                            ''')

        scores = list(self.cursor.fetchall())
        if scores:
            best_score = scores[0]
            return best_score

    def close(self):
        self.connection.close()
