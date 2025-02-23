import os
import sys
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ajouter le chemin racine du projet au PYTHONPATH
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)

# Création des dossiers nécessaires
backend_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.join(backend_dir, 'config')
data_dir = os.path.join(backend_dir, 'data')
output_dir = os.path.join(data_dir, 'output')

os.makedirs(config_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

from fastapi import FastAPI, Request, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import router

# Création des tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware pour logger toutes les requêtes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route de test
@app.get("/")
async def root():
    return {"message": "MCAP API Backend"}

# Route de test pour les modèles
@app.get("/api/v1/models/")
async def test_models():
    return {
        "models": [
            {"id": "model1", "name": "Modèle 1 (max)"},
            {"id": "model2", "name": "Modèle 2 (différence conditionnelle)"},
            {"id": "model3", "name": "Modèle 3 (différence simple)"},
            {"id": "model4", "name": "Modèle 4 (distance euclidienne)"},
            {"id": "model5", "name": "Modèle 5 (moyenne pondérée)"}
        ]
    }

# Route de test pour les types d'échelle
@app.get("/api/v1/scale-types/")
async def test_scale_types():
    return {
        "scale_types": [
            {"id": "0-1", "name": "Échelle [0,1]"},
            {"id": "free", "name": "Échelle libre"}
        ]
    }

# Route de test pour les fonctions MCAP
@app.get("/api/v1/mcap-functions/")
async def test_mcap_functions():
    return {
        "mcap_functions": [
            {"id": "sum", "name": "Somme"},
            {"id": "mean", "name": "Moyenne"},
            {"id": "sqrt", "name": "Racine carrée"}
        ]
    }

@app.post("/process")
async def process_files(
    request: Request,
    mca_file: UploadFile = File(...),
    mcp_file: UploadFile = File(...),
    model: str = Form(...),
    scale_type: str = Form(...),
    mcap_function: str = Form(...)
):
    try:
        # Save files temporarily
        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        mca_path = os.path.join(temp_dir, f'mca_{uuid.uuid4()}.csv')
        mcp_path = os.path.join(temp_dir, f'mcp_{uuid.uuid4()}.csv')
        
        async with aiofiles.open(mca_path, 'wb') as f:
            await f.write(await mca_file.read())
        async with aiofiles.open(mcp_path, 'wb') as f:
            await f.write(await mcp_file.read())

        # Initialize processor with explicit parameters
        processor = McapProcessor(
            logger=logger,
            mca_path=mca_path,
            mcp_path=mcp_path,
            model_function=get_model_function(model),
            mcap_function=mcap_function,
            scale_type=scale_type,
            is_web_request=True  # Always True for web requests
        )
        
        result = processor.process()
        
        # Validate result structure
        if not isinstance(result, dict) or 'status' not in result or 'data' not in result:
            raise ValueError("Invalid response format from processor")
            
        if result['status'] != 'success':
            raise ValueError(result.get('error', 'Unknown processing error'))
            
        return {
            'status': 'success',
            'data': {
                'ranking': result['data']['ranking'],
                'result': result['data']['result']
            }
        }
        
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }

# Inclusion des routes
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)