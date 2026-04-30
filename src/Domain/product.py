class ProductDomain:
    def __init__(self, id, name, price, quantity, status, image, userId):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.status = status
        self.image = image
        self.userId = userId
        
        

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": float(self.price) if self.price is not None else 0.0,
            "quantity": self.quantity,
            "status": self.status,
            "image": self.image,
            "userid": self.userId
        }