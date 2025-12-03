from flask import Flask, jsonify

app = Flask(__name__)

USUARIOS_MOCK = [
    {"id": 1, "nome": "Debora Buriti", "status": "Ativo", "criacao": "2023-01-15"},
    {"id": 2, "nome": "Mirella Santana", "status": "Inativo", "criacao": "2023-03-22"},
]

@app.route('/usuarios')
def listar_usuarios():
    return jsonify(USUARIOS_MOCK)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)