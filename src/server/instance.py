from flask import Flask, render_template
from flask_restx import Api, Namespace
import os

class Server:
    def __init__(self):
        # Configurar a aplicação Flask:
        self.app = Flask(
            __name__,
            template_folder=os.path.join(os.path.dirname(__file__), '../templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '../static')
        )

        # Configurar a API com Flask-RESTX:
        self.api = Api(self.app,
                       version='1.0',
                       title='Sample Hotel API',
                       description='Sample Hotel API',
                       doc='/docs')

        # Definir os diferentes namespaces:
        self.hotel_ns = Namespace('Hotel', description='Operações relacionadas ao hotel')
        self.reserva_ns = Namespace('Reserva', description='Operações relacionadas à reserva')
        self.room_ns = Namespace('Room', description='Operações relacionadas ao quarto')

        # Adicionar os namespaces ao objeto Api:
        self.api.add_namespace(self.hotel_ns)
        self.api.add_namespace(self.reserva_ns)
        self.api.add_namespace(self.room_ns)

        # Adicionar rotas principais:
        @self.app.route('/start')
        def start():
            return render_template('index.html')

        @self.app.route('/reservas')#para o menu da reservas
        def reservas():
            return render_template('reservas.html')

    def run(self):
        self.app.run(debug=True, use_reloader=False)


server = Server()