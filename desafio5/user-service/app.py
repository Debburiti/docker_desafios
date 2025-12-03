from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/users')
def get_users():
    return jsonify({"source": "user-service", "data": [
        {"id": 1, "nome": "Debora"},
        {"id": 2, "nome": "Mirella"}
    ]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)