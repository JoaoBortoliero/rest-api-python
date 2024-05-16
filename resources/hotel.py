from flask_restful import Resource, reqparse

from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'Curitiba'
    },
    {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 3.9,
        'diaria': 290.00,
        'cidade': 'São Paulo'
    },
    {
        'hotel_id': 'bellagio',
        'nome': 'Bellagio Hotel',
        'estrelas': 4.9,
        'diaria': 600.00,
        'cidade': 'Las Vegas'
    }
]


class Hoteis(Resource):
    @staticmethod
    def get():
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome')
    atributos.add_argument('estrelas')
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    @staticmethod
    def get(hotel_id):
        hotel = HotelModel.find_by_id(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404  # Not Found

    @staticmethod
    def post(hotel_id):
        if HotelModel.find_by_id(hotel_id):
            return {"message": f"Hotel id '{hotel_id}' already exists."}, 400  # Bad request

        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json()

    @staticmethod
    def put(hotel_id):
        dados = Hotel.atributos.parse_args()
        hotel_located = HotelModel.find_by_id(hotel_id)
        if hotel_located:
            hotel_located.update_hotel(**dados)
            hotel_located.save_hotel()
            return hotel_located.json(), 200  # OK
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201  # 201 = criado

    @staticmethod
    def delete(hotel_id):
        hotel = HotelModel.find_by_id(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404
