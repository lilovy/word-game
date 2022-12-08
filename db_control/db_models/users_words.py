from sqlalchemy import Column, Integer, ForeignKey, BigInteger, DateTime, String
from db_control.db_models.database import Base, engine
from datetime import datetime


class UserDict(Base):
    __tablename__ = 'user_dict'

    id = Column(Integer, primary_key=True)
    userId = Column(BigInteger, ForeignKey('users.userId'))
    word = Column(String(50))
    date = Column(DateTime, default=datetime.now)

    def __init__(self, userId: int, word: str):
        self.userId = userId
        self.word = word

    def __repr__(self):
        info: str = f'{self.word}'
        return info


Base.metadata.create_all(engine)

