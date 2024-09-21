import os
from src.server.instance import server
from src.controllers.hotel import * #importar todos os controllers
from src.controllers.reserva import * 


#app = Flask(__name__, static_folder='src/static', template_folder='src/templates')

if __name__ == '__main__':
    server.run()
    #app.run(debug=True)
