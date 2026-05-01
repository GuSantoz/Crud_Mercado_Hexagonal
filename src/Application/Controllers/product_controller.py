from flask import request, jsonify, make_response
from src.Application.Service.product_service import ProductService
from src.Application.Service.user_service import UserService


class ProductController:
    @staticmethod
    def get_all_products():
        token = request.headers.get('Authorization')
        if not token:
            return make_response(jsonify({"erro": "Token não fornecido"}), 401)
        
        token_validation = UserService.validate_token(token)
        if not token_validation["success"]:
            return make_response(jsonify({"erro": token_validation["message"]}), 401) 
        
        user_id = token_validation["user_id"]
        
        # 3. Busca só os produtos dele
        products = ProductService.get_all_products(user_id)

        return make_response(jsonify({
            "mensagem": "Produtos encontrados com sucesso",
            "usuarios": [product.to_dict() for product in products]
        }), 200)
    
    @staticmethod
    def create_product():
        token = request.headers.get('Authorization')
        if not token:
            return make_response(jsonify({"erro": "Token não fornecido"}), 401)
        
        token_validation = UserService.validate_token(token)
        if not token_validation["success"]:
            return make_response(jsonify({"erro": token_validation["message"]}), 401)
        
        user_id = token_validation["user_id"]

        data = request.get_json()
        
        name = data.get('name')
        price = data.get('price')
        quantity = data.get('quantity')
        image = data.get('image')

        if not name or not price or not quantity or not image:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)
 
        product = ProductService.create_product(name, price, quantity, image, user_id)
 
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
    
    @staticmethod
    def create_venda():
        token = request.headers.get('Authorization')
        data = request.get_json()

        if not token:
            return make_response(jsonify({"erro": "Token não fornecido"}), 401)

        if not data:
            return make_response(jsonify({"erro": "Dados para venda não fornecidos"}), 400)

        token_validation = UserService.validate_token(token)
        if not token_validation["success"]:
            return make_response(jsonify({"erro": token_validation["message"]}), 401)

        user_id = token_validation["user_id"]

        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if not product_id or not quantity:
            return make_response(jsonify({"erro": "ID do produto ou quantidade não fornecidos"}), 400)

        result = ProductService.create_venda(user_id, product_id, quantity)

        if result["success"]:
            return make_response(jsonify({
                "mensagem": result["message"],
                "venda": result["venda"]
            }), 201)
        return make_response(jsonify({"erro": result["message"]}), 400)
    
    @staticmethod
    def get_all_vendas():
        token = request.headers.get('Authorization')
        
        if not token:
            return make_response(jsonify({"erro": "Token não fornecido"}), 401)
        
        token_validation = UserService.validate_token(token)
        if not token_validation["success"]:
            return make_response(jsonify({"erro": token_validation["message"]}), 401)
        
        user_id = token_validation["user_id"]
        
        vendas = ProductService.get_all_vendas(user_id)
        
        return make_response(jsonify({
            "mensagem": "Vendas encontradas com sucesso",
            "vendas": [venda.to_dict() for venda in vendas]
        }), 200)
    