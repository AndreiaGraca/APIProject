from datetime import date

from flask import jsonify
from src.server.models.room import room  # Certifique-se de que Room está no mesmo diretório ou caminho acessível
from src.server.instance import server
from flask_restx import fields
import psycopg2

reserva = server.api.model('Reserva', {
    'name': fields.String(required=True, description='Nome do cliente'),
    'nif': fields.Integer(required=True, description='NIF do cliente'),
    'nights': fields.Integer(required=True, description='Número de noites reservadas'),
    'check_in': fields.Date(required=True, description='Data de check-in'),
    'check_out': fields.Date(required=True, description='Data de check-out'),
    'number_persons': fields.Integer(required=True, description='Número total de pessoas'),
    'room_type': fields.String(required=True, description='Tipo do quarto'),
    'adults': fields.Integer(required=True, description='Número de adultos'),
    'children': fields.Integer(required=True, description='Número de crianças'),
    'children_description': fields.Float(required=False, description='Descrição das crianças (idade)'),
    'pets': fields.Boolean(required=True, description='Se a reserva inclui animais de estimação'),
    'number_of_pets': fields.Integer(required=False, description='Número de animais de estimação'),
    'pet_description': fields.Float(required=False, description='Peso dos animais de estimação'),
    'price_per_night': fields.Float(required=True, description='Preço por noite do quarto'),
    'hydromassage': fields.Boolean(required=True, description='Se o quarto inclui hidromassagem'),
    'romantic_night': fields.Boolean(required=False, description='Se é uma noite romântica'),
    'n_beds': fields.Integer(required=True, description='Número de camas'),
    'email': fields.String(required=True, description='Email do cliente'),
    'room': fields.Integer(required=True, description='Número do quarto')
})


def get_daily_reservations():
    today = date.today()  # Obtém a data atual
    
    # Conexão com a base de dados PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname="postgres",  # Substitua pelo nome do seu banco
            user="postgres",      # Substitua pelo seu usuário
            password="andreia",    # Substitua pela sua senha
            host="localhost",        # Substitua se estiver em outro host
            port="5432"              # Porta padrão do PostgreSQL
        )
        
        cursor = conn.cursor()
        
        # Query para buscar as reservas do dia
        query = "SELECT n_room, reserva_id,name, type, number_persons, n_beds,check_in_made, check_out_made FROM reserve order by n_room"
        cursor.execute(query, (today,))
        
        # Busca todas as reservas do dia
        reservations = cursor.fetchall()
        
        # Fecha o cursor e a conexão
        cursor.close()
        conn.close()
        
        return reservations  # Retorna a lista de reservas
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return []


def get_reserva_by_id_change_bd(reserva_id,value):
    try:
        # Conexão com o banco de dados
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="andreia",
            host="localhost",
            port="5432"
        )
        
        cursor = conn.cursor()

        if(value==0):
           # Query de atualização
            sql = """
            UPDATE reserve
            SET check_in_made = true
            WHERE reserva_id = %s
            """

            # Executa a query
            cursor.execute(sql, (reserva_id,)) 
        elif (value==1):
            sql = """
            UPDATE reserve
            SET check_out_made = true
            WHERE reserva_id = %s
            """

            # Executa a query
            cursor.execute(sql, (reserva_id,)) 
        
        conn.commit()  # Confirma a transação

        # Fecha a conexão
        cursor.close()
        conn.close()

        # Retorna uma mensagem de sucesso ou nenhum valor
        return "Reserva atualizada com sucesso."
    
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

def get_reserva_by_id(reserva_id):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="andreia",
            host="localhost",
            port="5432"
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reserve WHERE reserva_id = %s", (reserva_id,))
        reserva = cursor.fetchone()
        
        cursor.close()
        conn.close()

        return reserva
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None


class Reservation:
    def __init__(self, name: str, nif: int, nights: int, check_in: date, check_out: date, number_persons: int, room_type: str, adults: int, children: int, 
                 children_description: float, pets: bool, number_of_pets: int, pet_description: float, price_per_night: float, hydromassage: bool, 
                 romantic_night: bool, room: int, n_beds: int, email: str):
        self.name = name
        self.nif = nif
        self.nights = nights
        self.check_in = check_in
        self.check_out = check_out
        self.number_persons = number_persons
        self.room_type = room_type
        self.adults = adults
        self.children = children
        self.children_description = children_description
        self.pets = pets
        self.number_of_pets = number_of_pets
        self.pet_description = pet_description
        self.price_per_night = price_per_night
        self.hydromassage = hydromassage
        self.romantic_night = romantic_night
        self.room = room
        self.n_beds = n_beds
        self.check_in_made = False
        self.check_out_made = False
        self.paid = False
        self.reservation_date = date.today()
        self.canceled = False
        self.email = email
        self.total_price = self.calculate_total_price()

    def calculate_total_price(self):
        # Calcula o preço total com base no número de noites e preço por noite
        total = self.nights * self.price_per_night
        # Adicione lógica adicional de preço aqui (pets, crianças, etc.)
        if self.pets:
            total += self.number_of_pets * self.pet_description  # Exemplo de cálculo para animais de estimação
        return total

    # Getters e Setters (não são necessários explicitamente em Python, mas incluí para manter a estrutura semelhante à Java)
    def get_name(self) -> str:
        return self.name

    def get_nif(self) -> int:
        return self.nif

    def set_email(self, email: str):
        self.email = email

    def get_email(self) -> str:
        return self.email

    def get_total_price(self) -> float:
        return self.total_price

    def get_nights(self) -> int:
        return self.nights

    def get_check_in(self) -> date:
        return self.check_in

    def get_check_out(self) -> date:
        return self.check_out

    def get_reservation_date(self) -> date:
        return self.reservation_date

    def is_canceled(self) -> bool:
        return self.canceled

    def get_number_persons(self) -> int:
        return self.number_persons

    def get_room_type(self) -> str:
        return self.room_type

    def get_adults(self) -> int:
        return self.adults

    def get_children(self) -> int:
        return self.children

    def get_children_description(self) -> float:
        return self.children_description

    def is_pets(self) -> bool:
        return self.pets

    def get_number_of_pets(self) -> int:
        return self.number_of_pets

    def get_pet_description(self) -> float:
        return self.pet_description

    def get_price_per_night(self) -> float:
        return self.price_per_night

    def is_hydromassage(self) -> bool:
        return self.hydromassage

    def is_romantic_night(self) -> bool:
        return self.romantic_night

    def get_room(self) -> int:
        return self.room

    def get_n_beds(self) -> int:
        return self.n_beds

    def is_check_in_made(self) -> bool:
        return self.check_in_made

    def is_check_out_made(self) -> bool:
        return self.check_out_made

    def is_paid(self) -> bool:
        return self.paid

    def set_paid(self, paid: bool):
        self.paid = paid

    def set_canceled(self, canceled: bool):
        self.canceled = canceled

    def __str__(self):
        return f"\n*** Reserve Number: {self.get_nif()} ***" + \
               f"\n\tClient Name: {self.get_name()}" + \
               f"\n\tIs Canceled: {self.is_canceled()}" + \
               f"\n\tTotal Price: {self.get_total_price()}" + \
               f"\n\tPrice per Night: {self.get_price_per_night()}" + \
               f"\n\tNights: {self.get_nights()}" + \
               f"\n\tCheck-In: {self.get_check_in()}" + \
               f"\n\tCheck-Out: {self.get_check_out()}" + \
               f"\n\tIs Paid: {self.is_paid()}" + \
               f"\n\tAdults: {self.get_adults()}" + \
               f"\n\tChildren: {self.get_children()}" + \
               f"\n\tPets: {self.get_number_of_pets()} -- Price: {self.get_pet_description()}" + \
               f"\n\tNumber of Beds: {self.get_n_beds()}" + \
               f"\n\tHydromassage: {self.is_hydromassage()}" + \
               f"\n\tRomantic: {self.is_romantic_night()}" + \
               f"\n\t{self.get_room()}" + \
               f"\nCheck-In Made: {self.is_check_in_made()}" + \
               f"\nCheck-Out Made: {self.is_check_out_made()}\n"


