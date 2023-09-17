import os

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Bird

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Index(Resource):
    def get(self):
        return make_response({'message': 'Welcome home!'}, 200)

class Birds(Resource):

    def get(self):
        birds = [bird.to_dict() for bird in Bird.query.all()]
        return make_response(jsonify(birds), 200)
    
class BirdByID(Resource):
    def get(self, id):
        bird = Bird.query.filter_by(id=id).first()
        return make_response(jsonify(bird), 200)

api.add_resource(Index, '/')
api.add_resource(Birds, '/birds')
api.add_resource(BirdByID, '/birds/<int:id>')

if __name__ == '__main__':
    # Check if DATABASE_URI is set
    if os.getenv('DATABASE_URI'):
        print("DATABASE_URI is set properly.")
    else:
        print("DATABASE_URI is not set.")

    app.run()