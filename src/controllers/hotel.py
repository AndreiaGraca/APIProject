from flask import Flask, jsonify, render_template, request
from flask_restx import Api, Namespace, Resource
from src.server.instance import server
from src.server.models.hotel import hotel
from src.server.models.reserva import get_daily_reservations, get_reserva_by_id, get_reserva_by_id_change_bd

app, api = server.app, server.api

quartos_db = [
    {'number': 1, 'capacity': "2", 'balcony':'true', 'clean': 'true', 'hydromassage':'true'},
    {'number': 2, 'capacity': "2", 'balcony':'true', 'clean': 'true', 'hydromassage':'true'},
    {'number': 3, 'capacity': "2", 'balcony':'true', 'clean': 'true', 'hydromassage':'false'},
    {'number': 4, 'capacity': "2", 'balcony':'true', 'clean': 'true', 'hydromassage':'false'},
    {'number': 5, 'capacity': "4", 'balcony':'true', 'clean': 'true', 'hydromassage':'true'},
    {'number': 6, 'capacity': "4", 'balcony':'true', 'clean': 'true', 'hydromassage':'true'},
    {'number': 7, 'capacity': "6", 'balcony':'true', 'clean': 'true', 'hydromassage':'true'},
    {'number': 8, 'capacity': "6", 'balcony':'true', 'clean': 'true', 'hydromassage':'true'},
    {'number': 9, 'capacity': "8", 'balcony':'true', 'clean': 'true', 'hydromassage':'true'},
    {'number': 10, 'capacity': "8", 'balcony':'true', 'clean': 'true', 'hydromassage':'true'},
]

hotel_ns = server.hotel_ns

#aprender Swagger
@hotel_ns.route('/hotel')
class HotelList(Resource):
    @hotel_ns.marshal_list_with(hotel)
    def get(self):
        return quartos_db
    
    #adiciona um quarto ao hotel
    @hotel_ns.expect(hotel,validate=True)
    @hotel_ns.marshal_list_with(hotel)
    def post(self,):
        response= api.payload
        quartos_db.append(response)
        return response, 201 #codigo de sucesso na inserção
    
    #apagar um quarto
    @hotel_ns.param('number', 'Número do Quarto a ser removido', type='int')
    @hotel_ns.response(204, 'Quarto removido com sucesso')
    @hotel_ns.response(404, 'Quarto não encontrado')
    def delete(self):
        number = request.args.get('number', type=int)  # Obtém o número do quarto 
        global quartos_db
        if number is None:
            return {'message': 'Número do quarto não fornecido'}, 400  # Retorna erro se o número não for fornecido
        
        for i, quarto in enumerate(quartos_db):
            if quarto['number'] == number:
                del quartos_db[i]
                return '', 204  # Código de sucesso na remoção
        return {'message': 'Quarto não encontrado'}, 404  # Retorna erro se o quarto não for encontrado
    

    @hotel_ns.param('number', 'Número do Quarto a ser atualizado', type='int')
    @hotel_ns.expect(hotel, validate=True)
    @hotel_ns.marshal_with(hotel)
    @hotel_ns.response(200, 'Quarto atualizado com sucesso')
    @hotel_ns.response(404, 'Quarto não encontrado')
    @hotel_ns.response(400, 'Número do quarto não fornecido ou dados inválidos')
    def put(self):
        number = request.args.get('number', type=int)
        if number is None:
            return {'message': 'Número do quarto não fornecido'}, 400
        
        data = api.payload
        global quartos_db
        
        for i, quarto in enumerate(quartos_db):
            if quarto['number'] == number:
                quartos_db[i].update(data)
                return quartos_db[i], 200
        return {'message': 'Quarto não encontrado'}, 404
    

#retornar todas as reservas que se encontram na base de dados
    @app.route('/api/reservas-dia', methods=['GET'])
    def reservas_dia():
        reservas = get_daily_reservations()
        return jsonify(reservas)
    
    @app.route('/api/reserva/<int:reserva_id>', methods=['GET'])
    def reserva(reserva_id):
        reserva = get_reserva_by_id(reserva_id)
        if reserva:
            return jsonify(reserva)
        else:
            return jsonify({'error': 'Reserva não encontrada'}), 404
        
    @app.route('/api/reserva/check/<int:reserva_id>', methods=['POST'])
    #para o check_in e o check_out apenas muda o valor 0/1 respetivamente
    def check(reserva_id):
        value = request.args.get('value', default=0, type=int) 

        reserva = get_reserva_by_id_change_bd(reserva_id, value)
        return jsonify(success=True), 200