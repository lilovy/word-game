import os
from collections import defaultdict

from db_control.db_models.database import DATABASE_NAME, create_db, Session
from sqlalchemy import and_
from db_control.db_models.users import Users
from db_control.db_models.games import Games
from db_control.db_models.user_buffer import UsersBuffer
from db_control.db_models.user_fault import UsersFault
from db_control.db_models.bot_buffer import BotBuffer
from db_control.db_models.users_words import UserDict


def create_database():
    create_db()


def create_record(table, **kwargs):
    session = Session()
    try:
        obj = table(**kwargs)
        session.add(obj)
        session.commit()
        session.close()
    except:
        # print('user already exists')
        return


def del_record(table, **kwargs):
    session = Session()
    try:
        rec = session.query(table).filter(and_(table.userId == kwargs['userId'],
                                               table.word == kwargs['word'],
                                               table.game == kwargs['game'])).first()
        session.delete(rec)
        session.commit()
        session.close()
    except:
        return


def get_items(table, **kwargs):
    session = Session()
    arg = kwargs
    items = []
    for it in session.query(table).filter(eval(f'table.{list(arg)[0]}') == list(arg.values())[0]):
        user = str(it).split()
        items.append(user)
    session.close()
    return items


def check_user(userId, name):
    session = Session()
    if session.query(Users).filter(Users.userId == userId).first() is not None:
        return True
    create_record(Users, userId=userId, username=name)


def check_word(table, userId, word, game):
    session = Session()
    return session.query(table).filter(and_(table.word == word, table.userId == userId, table.game == game)).first() is not None


def check_game(userId):
    session = Session()
    try:
        game = session.query(Games).filter(Games.userId == userId).order_by(Games.id.desc()).first()
        return int(str(game).split()[1])
    except:
        return 0


def check_buffer(table, **kwargs):
    session = Session()
    res = []
    if len(kwargs) != 0:
        for it in session.query(table).filter(and_(table.userId == kwargs['userId'], table.game == kwargs['game'])):
            user = str(it).split('\n')
            id = user[0]
            word = user[1]
            game = int(user[2])
            # date = user[3]
            res.append(f"Id: {id}, word: {word}, game: {game}")
        return res

    else:
        res = defaultdict(list)
        for it in session.query(table):
            try:
                user = str(it).split('\n')
                id = user[0]
                username = get_username(int(id))
                word = user[1]
                try:
                    game = int(user[2])
                    # date = user[3]

                except:
                    word += f' {user[2]}'
                    game = int(user[3])
                    # date = user[4]
            except:
                ...
            # res.append(f"{id},  {word},  {game}\n")
            res[username].append(word)
        return dict(res)


def get_word(table, **kwargs):
    session = Session()
    try:
        word = session.query(table).filter(table.userId == kwargs['userId']).order_by(table.id.desc()).first()
        return str(word).split()[1]
    except:
        return


def get_user():
    session = Session()
    res = []
    for it in session.query(Users):
        user = str(it).split('\n')
        id = user[0]
        username = user[1]
        # date = user[2]
        res.append(f"ID: {id},  USERNAME: {username}")
    return res


def get_username(userId):
    session = Session()
    word = session.query(Users).filter(Users.userId == userId).first()
    return str(word).split('\n')[1]


def last_record(userId, word):
    session = Session()



if __name__ == "__main__":
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        print("create...")
        create_database()
        print("db is created")

    print(get_user())
