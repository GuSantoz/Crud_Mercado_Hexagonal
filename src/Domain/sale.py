class SaleDomain:
    def __init__(self, id, product_id, product_name, quantity, price, total_price, user_id, created_at):
        self.id = id
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
        self.total_price = total_price
        self.user_id = user_id
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "price": float(self.price) if self.price is not None else 0.0,
            "total_price": float(self.total_price) if self.total_price is not None else 0.0,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
