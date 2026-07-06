import sqlite3
from datetime import datetime

DATABASE_NAME = "results.db"


class Database:

    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """Создание таблицы результатов."""

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS results(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                date TEXT,

                difficulty TEXT,

                score INTEGER,

                coins INTEGER,

                enemies INTEGER,

                bosses INTEGER,

                victory INTEGER,

                play_time REAL

            )
        """)

        self.connection.commit()

    def add_result(
            self,
            difficulty,
            score,
            coins,
            enemies,
            bosses,
            victory,
            play_time
    ):

        self.cursor.execute("""

            INSERT INTO results(

                date,
                difficulty,
                score,
                coins,
                enemies,
                bosses,
                victory,
                play_time

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            datetime.now().strftime("%d.%m.%Y %H:%M"),

            difficulty,
            score,
            coins,
            enemies,
            bosses,
            int(victory),
            round(play_time, 1)

        ))

        self.connection.commit()

    def get_statistics(self):
        """Общая статистика."""

        self.cursor.execute("""

            SELECT

                COUNT(*),
                COUNT(CASE WHEN victory = 1 THEN 1 END),
                COUNT(CASE WHEN victory = 0 THEN 1 END),
                AVG(score),
                SUM(coins),
                SUM(enemies),
                SUM(bosses),
                MAX(score)

            FROM results

        """)

        row = self.cursor.fetchone()

        if row[0] == 0:
            return {

            "games": 0,
            "wins": 0,
            "losses": 0,
            "avg_score": 0,
            "coins": 0,
            "enemies": 0,
            "bosses": 0,
            "best_score": 0

        }

        return {

            "games": row[0],
            "wins": row[1],
            "losses": row[2],
            "avg_score": int(row[3] or 0),
            "coins": row[4] or 0,
            "enemies": row[5] or 0,
            "bosses": row[6] or 0,
            "best_score": row[7] or 0

        }

    def get_last_games(self, limit=10):

        self.cursor.execute("""

            SELECT

                date,
                difficulty,
                score,
                coins,
                victory,
                play_time

            FROM results

            ORDER BY id DESC

            LIMIT ?

        """, (limit,))

        return self.cursor.fetchall()

    def close(self):

        self.connection.close()