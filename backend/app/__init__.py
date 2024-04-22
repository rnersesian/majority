from flask import Flask, jsonify


def create_app():
    print('heeeu')
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({"message": "Hello World"})
    
    return app

