from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token
from secrets import compare_digest

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank.")
atributos.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank.")


class User(Resource):
    #  /users/{user_id}
    @staticmethod
    def get(user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404  # Not Found

    @staticmethod
    def delete(user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error occurred trying to delete user.'}, 500  # Internal Server Error
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404


class UserRegister(Resource):
    #  /register
    @staticmethod
    def post():
        data = atributos.parse_args()

        if UserModel.find_by_login(data['login']):
            return {'message': f"The login '{data['login']}' already exists."}

        user = UserModel(**data)
        user.save_user()
        return {'message': 'User created successfully!'}, 201  # Created


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = atributos.parse_args()

        user = UserModel.find_by_login(data['login'])
        # safe_str_cmp é uma função segura para comparar strings
        if user and compare_digest(user.password, data['password']):
            acess_token = create_access_token(identity=user.user_id)
            return {'acess_token': acess_token}, 200
        return {'message': 'The username os password is incorrect'}, 401  # unauthorized
