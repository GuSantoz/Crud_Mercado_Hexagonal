import time
from src.routes import app
from src.Infrastructure.Model.seller_model import db, SellerModel

def connect_with_retry():
    # Tenta conectar 10 vezes com intervalo de 3 segundos
    retries = 10
    while retries > 0:
        try:
            print(f"Tentando conectar ao MySQL... ({11 - retries}/10)")
            db.connect()
            # Se conectou, cria as tabelas
            db.create_tables([SellerModel])
            print("Conectado com sucesso e tabelas verificadas!")
            return True
        except Exception as e:
            retries -= 1
            print(f"Banco ainda não pronto. Aguardando... Erro: {e}")
            time.sleep(3)
    return False

if __name__ == "__main__":
    if connect_with_retry():
        # Somente sobe o Flask se o banco estiver ok
        app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        print("Não foi possível conectar ao banco de dados após várias tentativas.")