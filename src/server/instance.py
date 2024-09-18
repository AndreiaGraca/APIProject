from flask import Flask
from flask_restx import Api, Namespace
import os
class Server:
    def __init__(self):
        self.app = Flask(
            __name__,
            template_folder=os.path.join(os.path.dirname(__file__), '../templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '../static')
        )
        self.api = Api(self.app,
                       version='1.0',
                       title='Sample Hotel API',
                       description='Sample Hotel API',
                       doc='/docs')

        # Definir os diferentes namespaces
        self.hotel_ns = Namespace('Hotel', description='Operações relacionadas ao hotel')
        self.reserva_ns = Namespace('Reserva', description='Operações relacionadas à reserva')
        self.room_ns = Namespace('Room', description='Operações relacionadas ao quarto')

        # Adicionar os namespaces ao objeto Api
        self.api.add_namespace(self.hotel_ns)
        self.api.add_namespace(self.reserva_ns)
        self.api.add_namespace(self.room_ns)

    def run(self, ):
        self.app.run(
            debug=True #no deploy fica a false
    )


server= Server()