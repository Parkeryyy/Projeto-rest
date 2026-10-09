from flask import Flask, jsonify
app = Flask(__name__)
@app.route("/usuarios")
def listar_usuarios():
    return jsonify([
        {"id": 1, "nome": "Joao"},
        {"id": 2, "nome": "Maria"}
    ])
if __name__ == "__main__":
    app.run(port=5001, debug=True)