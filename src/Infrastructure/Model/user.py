from peewee import Model, CharField, AutoField, IntegerField, BooleanField
from src.Infrastructure.Model.seller_model import db

class User(Model):
    id = AutoField()
    name = CharField(null=False)
    email = CharField(unique=True, null=False)
    password = CharField(null=False)
    phone = CharField(null=True)
    status = BooleanField(default=False)
    activation_code = CharField(null=True)

    class Meta:
        database = db
        table_name = 'users'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "status": self.status,
            "activation_code": self.activation_code
        }
