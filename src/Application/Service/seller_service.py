from src.Infrastructure.Model.seller_model import SellerRepository
from werkzeug.security import generate_password_hash
from src.Domain.seller import Seller

class SellerService:
    def get_all_sellers_service(self):
        repo = SellerRepository()
        return repo.get_all_model()
    
    @staticmethod
    def create_seller_service(name, cnpj, email, cellphone, password):
        # hashed_password = generate_password_hash(password)
        new_seller_domain = Seller(id = None, name = name, 
                                   cnpj = cnpj, email = email, 
                                   cellphone = cellphone, 
                                   password = password) #Alterar para password=hashed_password se foi criptografar
        
        repo = SellerRepository()
        saved_seller = repo.create_seller_model(new_seller_domain)
        return saved_seller



# # Na hora de salvar:
# hashed_password = generate_password_hash("senha_do_usuario_aqui")
# # Salve o 'hashed_password' no banco usando o Peewee