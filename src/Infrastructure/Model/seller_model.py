from peewee import Model, CharField, AutoField, IntegerField, MySQLDatabase
import os
from src.Domain.seller import Seller

# Conexão usando as variáveis do seu docker-compose
db = MySQLDatabase(
    os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=3306
)

class SellerModel(Model):
    id = AutoField()
    name = CharField()
    cnpj = IntegerField()
    email = CharField(unique=True)
    cellphone = IntegerField()
    password = CharField(max_length=255)

    class Meta:
        database = db
        table_name = 'sellers'

class SellerRepository:
    def get_all_model(self):
        # Busca no MySQL e converte para a Entidade do Domain
        query = SellerModel.select()
        return [Seller(id=s.id, name=s.name, cnpj=s.cnpj, email=s.email, cellphone=s.cellphone, password=s.password) for s in query]
    
    def create_seller_model(self, seller: Seller):
        new_seller = SellerModel.create(
            name = seller.name,
            cnpj = seller.cnpj,
            email = seller.email,
            cellphone = seller.cellphone,
            password = seller.password
        )
        seller.id = new_seller.id
        return seller