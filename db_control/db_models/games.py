from sqlalchemy import Column, Integer, ForeignKey, BigInteger, DateTime
from db_control.db_models.database import Base, engine
from datetime import datetime


class Games(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    userId = Column(BigInteger, ForeignKey('users.userId'))
    game = Column(Integer)
    date = Column(DateTime, default=datetime.now)

    def __init__(self, userId: int, game: int):
        self.userId = userId
        self.game = game

    def __repr__(self):
        info: str = f'{self.userId}\n' \
                    f'{self.game}\n' \
                    f'{str(self.date)[:19]}'
        return info


Base.metadata.create_all(engine)

