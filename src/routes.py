from flask import render_template, request, jsonify
from app import app
from core.mcap_processor import McapProcessor
#from core.model_functions import get_model_function
#from core.utils import process_files
from config import setup_logging

# Configurer le logging
logger = setup_logging()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Get all parameters from form
        mca_file = request.files['mca']
        mcp_file = request.files['mcp']
        model = request.form.get('model', 'model5')
        scale_type = request.form.get('scale', '0-1')
        mcap_function = request.form.get('mcap', 'sum')  # Make sure we get 'mcap' not 'function'
        
        logger.info(f"Received parameters: model={model}, scale={scale_type}, mcap={mcap_function}")
        
        # Validate parameters
        if not mca_file or not mcp_file:
            return jsonify({"error": "Missing required files"}), 400
            
        # Pass all parameters to process endpoint
        result = process_files(mca_file, mcp_file, model, scale_type, mcap_function)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/process-mcap', methods=['POST'])
def process_mcap():
    try:
        data = request.get_json()
        logger.info("\n=== New MCAP Web Request ===")
        
        # Validation stricte des paramètres
        required_params = ['mca_matrix', 'mcp_matrix', 'model_function', 'mcap_function', 'scale_type']
        if not all(param in data for param in required_params):
            raise ValueError(f"Missing parameters: {[p for p in required_params if p not in data]}")

        # Log détaillé des paramètres reçus
        logger.info("Frontend Parameters:")
        logger.info(f"Model Function: {data['model_function']}")
        logger.info(f"MCAP Function: {data['mcap_function']}")
        logger.info(f"Scale Type: {data['scale_type']}")

        # Obtenir la fonction modèle
        model_function = get_model_function(data['model_function'])
        if model_function is None:
            raise ValueError(f"Invalid model function: {data['model_function']}")

        # Créer le processeur avec les paramètres exacts
        processor = McapProcessor(
            logger=logger,
            mca_matrix=data['mca_matrix'],
            mcp_matrix=data['mcp_matrix'],
            model_function=model_function,
            mcap_function=data['mcap_function'],
            scale_type=data['scale_type'],
            normalize=True,
            norm='l2',
            axis=1
        )

        # Traiter et obtenir les résultats
        results = processor.process()
        
        # Préparer la réponse avec la matrice dans le bon format
        response_data = {
            'status': 'success',
            'data': {
                'ranking_matrix': results['ranking_matrix'].to_dict(),
                'result_matrix': results['result_matrix'].transpose().to_dict(),  # Transposer pour l'affichage web
                'parameters_used': {
                    'model_function': data['model_function'],
                    'mcap_function': data['mcap_function'],
                    'scale_type': data['scale_type']
                }
            }
        }

        logger.info("=== Request Completed Successfully ===\n")
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 400
