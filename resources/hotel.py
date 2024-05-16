from flask_restful import Resource, reqparse

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


class HotelModel:
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade


class Hoteis(Resource):
    @staticmethod
    def get():
        return {'hoteis': hoteis}  # Dicionário / Flask_restful converte para JSON


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    @staticmethod
    def find_by_id(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    @staticmethod
    def get(hotel_id):
        hotel = Hotel.find_by_id(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found.'}, 404  # Not Found

    @staticmethod
    def post(hotel_id):
        dados = Hotel.argumentos.parse_args()
        novo_hotel = {'hotel_id': hotel_id, **dados}
        hoteis.append(novo_hotel)
        return novo_hotel, 200

    @staticmethod
    def put(hotel_id):
        dados = Hotel.argumentos.parse_args()
        novo_hotel = {'hotel_id': hotel_id, **dados}
        hotel = Hotel.find_by_id(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200  # OK
        hoteis.append(novo_hotel)
        return novo_hotel, 201  # 201 = criado

    @staticmethod
    def delete(hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted'}
