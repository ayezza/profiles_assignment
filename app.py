from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    model = data.get('model')
    scale = data.get('scale')
    mcap_function = data.get('function')
    
    # Effectuer vos calculs MCAP ici avec les valeurs sélectionnées
    results = calculate_mcap(model, scale, mcap_function)
    
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
