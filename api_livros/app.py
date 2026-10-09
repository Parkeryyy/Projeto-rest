from flask import Flask, jsonify
app = Flask(__name__)
@app.route("/livros")
def listar_livros():
    return jsonify([
        {"id": 1, "titulo": "Dom Casmurro"},
        {"id": 2, "titulo": "O Cortico"}
    ])
if __name__ == "__main__":
    app.run(port=5002, debug=True)