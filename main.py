from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

ORDERS_FILE = "orders.json"

def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_orders(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Сервер работает"})

@app.route("/orders", methods=["GET"])
def get_orders():
    orders = load_orders()
    return jsonify(orders)

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    required_fields = ["client_name", "service_type", "date"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Отсутствуют обязательные поля"}), 400

    new_order = {
        "id": len(load_orders()) + 1,
        "client_name": data["client_name"],
        "service_type": data["service_type"],
        "date": data["date"]
    }

    orders = load_orders()
    orders.append(new_order)
    save_orders(orders)
    return jsonify(new_order), 201

if __name__ == "__main__":
    app.run(debug=True)
