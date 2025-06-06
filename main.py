from flask import Flask, request, jsonify
import os
import json
from cryptography.fernet import Fernet

app = Flask(__name__)

KEY_FILE = "secret.key"
ORDERS_FILE = "orders.json"

# Генерация и загрузка ключа шифрования
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return Fernet(key)

fernet = load_key()

# Загрузка заказов из зашифрованного файла
def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, "rb") as f:
        encrypted_data = f.read()
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception:
            return []

# Сохранение заказов в файл (зашифрованно)
def save_orders(orders):
    data = json.dumps(orders).encode()
    encrypted = fernet.encrypt(data)
    with open(ORDERS_FILE, "wb") as f:
        f.write(encrypted)

orders = load_orders()

@app.route("/")
def index():
    return "Сервер запущен и работает!"

@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(orders)

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    if not data:
        return jsonify({"error": "Нет данных"}), 400

    new_order = {
        "id": len(orders) + 1,
        "client_name": data.get("client_name"),
        "service_type": data.get("service_type"),
        "date": data.get("date")
    }
    orders.append(new_order)
    save_orders(orders)
    return jsonify(new_order), 201

if __name__ == "__main__":
    # Только для локального запуска
    app.run(host="0.0.0.0", port=8000)
