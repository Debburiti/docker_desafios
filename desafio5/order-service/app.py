from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/orders')
def get_orders():
    return jsonify({"source": "order-service", "data": [
        {"id": 101, "produto": "Teclado"},
        {"id": 102, "produto": "Monitor"}
    ]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)