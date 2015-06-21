import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from settings import DB_URI

Base = declarative_base()

class Game(Base):

    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    word_status = sqlalchemy.Column(sqlalchemy.String)
    wrong_letters = sqlalchemy.Column(sqlalchemy.String)
    num_wrong_letters = sqlalchemy.Column(sqlalchemy.Integer)
    game_status = sqlalchemy.Column(sqlalchemy.Integer)
    game_id = sqlalchemy.Column(sqlalchemy.Integer)


class Settings(Base):

    __tablename__ = 'settings'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    participant_name = sqlalchemy.Column(sqlalchemy.String)
    participant_number = sqlalchemy.Column(sqlalchemy.Integer)

engine = sqlalchemy.create_engine(DB_URI)

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
