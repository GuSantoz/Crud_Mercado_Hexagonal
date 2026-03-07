from flask import jsonify, request, make_response
from src.Application.Service.seller_service import SellerService
# from src.Domain.seller import to_dict

def get_all_sellers_controller():
    service = SellerService()
    sellers = service.get_all_sellers_service()
    return jsonify([seller.to_dict() for seller in sellers]), 200

def create_seller_controller():
    data = request.get_json()
    name = data.get("name")
    cnpj = data.get("cnpj")
    email = data.get("email")
    cellphone = data.get("cellphone")
    password = data.get("password")
    service = SellerService()
    seller_criado = service.create_seller_service(name, cnpj, email,cellphone, password)
    return jsonify(seller_criado.to_dict()), 201