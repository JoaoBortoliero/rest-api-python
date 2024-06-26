from flask import Flask, jsonify
from flask_restful import Api

from blacklist import BLACKLIST
from resources.hotel import Hotels, Hotel
from resources.user import User, UserRegister, UserLogin, UserLogout

from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def verify_blacklist(self, token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_invalid(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401  # Unauthorized


api.add_resource(Hotels, '/hotels')
api.add_resource(Hotel, '/hotels/<string:hotel_id>')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import database

    database.init_app(app)
    with app.app_context():
        database.create_all()
    app.run(debug=True)
