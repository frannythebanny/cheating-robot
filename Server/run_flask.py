from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

games = {}

class GameResource(Resource):

    def get(self, game_id):
        return {"word_status" : games[game_id]}

    def put(self, game_id):
        games[game_id] = request.form['data']
        return {"word_status" : games[game_id]}
        
api.add_resource(GameResource, '/<string:game_id>')
    
if __name__ == "__main__":
    app.run(port=1234, debug=True)
