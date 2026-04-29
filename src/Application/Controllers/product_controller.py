import os
from flask import request, jsonify, make_response
from werkzeug.utils import secure_filename
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
        name = None
        price = None
        quantity = None
        image = None

        if request.content_type and 'multipart/form-data' in request.content_type:
            name = request.form.get('name')
            price = request.form.get('price')
            quantity = request.form.get('quantity')
            image_file = request.files.get('image')

            if image_file:
                filename = secure_filename(image_file.filename)
                # Use absolute path from the app root
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                uploads_dir = os.path.join(base_dir, 'uploads')
                os.makedirs(uploads_dir, exist_ok=True)
                image_path = os.path.join(uploads_dir, filename)
                image_file.save(image_path)
                # Store just the filename for database
                image = filename
        else:
            data = request.get_json() or {}
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

        if not token:
            return make_response(jsonify({"erro": "Token não fornecido"}), 401)

        token_validation = UserService.validate_token(token)
        if not token_validation["success"]:
            return make_response(jsonify({"erro": token_validation["message"]}), 401)

        data = {}
        product_id = None

        if request.content_type and 'multipart/form-data' in request.content_type:
            product_id = request.form.get('id')
            data['name'] = request.form.get('name')
            data['price'] = request.form.get('price')
            data['quantity'] = request.form.get('quantity')
            data['status'] = request.form.get('status') == 'true'
            
            image_file = request.files.get('image')
            if image_file:
                filename = secure_filename(image_file.filename)
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                uploads_dir = os.path.join(base_dir, 'uploads')
                os.makedirs(uploads_dir, exist_ok=True)
                image_path = os.path.join(uploads_dir, filename)
                image_file.save(image_path)
                data['image'] = filename
            else:
                data['image'] = request.form.get('image')
        else:
            data = request.get_json() or {}
            product_id = data.get('id')

        if not product_id:
            return make_response(jsonify({"erro": "ID do produto não fornecido"}), 400)

        if not data:
            return make_response(jsonify({"erro": "Dados para atualização não fornecidos"}), 400)

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
    def delete_product(product_id):
        token = request.headers.get('Authorization')

        if not token:
            return make_response(jsonify({"erro": "Token não fornecido"}), 401)

        token_validation = UserService.validate_token(token)
        if not token_validation["success"]:
            return make_response(jsonify({"erro": token_validation["message"]}), 401)

        if not product_id:
            return make_response(jsonify({"erro": "ID do produto não fornecido"}), 400)

        result = ProductService.delete_product(product_id)

        if result["success"]:
            return make_response(jsonify({"mensagem": result["message"]}), 200)
        else:
            return make_response(jsonify({"erro": result["message"]}), 400)