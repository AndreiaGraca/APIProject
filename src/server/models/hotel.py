from flask_restx import Namespace, fields

from src.server.instance import server


hotel = server.api.model('Hotel', {
    'number': fields.Integer(required=True, description='O número do Quarto'),
    'capacity': fields.Integer(required=True, description='Capacidade do Quarto'),
    'balcony': fields.Boolean(required=True, description='Se tem varanda'),
    'clean': fields.Boolean(required=True, description='Se está limpo'),
    'hydromassage': fields.Boolean(required=True, description='Se tem hidromassagem'),
})