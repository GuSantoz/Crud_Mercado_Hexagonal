class UserDomain:
    def __init__(self, id, name, email, password, phone=None, status=False, activation_code=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.status = status
        self.activation_code = activation_code
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "status": self.status,
            "activation_code": self.activation_code
        }
