from flask import Flask
import requests

app = Flask(__name__)

API_URL = "http://data-service:5000/usuarios" 

@app.route('/')
def consumir_usuarios():
    try:
        response = requests.get(API_URL)
        response.raise_for_status() 
        
        usuarios = response.json()
        
        output = "<h1>Lista de Usuários (Consumido do Data Service)</h1>"
        output += "<ul>"
        for user in usuarios:
            output += f"<li>**{user['nome']}** está **{user['status']}** desde **{user['criacao']}**</li>"
        output += "</ul>"
        
        return output
    except requests.exceptions.RequestException as e:
        return f"<h1>Erro ao conectar ao Data Service:</h1><p>{e}</p>", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)