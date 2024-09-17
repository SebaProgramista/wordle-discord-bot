from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, DateTime, BigInteger

Base = declarative_base()

class Member(Base):
    __tablename__ = "members"

    id = Column(BigInteger, primary_key=True)
    words_guessed = Column(Integer)
    yellow_guessed = Column(Integer)
    green_guessed = Column(Integer)

    def __repr__(self) -> str:
        return f"<Member id: {self.id}, words_guessed: {self.words_guessed}, yellow_guessed: {self.yellow_guessed}, green_guessed: {self.green_guessed}"
    
