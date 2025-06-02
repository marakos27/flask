from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # Замени на свой ключ в продакшене

jwt = JWTManager(app)

# Простая "база данных"
users = {}

@app.route('/')
def home():
    return jsonify(message="Добро пожаловать на сервер!"), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify(error="Нужны username и password"), 400

    if username in users:
        return jsonify(error="Пользователь уже существует"), 409

    hashed_password = generate_password_hash(password)
    users[username] = hashed_password
    return jsonify(message="Регистрация успешна"), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username not in users or not check_password_hash(users[username], password):
        return jsonify(error="Неверные данные"), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/private', methods=['GET'])
@jwt_required()
def private():
    current_user = get_jwt_identity()
    return jsonify(message=f"Привет, {current_user}. Это приватный маршрут!"), 200
