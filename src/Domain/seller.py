class Seller:
    def __init__(self, id, name, cnpj, email, cellphone, password, status = False):
        self.id = id
        self.name = name
        self.cnpj = cnpj
        self.email = email
        self.cellphone = cellphone
        self.password = password
        self.status = status

    def to_dict(self):
        return {"id": self.id, "name": self.name,
                "cnpj": self.cnpj,  "email": self.email,
                "cellphone": self.cellphone, 
                "status": self.status}