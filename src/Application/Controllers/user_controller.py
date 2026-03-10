from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def register_user(): #Nome, CNPJ, E-mail, Celular, Senha, Status(Padrão: Inativo)
        data = request.get_json()
        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email')
        phone = data.get('cellphone')  # Usando 'cellphone' conforme o JSON do usuário
        password = data.get('password')
        status = False

        if not name or not email or not password:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)

        user = UserService.create_user(name, email, password, phone)
        return make_response(jsonify({
            "mensagem": "User salvo com sucesso",
            "usuarios": user.to_dict()
        }), 200)

    @staticmethod
    def activate_user():
        data = request.get_json()
        email = data.get('email')
        activation_code = data.get('activation_code')

        if not email or not activation_code:
            return make_response(jsonify({"erro": "Email e código de ativação são obrigatórios"}), 400)

        success = UserService.activate_user(email, activation_code)
        if success:
            return make_response(jsonify({"mensagem": "Conta ativada com sucesso"}), 200)
        else:
            return make_response(jsonify({"erro": "Código de ativação inválido ou usuário não encontrado"}), 400)
