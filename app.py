from flask import Flask
from flask_restful import Api

from resources.hotel import Hotels, Hotel
from resources.user import User, UserRegister

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

api.add_resource(Hotels, '/hotels')
api.add_resource(Hotel, '/hotels/<string:hotel_id>')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from sql_alchemy import database

    database.init_app(app)
    with app.app_context():
        database.create_all()
    app.run(debug=True)
