from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
client = MongoClient(
    host="mongodb+srv://dillmaster:aDm1N4P!@macro-tracker.5orft.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


@app.route('/')
def ready():
    return 'ready'


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(host='localhost', port=3002)
