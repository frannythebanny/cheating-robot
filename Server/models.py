import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from settings import DB_URI

Base = declarative_base()

class Game(Base):

    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    word_status = sqlalchemy.Column(sqlalchemy.String)
    guessed_letters = sqlalchemy.Column(sqlalchemy.String)
    game_status = sqlalchemy.Column(sqlalchemy.Integer)
    game_id = sqlalchemy.Column(sqlalchemy.Integer)


engine = sqlalchemy.create_engine(DB_URI)

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
