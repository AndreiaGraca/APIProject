from src.server.instance import server
from flask_restx import Namespace, fields

class Room:
    def __init__(self, number: int, capacity: int, balcony: bool, clean: bool, hydromassage: bool, room_type='SINGLE'):
        self.occupied = False
        self.number = number
        self.capacity = capacity
        self.type = room_type
        self.balcony = balcony
        self.price_per_night = self.get_price_per_night(room_type)
        self.clean = clean
        self.hydromassage = hydromassage

    def get_price_per_night(self, room_type):
        # Simulando preços baseados no tipo de quarto
        prices = {
            'SINGLE': 50.0,
            'DOUBLE': 75.0,
            'SUITE': 120.0
        }
        return prices.get(room_type, 50.0)

    def is_occupied(self) -> bool:
        return self.occupied

    def get_number(self) -> int:
        return self.number

    def get_capacity(self) -> int:
        return self.capacity

    def get_type(self) -> str:
        return self.type

    def has_balcony(self) -> bool:
        return self.balcony

    def get_price_per_night(self) -> float:
        return self.price_per_night

    def is_clean(self) -> bool:
        return self.clean

    def has_hydromassage(self) -> bool:
        return self.hydromassage

    def set_occupied(self, occupied: bool):
        self.occupied = occupied

    def set_capacity(self, capacity: int):
        self.capacity = capacity

    def set_type(self, room_type: str):
        self.type = room_type
        self.price_per_night = self.get_price_per_night(room_type)

    def set_clean(self, clean: bool):
        self.clean = clean

    def set_hydromassage(self, hydromassage: bool):
        self.hydromassage = hydromassage

    def chooses(self, choice: bool) -> str:
        return "Yes" if choice else "No"

    def __str__(self):
        return f"Room Number: {self.get_number()}" + \
               f"\n\t\tOccupied: {self.chooses(self.is_occupied())}" + \
               f"\n\t\tCapacity: {self.get_capacity()}" + \
               f"\n\t\tRoom Type: {self.get_type()}" + \
               f"\n\t\tBalcony: {self.chooses(self.has_balcony())}" + \
               f"\n\t\tPrice per Night: {self.get_price_per_night():.1f}" + \
               f"\n\t\tClean: {self.chooses(self.is_clean())}" + \
               f"\n\t\tHydromassage: {self.chooses(self.has_hydromassage())}"


room = server.api.model('Room', {
    'number': fields.Integer(required=True, description='Número do quarto'),
    'capacity': fields.Integer(required=True, description='Capacidade do quarto'),
    'balcony': fields.Boolean(required=True, description='Se o quarto tem varanda'),
    'clean': fields.Boolean(required=True, description='Se o quarto está limpo'),
    'hydromassage': fields.Boolean(required=True, description='Se o quarto tem hidromassagem'),
    'type': fields.String(required=True, description='Tipo do quarto (casal, duplo, etc.)'),
    'price_per_night': fields.Float(required=True, description='Preço por noite'),
    'occupied': fields.Boolean(required=True, description='Ocupado'),
})