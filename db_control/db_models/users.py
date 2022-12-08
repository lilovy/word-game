from sqlalchemy import Column, String, BigInteger, DateTime
from db_control.db_models.database import Base, engine
from datetime import datetime


class Users(Base):
    __tablename__ = 'users'

    """
    userId: telegram id
    username: username telegram user
    registration: date of registration
    """

    userId = Column(BigInteger, primary_key=True)
    username = Column(String(50))
    registration = Column(DateTime, default=datetime.now)

    def __init__(self, userId: int, username: str):
        self.userId = userId
        self.username = username

    def __repr__(self):
        info: str = f'{self.userId}\n' \
                    f'{self.username}\n' \
                    f'{self.registration}'
        return info


Base.metadata.create_all(engine)
