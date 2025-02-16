from flask import Flask, request
from config import setup_logging
from core.mcap_processor import McapProcessor  # Changed from MCAPProcessor
import os

# Setup logging
logger = setup_logging()

# Create Flask app
app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_files():
    try:
        # Log all form data for debugging
        logger.info("Received form data:")
        for key, value in request.form.items():
            logger.info(f"- {key}: {value}")
            
        mca_file = request.files['mca']
        mcp_file = request.files['mcp']
        model = request.form.get('model', 'model5')
        scale_type = request.form.get('scale', '0-1')
        mcap_function = request.form.get('mcap')  # Remove default to catch missing parameter
        
        if not mcap_function:
            logger.error("MCAP function not provided in form data")
            return {"error": "MCAP function is required"}, 400
            
        logger.info(f"Processing with parameters: model={model}, scale={scale_type}, mcap={mcap_function}")
        
        # Save uploaded files temporarily
        mca_path = os.path.join('data', 'input', 'mca.csv')
        mcp_path = os.path.join('data', 'input', 'mcp.csv')
        mca_file.save(mca_path)
        mcp_file.save(mcp_path)
        
        # Initialize processor with correct parameters
        processor = McapProcessor(
            mca_path=mca_path,
            mcp_path=mcp_path,
            model=model,
            scale_type=scale_type,
            mcap_function=mcap_function  # Verify this parameter name matches the processor's expected parameter
        )
        
        # Process the data
        result = processor.process()
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {"error": str(e)}, 500

# Import routes after app is created
from routes import *

if __name__ == '__main__':
    app.run(debug=True, port=3001)
