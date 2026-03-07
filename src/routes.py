from flask import Flask, request
from src.Application.Controllers.seller_controller import get_all_sellers_controller, create_seller_controller

app = Flask(__name__)

@app.route('/sellers', methods=['GET'])
def list_sellers():
    return get_all_sellers_controller()

@app.route('/sellers', methods=['POST'])
def create_sellers():
    return create_seller_controller()