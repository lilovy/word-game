import psycopg2
# from config import port, host, db_name, password, user
from datetime import datetime
import config as cf
import psycopg2 as pg2

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker


# try:
class DatabaseTg:
    def __init__(self, host, port, user, password, database):
        """

        :type host: str
        :type port: str
        :type user: str
        :type password: str
        :type database: str
        """
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.host = host
        self.connection = None

    def connect(self):
        self.connection = pg2.connect(user=self.user, password=self.password, port=self.port, host=self.host, dbname=self.database)
        print('[INFO] PostgreSQL database connection established')

    def sel_ver(self):
        with self.connection.cursor() as cursor:
            cursor().execute(
                "select version()"
            )
            return cursor.fetchone()

    def select_user(self, tg_user):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""select *
                from wordgame.user
                where userId = {tg_user}"""
            )
            return cursor.fetchone()

    def select_all_users(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """select *
                from wordgame.user
                order by registration"""
            )
            return cursor.fetchall()

    def select_all_games(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""select *
                from wordgame.games
                """
            )
            return cursor.fetchall()

    def select_all_botbuff(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """select *
                from wordgame.botbuffer
                order by date 
                """
            )
            return cursor.fetchall()

    def select_all_userbuff(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """select *
                from wordgame.userbuffer
                order by date
                """
            )
            return cursor.fetchall()

    def select_all_faults(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """select *
                from wordgame.userfault
                order by date
                """
            )
            return cursor.fetchall()

    def select_user_fault(self, tg_user):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""select *
                from wordgame.userfault
                where userId = {tg_user}
                order by date """
            )
            return cursor.fetchall()

    def select_last_game(self, tg_user):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""select game
                from wordgame.games
                where userId = {tg_user}
                order by timestart
                limit 1"""
            )
            return cursor.fetchone()

    def select_bot_buff(self, tg_user, game=None):
        if game is None:
            if self.select_last_game(tg_user):
                game = self.select_last_game(tg_user)[0]
            else:
                return 'buffer is empty'
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""select word
                from wordgame.botbuffer
                where userId = {tg_user}
                and game = {game}
                order by date """
            )
            return cursor.fetchall()

    def select_user_buff(self, tg_user, game=None):
        if game is None:
            if self.select_last_game(tg_user):
                game = self.select_last_game(tg_user)[0]
            else:
                return 'buffer is empty'
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""select word
                from wordgame.userbuffer
                where userId = {tg_user}
                and game = {game}
                order by date """
            )
            return cursor.fetchall()

    def select_last_word(self, tg_user, game=0):
        if game == 0:
            if self.select_last_game(tg_user):
                game = self.select_last_game(tg_user)[0]
            else:
                return 'buffer is empty'
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""select word
                            from wordgame.userbuffer
                            where userId = {tg_user}
                            and game = {game}
                            order by date
                            limit 1"""
            )
            res = cursor.fetchone()
            if res:
                return res[-1]
            else:
                return 'buffer is empty'

    #
    # insert data section

    def insert_user(self, tg_user, name):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""insert into wordgame.user (userId, username, registration)
                    values ({tg_user}, '{name}', LOCALTIMESTAMP(2))
                """
            )
            self.connection.commit()

    def insert_user_buff(self, tg_user, word, game=None):
        if game is None:
            game = self.select_last_game(tg_user)[0]
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""insert into wordgame.userBuffer (userId, word, game, date)
                    values ({tg_user}, '{word}', {game}, LOCALTIMESTAMP(2))
                """
            )
            self.connection.commit()

    def insert_user_fault(self, tg_user, word, game=None):
        if game is None:
            game = self.select_last_game(tg_user)[0]
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""insert into wordgame.userFault (userId, word, game, date)
                    values ({tg_user}, '{word}', {game}, LOCALTIMESTAMP(2))
                """
            )
            self.connection.commit()

    def insert_bot_buff(self, tg_user, word, game=None):
        if game is None:
            game = self.select_last_game(tg_user)[0]
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""insert into wordgame.botBuffer (userId, word, game, date)
                    values ({tg_user}, '{word}', {game}, LOCALTIMESTAMP(2))
                """
            )
            self.connection.commit()

    def insert_game(self, tg_user, game=None):
        if game is None:
            previous_game = self.select_last_game(tg_user)[0]
            if previous_game is None:
                previous_game = 0
            game = previous_game + 1
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""insert into wordgame.games (userId, timestart, game)
                    values ({tg_user}, LOCALTIMESTAMP(2), {game})
                """
            )
            self.connection.commit()

    # delete data solution

    def del_word(self, tg_user, word):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""delete from wordgame.userbuffer
                    where userId = {tg_user}
                    and word = '{word}'
                """
            )
            self.connection.commit()


# def main():
#     return select_user(347265373)
#
#
# if __name__ == "__main__":
#     print(main())

db = DatabaseTg(port=cf.port, user=cf.user, password=cf.password, database=cf.db_name, host=cf.host)
db.connect()


# print(db.select_last_word(347265373))
# print(db.select_user_buff(347265373))
# print(db.select_last_word(347265373))
# print(db.select_user_fault(347265373))
# print(db.select_bot_buff(347265373))


