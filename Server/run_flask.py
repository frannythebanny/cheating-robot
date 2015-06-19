from flask import Flask, request
from flask_restful import Resource, Api, fields
from flask_restful import reqparse, marshal_with, abort
from db import session
import models

game_fields = {

    'word_status': fields.String,
    'guessed_letters': fields.String,
    'game_status': fields.Integer,
    }

parser = reqparse.RequestParser()

parser.add_argument('word_status')
parser.add_argument('guessed_letters')
parser.add_argument('game_status', type=int)

app = Flask(__name__)
api = Api(app)

class GameResource(Resource):

    
    @marshal_with(game_fields)
    def get(self, game_id):

        game = session.query(models.Game).filter(models.Game.game_id == game_id).order_by('-id').first()

        if not game:
            abort(404, message="Could not find that game")

        return game


    @marshal_with(game_fields)
    def put(self, game_id):

        parsed_args = parser.parse_args()
        
        word_status = parsed_args['word_status']
        guessed_letters = parsed_args['guessed_letters']
        game_status = parsed_args['game_status']

        print(word_status)
        print(guessed_letters)
        print(game_status)
        
        game = models.Game(
            game_id=game_id,
            word_status=word_status,
            guessed_letters=guessed_letters,
            game_status=game_status)

        session.add(game)
        session.commit()

        return game

        

class GameListResource(Resource):

    @marshal_with(game_fields)
    def get(self, game_id):

        game = session.query(models.Game).filter(models.Game.game_id == game_id).all()

        if not game:
            abort(404, message="Could not find that game")

        return game

    

# api.add_resource(GameResource, 'games/<int:id>', endpoint=10)
api.add_resource(GameResource, '/<int:game_id>')
api.add_resource(GameListResource, '/games/<int:game_id>')
    
if __name__ == "__main__":
    app.run(port=1234, debug=True)
