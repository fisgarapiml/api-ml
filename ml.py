import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Rota para obter os produtos
@app.route('/produtos', methods=['GET'])
def produtos():
    try:
        # Consumindo a API do Mercado Livre
        response = requests.get('https://api.mercadolibre.com/sites/MLB/search?q=notebook')
        # Retorna os dados da API em formato JSON
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        # Caso haja erro, retornamos uma mensagem de erro
        return jsonify({'error': str(e)}), 500

# Inicializando o servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
