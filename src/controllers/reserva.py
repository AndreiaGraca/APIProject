from flask import Flask, jsonify, render_template, request
from flask_restx import Api, Namespace, Resource
from src.server.instance import server
from src.server.models.reserva import get_daily_reservations, reserva
from datetime import datetime 
app, api = server.app, server.api
reserva_ns=server.reserva_ns

reservas=[]

@reserva_ns.route('/reservas-dia')
class ReservasDia(Resource):
    def get(self):
        reservas = get_daily_reservations()
        return jsonify(reservas)
    
@reserva_ns.route('/reserva')
class ReservasList(Resource):
    @reserva_ns.marshal_list_with(reserva) #formata a saída com base num modelo Reserva
    def get(self): #retorna todas as reservas
        return reservas
    
    #adiciona uma reserva ao hotel
    @reserva_ns.expect(reserva,validate=True) # o corpo da requisição deve estar de acordo com o modelo Reserva. e os dados devem ser validados
    @reserva_ns.marshal_list_with(reserva)
    def post(self,):
        response= api.payload # o corpo do pedido JSON (enviado pelo cliente) é recuperado e armazenado em RESPONSE
        reservas.append(response)
        return response, 201 #codigo de sucesso na inserção
    
    #apaga uma reserva
    @reserva_ns.param('name', 'Nome da Reserva', type='string')
    @reserva_ns.param('check_in', 'CheckIn da Reserva', type='string')###################333
    @reserva_ns.param('check_out', 'CkeckOut da Reserva', type='string')##############33
    @reserva_ns.response(204, 'Reserva removida com sucesso')
    @reserva_ns.response(404, 'Reserva não encontrada')
    def delete(self):
        name = request.args.get('name')  # Obtém o nome da reserva 
        check_in = request.args.get('check_in')  # Obtém o check-in como string
        check_out = request.args.get('check_out')  # Obtém o check-out como string
        
        global reservas
        if not name or not check_in or not check_out:
            return {'message': 'Nome da reserva ou datas não fornecidos'}, 400  # Validação dos parâmetros
        
        # Converte as strings de data para objetos datetime.date
        
        # Agora, percorremos a lista de reservas e comparamos os objetos de data corretamente
        for i, r in enumerate(reservas):
            # Supondo que 'r' seja uma instância da classe Reservation
            print(r['name'])
            print(type(r['check_in']))
            print(r['check_out'])
            if r['name'] == name and r['check_in'] == check_in and r['check_out'] == check_out:
                del reservas[i]  # Remove a reserva encontrada
                return '', 204  # Remoção bem-sucedida
        
        return {'message': 'Reserva não encontrada'}, 404  # Reserva não encontrada
    

    @reserva_ns.param('name', 'Nome da Reserva', type='string')
    @reserva_ns.param('check_in', 'CheckIn da Reserva', type='string')###################333
    @reserva_ns.param('check_out', 'CkeckOut da Reserva', type='string')##############33
    @reserva_ns.response(204, 'Reserva removida com sucesso')
    @reserva_ns.response(404, 'Reserva não encontrada')
    @reserva_ns.response(400, 'Reseerva não fornecido ou dados inválidos')
    @reserva_ns.marshal_list_with(reserva)
    @reserva_ns.expect(reserva, validate=True)
    def put(self):
        name = request.args.get('name')  # Obtém o nome da reserva 
        check_in = request.args.get('check_in')  # Obtém o check-in como string
        check_out = request.args.get('check_out')  # Obtém o check-out como string
        global reservas
        if not name or not check_in or not check_out:
            return {'message': 'Nome da reserva ou datas não fornecidos'}, 400  # Validação dos parâmetros
        
        # Converte as strings de data para objetos datetime.date
        data = api.payload
        # Agora, percorremos a lista de reservas e comparamos os objetos de data corretamente
        for i, r in enumerate(reservas):
            # Supondo que 'r' seja uma instância da classe Reservation
            print(r['name'])
            print(type(r['check_in']))
            print(r['check_out'])
            if r['name'] == name and r['check_in'] == check_in and r['check_out'] == check_out:
                reservas[i].update(data)
                return reservas[i], 200
        return {'message': 'Reserva não encontrado'}, 404
        

