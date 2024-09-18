from flask import Flask, render_template, request
from flask_restx import Api, Namespace, Resource
from src.server.instance import server
from src.server.models.reserva import reserva

app, api = server.app, server.api
reserva_ns=server.reserva_ns

reservas=[]

@reserva_ns.route('/reserva')
class ReservasList(Resource):
    @reserva_ns.marshal_list_with(reserva)
    def get(self): 
        return reservas
    
    #adiciona uma reserva ao hotel
    @reserva_ns.expect(reserva,validate=True)
    @reserva_ns.marshal_list_with(reserva)
    def post(self,):
        response= api.payload
        reservas.append(response)
        return response, 201 #codigo de sucesso na inserção