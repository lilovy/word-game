from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, DateTime
from db_control.db_models.database import Base,engine
from datetime import datetime


class UsersFault(Base):
    __tablename__ = 'user_fault'

    id = Column(Integer, primary_key=True)
    userId = Column(BigInteger, ForeignKey('users.userId'))
    word = Column(String(50))
    game = Column(Integer)
    date = Column(DateTime, default=datetime.now)

    def __init__(self, userId: int, word: str, game: int):
        self.userId = userId
        self.word = word
        self.game = game

    def __repr__(self):
        info: str = f'userId: {self.userId}' \
                    f'word: {self.word}' \
                    f'game: {self.game}' \
                    f'date: {str(self.date)[:19]}'
        return info


Base.metadata.create_all(engine)
