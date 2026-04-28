from flask import request, jsonify, make_response
from src.Application.Service.product_service import ProductService
from src.Application.Service.user_service import UserService


class ProductController:
    @staticmethod
    def get_all_products():
        products = ProductService.get_all_products()
        return make_response(jsonify({
            "mensagem": "Produtos encontrados com sucesso",
            "usuarios": [product.to_dict() for product in products]
        }), 200)
    
    @staticmethod
    def create_product():
        data = request.get_json()
        
        name = data.get('name')
        price = data.get('price')
        quantity = data.get('quantity')
        image = data.get('image')

        if not name or not price or not quantity or not image:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)
 
        product = ProductService.create_product(name, price, quantity, image)
 
        if not product["success"]:
            return make_response(jsonify({"erro": product["message"]}), 400)
 
        productDomain = product["produto"]

        return make_response(
            jsonify({
                "message": "Produto cadastrado com sucesso!",
                "produto": productDomain.to_dict()
            }), 201
        )
    
    @staticmethod
    def update_product():
        token = request.headers.get('Authorization')
        data = request.get_json()

        if not token:
            return make_response(jsonify({"erro": "Token não fornecido"}), 401)

        if not data:
            return make_response(jsonify({"erro": "Dados para atualização não fornecidos"}), 400)

        token_validation = UserService.validate_token(token)
        if not token_validation["success"]:
            return make_response(jsonify({"erro": token_validation["message"]}), 401)

        product_id = data.get('id')
        if not product_id:
            return make_response(jsonify({"erro": "ID do produto não fornecido"}), 400)

        result = ProductService.update_product(product_id, data)

        if result["success"]:
                return make_response(jsonify({"mensagem": result["message"]}), 200)
        else:
                return make_response(jsonify({"erro": result["message"]}), 400)


    @staticmethod
    def update_status_product():
        token = request.headers.get('Authorization')
        data = request.get_json()

        if not token:
            return make_response(jsonify({"erro": "Token não fornecido"}), 401)

        if not data:
            return make_response(jsonify({"erro": "Dados para atualização não fornecidos"}), 400)

        token_validation = UserService.validate_token(token)
        if not token_validation["success"]:
            return make_response(jsonify({"erro": token_validation["message"]}), 401)

        product_id = data.get('id')
        if not product_id:
            return make_response(jsonify({"erro": "ID do produto não fornecido"}), 400)

        if 'status' not in data:
            return make_response(jsonify({"erro": "Status não fornecido"}), 400)

        result = ProductService.update_product(product_id, {"status": data.get('status')})

        if result["success"]:
            return make_response(jsonify({"mensagem": result["message"]}), 200)
        return make_response(jsonify({"erro": result["message"]}), 400)