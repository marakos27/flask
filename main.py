from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

orders = []

@app.route("/")
def index():
    return jsonify({"message": "Добро пожаловать в сервис заказов!"})

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    required_fields = ["client_name", "service_type", "date"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Отсутствуют обязательные поля."}), 400

    try:
        datetime.strptime(data["date"], "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Неверный формат даты. Используйте YYYY-MM-DD."}), 400

    order = {
        "id": len(orders) + 1,
        "client_name": data["client_name"],
        "service_type": data["service_type"],
        "date": data["date"]
    }
    orders.append(order)
    return jsonify(order), 201

@app.route("/orders", methods=["GET"])
def list_orders():
    return jsonify(orders)
