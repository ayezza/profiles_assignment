from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request, Form
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io
from . import crud, models, schemas
from .database import get_db
from src.core.mcap_processor import McapProcessor
from src.models.model_functions import ModelFunctions
from src.utils.logger import LoggerSetup
import matplotlib.pyplot as plt
import base64
from fastapi.responses import JSONResponse
import os
import traceback
import logging
import shutil
import uuid

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

# Obtenir les chemins absolus
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(backend_dir, 'config', 'mylogger.ini')
log_path = os.path.join(backend_dir, 'data', 'output', 'mylog.log')

# Initialize MCAP logger at module level
try:
    mcap_logger = LoggerSetup.setup_logger(
        config_path,
        'myLogger',
        log_path
    )
    if not mcap_logger:
        raise Exception("Logger setup returned None")
except Exception as e:
    logger.error(f"Error initializing MCAP logger: {str(e)}")
    mcap_logger = logging.getLogger('mcap_logger')  # Fallback logger

@router.post("/profiles/", response_model=schemas.Profile)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    return crud.create_profile(db=db, profile=profile)

@router.get("/profiles/", response_model=List[schemas.Profile])
def read_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    profiles = crud.get_profiles(db, skip=skip, limit=limit)
    return profiles

@router.get("/profiles/{profile_id}", response_model=schemas.Profile)
def read_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile non trouvé")
    return db_profile

@router.post("/competencies/", response_model=schemas.Competency)
def create_competency(competency: schemas.CompetencyCreate, db: Session = Depends(get_db)):
    return crud.create_competency(db=db, competency=competency)

@router.get("/competencies/", response_model=List[schemas.Competency])
def read_competencies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    competencies = crud.get_competencies(db, skip=skip, limit=limit)
    return competencies

@router.get("/competencies/{competency_id}", response_model=schemas.Competency)
def read_competency(competency_id: int, db: Session = Depends(get_db)):
    db_competency = crud.get_competency(db, competency_id=competency_id)
    if db_competency is None:
        raise HTTPException(status_code=404, detail="Compétence non trouvée")
    return db_competency

@router.post("/process-mcap/")
async def process_mcap(
    mca_file: UploadFile = File(...),
    mcp_file: UploadFile = File(...),
    model_name: str = Form(...),  # Changed to required
    scale_type: str = Form(...),  # Changed to required
    mcap_function: str = Form(...) # Changed to required
):
    try:
        logger.info("="*50)
        logger.info("Processing MCAP request")
        logger.info(f"Request parameters:")
        logger.info(f"- model_name: {model_name}")
        logger.info(f"- scale_type: {scale_type}")
        logger.info(f"- mcap_function: {mcap_function}")

        # Validate parameters
        if not model_name or not scale_type or not mcap_function:
            raise ValueError("Missing required parameters")

        # Read and validate files
        logger.info("Reading files...")
        mca_content = await mca_file.read()
        mcp_content = await mcp_file.read()
        
        logger.info("Converting to dataframes...")
        mca_df = pd.read_csv(io.StringIO(mca_content.decode('utf-8')), index_col=0)
        mcp_df = pd.read_csv(io.StringIO(mcp_content.decode('utf-8')), index_col=0)
        
        logger.info(f"MCA shape: {mca_df.shape}, MCP shape: {mcp_df.shape}")
        
        # Get model function with provided model name
        logger.info(f"Getting model function for: {model_name}")
        model_function = ModelFunctions.get_model_function(model_name)
        if not model_function:
            raise ValueError(f"Invalid model name: {model_name}")
            
        # Initialize processor with validated parameters
        logger.info("Initializing processor...")
        processor = McapProcessor(
            logger=mcap_logger,
            mca_matrix=mca_df,
            mcp_matrix=mcp_df,
            model_function=model_function,
            mcap_function=mcap_function,  # Use received parameter
            scale_type=scale_type,        # Use received parameter
            normalize=True,
            is_web_request=True
        )
        
        logger.info("Processing data...")
        result = processor.process()
        
        # Ensure result_matrix is properly formatted
        result_matrix = result['result_matrix']
        if 'max_value' in result_matrix.columns:
            result_matrix = result_matrix.drop(['max_value'], axis=1)
        if 'first_best_profile' in result_matrix.columns:
            result_matrix = result_matrix.drop(['first_best_profile'], axis=1)

        # Convert figures to base64 with higher DPI for bar plot
        figure_data = {}
        for name, fig in processor.figures.items():
            try:
                buf = io.BytesIO()
                # Use higher DPI for bar plot
                dpi = 300 if name != 'bar_plot' else 150
                fig.savefig(buf, format='png', bbox_inches='tight', dpi=dpi)
                buf.seek(0)
                img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                figure_data[name] = f'data:image/png;base64,{img_base64}'
                plt.close(fig)
                logger.info(f"Successfully converted figure {name}")
            except Exception as e:
                logger.error(f"Error converting figure {name}: {str(e)}")

        # Log the response data before sending
        logger.info("Preparing response with data:")
        logger.info(f"- Ranking matrix shape: {result['ranking_matrix'].shape if 'ranking_matrix' in result else 'missing'}")
        logger.info(f"- Result matrix shape: {result['result_matrix'].shape if 'result_matrix' in result else 'missing'}")
        logger.info(f"- Has ranking results: {bool(result.get('ranking_results'))}")
        logger.info(f"- Number of figures: {len(figure_data)}")
        
        response_data = {
            'status': 'success',
            'data': {
                'ranking_matrix': result['ranking_matrix'].to_dict('index'),
                'ranking_results': result['ranking_results'],
                'result_matrix': result_matrix.to_dict('index'),  # Use cleaned result_matrix
                'parameters_used': {
                    'model_name': model_name,
                    'mcap_function': mcap_function,
                    'scale_type': scale_type
                },
                'figures': figure_data
            }
        }

        # Verify response data
        logger.info("Final response verification:")
        logger.info(f"- Has ranking matrix: {bool(response_data['data']['ranking_matrix'])}")
        logger.info(f"- Ranking matrix keys: {list(response_data['data']['ranking_matrix'].keys())}")
        logger.info(f"- Has result matrix: {bool(response_data['data']['result_matrix'])}")
        logger.info(f"- Result matrix keys: {list(response_data['data']['result_matrix'].keys())}")
        logger.info(f"- Has figures: {bool(response_data['data']['figures'])}")
        logger.info(f"- Figure count: {len(response_data['data']['figures'])}")

        return response_data

    except Exception as e:
        logger.error(f"Process error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=400,
            content={
                'status': 'error',
                'error': str(e),
                'traceback': traceback.format_exc()
            }
        )

@router.post("/process")
async def process_files(request: Request):
    try:
        logger.info("="*50)
        logger.info("Début du traitement des fichiers")
        
        # Process files
        mca_file = request.files['mca_file']
        mcp_file = request.files['mcp_file']
        model_name = request.form.get('model_name', 'model2')
        scale_type = request.form.get('scale_type', '0-1')
        mcap_function = request.form.get('mcap_function', 'sum')
        
        mca_df = pd.read_csv(io.StringIO(mca_file.read().decode('utf-8')), index_col=0)
        mcp_df = pd.read_csv(io.StringIO(mcp_file.read().decode('utf-8')), index_col=0)
        
        # Create processor with global mcap_logger
        processor = McapProcessor(
            logger=mcap_logger,  # Use the globally initialized logger
            mca_matrix=mca_df,
            mcp_matrix=mcp_df,
            model_function=ModelFunctions.get_model_function(model_name),
            mcap_function=mcap_function,
            normalize=True,
            scale_type=scale_type
        )
        
        result = processor.process()
        
        if not isinstance(result, dict) or 'status' not in result:
            raise ValueError("Invalid processor response")
            
        if result['status'] != 'success':
            raise ValueError(result.get('error', 'Unknown error'))
            
        # Ensure we have the correct data structure
        if 'data' not in result or 'ranking' not in result['data'] or 'result' not in result['data']:
            raise ValueError("Missing required data in processor response")
            
        return {
            'status': 'success',
            'data': {
                'ranking': result['data']['ranking'],
                'result': result['data']['result']
            }
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }

@router.get("/models")  # Remove trailing slash
def get_available_models():
    return {
        "models": [
            {"id": "model1", "name": "Modèle 1 (max)"},
            {"id": "model2", "name": "Modèle 2 (différence conditionnelle)"},
            {"id": "model3", "name": "Modèle 3 (différence simple)"},
            {"id": "model4", "name": "Modèle 4 (distance euclidienne)"},
            {"id": "model5", "name": "Modèle 5 (moyenne pondérée)"}
        ]
    }

@router.get("/scale-types")  # Remove trailing slash
def get_scale_types():
    return {
        "scale_types": [
            {"id": "0-1", "name": "Échelle [0,1]"},
            {"id": "free", "name": "Échelle libre"}
        ]
    }

@router.get("/mcap-functions")  # Remove trailing slash
def get_mcap_functions():
    return {
        "mcap_functions": [
            {"id": "sum", "name": "Somme"},
            {"id": "mean", "name": "Moyenne"},
            {"id": "sqrt", "name": "Racine carrée"}
        ]
    }