from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 👈 Включаем поддержку CORS

orders = []

@app.route("/")
def home():
    return jsonify({"message": "Добро пожаловать на сервер заказов!"})

@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(orders)

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    orders.append(data)
    return jsonify({"message": "Заказ создан", "order": data}), 201
