from flask import Flask
from database.db import initialize_db
from flask_restful import Api
from flask_bcrypt import Bcrypt
from resources.jwt_manger import initialize_jwt
from routes import initialize_routes
from flask_socketio import SocketIO

# TODO: marshmallow validation of IO
# TODO: Generate Swagger


app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')

api = Api(app)
bcrypt = Bcrypt(app)
socketIO = SocketIO(app)

initialize_jwt(app)
initialize_db(app)

initialize_routes(api)

if __name__ == '__main__':
    # app.run(debug=True)
    socketIO.run(app, debug=True, host='0.0.0.0')
