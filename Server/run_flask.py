from flask import Flask, request
from flask_restful import Resource, Api, fields
from flask_restful import reqparse, marshal_with, abort
from db import session
import models

game_fields = {

    'word_status': fields.String,
    'wrong_letters': fields.String,
    'num_wrong_letters': fields.Integer,
    'game_status': fields.Integer

    }


settings_fields = {

    'participant_number': fields.Integer,
    'participant_name': fields.String,
    'game_variant': fields.Integer,
    'condition': fields.Integer
    
}

parser = reqparse.RequestParser()

parser.add_argument('word_status')
parser.add_argument('wrong_letters')
parser.add_argument('num_wrong_letters', type=int)
parser.add_argument('game_status', type=int)


settings_parser = reqparse.RequestParser()
settings_parser.add_argument('participant_name')
settings_parser.add_argument('participant_number', type=int)
settings_parser.add_argument('game_variant', type=int)
settings_parser.add_argument('condition', type=int)

app = Flask(__name__)
api = Api(app)

host_ip ='192.168.0.101'
#host_ip ='145.94.155.239' #if not specified at bottom, localhost is used
host_port = 1235 #if not using localhost and accessing from within, make sure to open port (e.g. Windows firewall)

class GameResource(Resource):

    
    @marshal_with(game_fields)
    def get(self, game_id):

        # Return last entry
        game = session.query(models.Game).filter(models.Game.game_id == game_id).order_by('-id').first()

        if not game:
            abort(404, message="Could not find that game")

        return game


    @marshal_with(game_fields)
    def put(self, game_id):

        parsed_args = parser.parse_args()
        
        word_status = parsed_args['word_status']
        wrong_letters = parsed_args['wrong_letters']
        num_wrong_letters = parsed_args['num_wrong_letters']
        game_status = parsed_args['game_status']
        
        game = models.Game(
            game_id=game_id,
            word_status=word_status,
            wrong_letters=wrong_letters,
            num_wrong_letters=num_wrong_letters,
            game_status=game_status)

        session.add(game)
        session.commit()

        return game

        

class GameListResource(Resource):

    @marshal_with(game_fields)
    def get(self, game_id):

        # Return list of game states
        game = session.query(models.Game).filter(models.Game.game_id == game_id).all()

        if not game:
            abort(404, message="Could not find that game")

        return game

class SettingsResource(Resource):

    @marshal_with(settings_fields)
    def get(self):

        settings = session.query(models.Settings).order_by('-id').first()

        if not settings:
            abort(404, message="Could not find any settings")

        return settings

    @marshal_with(settings_fields)
    def put(self):

        print('I\'m here')

        parsed_args = settings_parser.parse_args()

        print("parsed_args are", parsed_args)

        participant_name = parsed_args['participant_name']
        participant_number = parsed_args['participant_number']
        game_variant = parsed_args['game_variant']
        condition = parsed_args['condition']


        settings = models.Settings(
            participant_name=participant_name,
            participant_number=participant_number,
            game_variant=game_variant,
            condition=condition)

        session.add(settings)
        session.commit()

        return settings


class SettingsListResource(Resource):

    @marshal_with(settings_fields)
    def get(self):

        settings = session.query(models.Settings).all()

        if not settings:
            abort(404, message="Could not find any settings")

        return settings



# api.add_resource(GameResource, 'games/<int:id>', endpoint=10)
api.add_resource(GameResource, '/<int:game_id>')
api.add_resource(GameListResource, '/games/<int:game_id>')
api.add_resource(SettingsResource, '/settings')
api.add_resource(SettingsListResource, '/allsettings')
    
if __name__ == "__main__":
    app.run(host=host_ip, port=host_port, debug=True)
