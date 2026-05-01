from src.Domain.product import ProductDomain
from src.Domain.sale import SaleDomain
from src.Infrastructure.Model.product import Product
from src.Infrastructure.Model.sale import Sale
from src.config.data_base import db
from datetime import datetime

class ProductService:
    def get_all_products(user_id):
        products = db.session.query(Product).filter(Product.user_id == user_id).all()
        return [ProductDomain(product.id, product.name, product.price, product.quantity, product.status, product.image, product.user_id)for product in products]
    
    @staticmethod
    def create_product(name, price, quantity, image, user_id):
        if db.session.query(Product).filter(Product.name == name, Product.user_id == user_id).first():
            return {"success": False, "message": "Já há um produto cadastrado com esse nome!"}
        
        product = Product(name=name, price=price, quantity=quantity, image=image, user_id=user_id)
        db.session.add(product)
        db.session.commit()
 
        product = ProductDomain(
            product.id, product.name, product.price, 
            product.quantity, product.status, product.image, product.user_id
        )

        return {
            "success": True,
            "produto": product
        }
    
    # def update_product(product_id, data):
    #     product = db.session.query(Product).filter(Product.id == product_id).first()
    #     if not product:
    #         return {"success": False, "message": "Produto não encontrado!"}
        
    #     if 'name' in data:
    #         product.name = data['name']
    #     if 'image' in data:
    #         product.image = data['image']
    #     if 'price' in data:
    #         product.price = data['price']
    #     if 'quantity' in data:
    #         product.quantity = data['quantity']
    #         if product.quantity == 0:
    #             product.status = False
    #     if 'status' in data:
    #         product.status = data['status']

    #     try:
    #         db.session.commit()
    #         return {"success": True, "message": "Informações do produto atualizadas com sucesso."}
    #     except Exception as e:
    #         db.session.rollback()
    #         return {"success": False, "message": f"Erro ao atualizar o banco de dados: {str(e)}"}
    
    @staticmethod
    def update_product(product_id, data):
        product = db.session.query(Product).filter(Product.id == product_id).first()
        if not product:
            return {"success": False, "message": "Produto não encontrado!"}
        
        if 'name' in data:
            product.name = data['name']
        if 'image' in data:
            product.image = data['image']
        if 'price' in data:
            product.price = data['price']
            
        # 1. PRIMEIRO: Atualiza o status caso o front-end tenha enviado (ex: botão de inativar manualmente)
        if 'status' in data:
            product.status = data['status']

        # 2. POR ÚLTIMO: Aplica a regra matemática do estoque. 
        # Isso garante que se houver alteração de quantidade, essa regra tem prioridade máxima!
        if 'quantity' in data:
            nova_quantidade = int(data['quantity'])
            product.quantity = nova_quantidade
            
            if nova_quantidade <= 0:
                product.status = False
            else:
                product.status = True

        try:
            db.session.commit()
            return {"success": True, "message": "Informações do produto atualizadas com sucesso."}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Erro ao atualizar o banco de dados: {str(e)}"}

    @staticmethod
    def create_venda(user_id, product_id, quantity):
        try:
            # Busca o produto
            product = db.session.query(Product).filter(Product.id == product_id, Product.user_id == user_id).first()
            
            if not product:
                return {"success": False, "message": "Produto não encontrado!"}
            
            # Verifica se tem quantidade suficiente
            if product.quantity < quantity:
                return {"success": False, "message": f"Quantidade insuficiente! Disponível: {product.quantity}"}
            
            # Calcula o preço total
            total_price = float(product.price) * quantity
            
            # Cria a venda
            sale = Sale(
                product_id=product.id,
                product_name=product.name,
                quantity=quantity,
                price=product.price,
                total_price=total_price,
                user_id=user_id
            )
            
            # Reduz a quantidade do produto
            product.quantity -= quantity
            if product.quantity == 0:
                product.status = False
            
            db.session.add(sale)
            db.session.commit()
            
            # Retorna os dados da venda com o produto e quantidade
            sale_domain = SaleDomain(
                sale.id,
                sale.product_id,
                sale.product_name,
                sale.quantity,
                sale.price,
                sale.total_price,
                sale.user_id,
                sale.created_at
            )
            
            return {
                "success": True,
                "message": f"Venda realizada com sucesso! Produto: {product.name}, Quantidade: {quantity}",
                "venda": sale_domain.to_dict()
            }
        
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Erro ao registrar venda: {str(e)}"}
    
    @staticmethod
    def get_all_vendas(user_id):
        try:
            sales = db.session.query(Sale).filter(Sale.user_id == user_id).all()
            return [SaleDomain(
                sale.id,
                sale.product_id,
                sale.product_name,
                sale.quantity,
                sale.price,
                sale.total_price,
                sale.user_id,
                sale.created_at
            ) for sale in sales]
        except Exception as e:
            return {"success": False, "message": f"Erro ao buscar vendas: {str(e)}"}
