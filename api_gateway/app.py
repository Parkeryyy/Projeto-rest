from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required
)
import requests

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = "senha-super-secreta"

jwt = JWTManager(app)

app.config["SWAGGER"] = {
    "title": "Projeto REST - API Gateway",
    "uiversion": 3
}

app.config["SWAGGER_TEMPLATE"] = {
    "swagger": "2.0",
    "info": {
        "title": "Projeto REST - API Gateway",
        "description": "Gateway com APIs de usuários e livros e autenticação JWT.",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Digite Bearer, um espaço e seu token JWT."
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}

swagger = Swagger(app, template=app.config["SWAGGER_TEMPLATE"])


@app.route("/api/usuarios", methods=["GET"])
@jwt_required()
def usuarios():
    """
    Consultar usuários.
    ---
    tags:
      - Usuários
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de usuários com links HATEOAS.
      401:
        description: Token JWT ausente ou inválido.
    """
    resposta = requests.get(
        "http://localhost:5001/usuarios"
    )
    return jsonify({
        "dados": resposta.json(),
        "_links": {
            "self": {"href": "/api/usuarios"},
            "livros": {"href": "/api/livros"}
        }
    })


@app.route("/api/livros", methods=["GET"])
@jwt_required()
def livros():
    """
    Consultar livros.
    ---
    tags:
      - Livros
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de livros com links HATEOAS.
      401:
        description: Token JWT ausente ou inválido.
    """
    resposta = requests.get(
        "http://localhost:5002/livros"
    )
    return jsonify({
        "dados": resposta.json(),
        "_links": {
            "self": {"href": "/api/livros"},
            "usuarios": {"href": "/api/usuarios"}
        }
    })


@app.route("/login", methods=["POST"])
def login():
    """
    Fazer login e receber um token JWT.
    ---
    tags:
      - Autenticação
    consumes:
      - application/json
    parameters:
      - in: body
        name: credenciais
        required: true
        schema:
          type: object
          required:
            - usuario
            - senha
          properties:
            usuario:
              type: string
              example: admin
            senha:
              type: string
              example: "123"
    responses:
      200:
        description: Login realizado com sucesso.
      401:
        description: Credenciais inválidas.
    """
    dados = request.get_json()
    usuario = dados.get("usuario")
    senha = dados.get("senha")
    if usuario == "admin" and senha == "123":
        token = create_access_token(identity=usuario)
        return jsonify(token=token)
    return jsonify(mensagem="Credenciais inválidas"), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
