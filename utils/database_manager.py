from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from utils.models import *

class SessionManager:
    _default_url = "sqlite:///.database.db"
    _engine = None
    _Session = None

    @classmethod
    def create_engine(cls, url=_default_url):
        """Create and configure the SQLAlchemy engine and session."""
        cls._engine = create_engine(url)
        Base.metadata.create_all(cls._engine)
        cls._Session = sessionmaker(bind=cls._engine)
        print(f"Engine created with URL: {url}")

    @classmethod
    def get_session(cls):
        """Get a new SQLAlchemy session"""
        if cls._Session is None:
            raise RuntimeError("Engine is not created. Call `create_engine` first.")
        return cls._Session()
    
    @classmethod
    def close_engine(cls):
        """Dispose of the SQLAlchemy engine."""
        if cls._engine:
            cls._engine.dispose()
            cls._engine = None
            cls._Session = None
            print("Engine disposed.")

    @classmethod
    def get_member(cls, member_id: int):
        session = cls.get_session()

        try:
            member = session.query(Member).filter_by(id=member_id).first()
            if member is None:
                member = Member(id=member_id, words_guessed=0, yellow_guessed=0, green_guessed=0)
                session.add(member)
                session.commit()
                
        except Exception as e:
            session.rollback()
            print(f"Error incrementing win for member {member_id}: {e}")
        finally:
            session.close()

        return member

    @classmethod
    def increment_yellow_guessed(cls, member_id: int):
        session = cls.get_session()

        try:
            member = session.query(Member).filter_by(id=member_id).first()
            if member is None:
                member = Member(id=member_id, words_guessed=0, yellow_guessed=1, green_guessed=0)
                session.add(member)

            member.yellow_guessed += 1

            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error incrementing win for member {member_id}: {e}")
        finally:
            session.close()

    @classmethod
    def increment_green_guessed(cls, member_id: int):
        session = cls.get_session()

        try:
            member = session.query(Member).filter_by(id=member_id).first()
            if member is None:
                member = Member(id=member_id, words_guessed=0, yellow_guessed=0, green_guessed=1)
                session.add(member)

            member.green_guessed += 1

            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error incrementing win for member {member_id}: {e}")
        finally:
            session.close()

    @classmethod
    def increment_win(cls, member_id: int):
        session = cls.get_session()

        try:
            member = session.query(Member).filter_by(id=member_id).first()
            if member is None:
                member = Member(id=member_id, words_guessed=0, yellow_guessed=0, green_guessed=0)
                session.add(member)

            member.words_guessed += 1

            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error incrementing win for member {member_id}: {e}")
        finally:
            session.close()

SessionManager.create_engine()