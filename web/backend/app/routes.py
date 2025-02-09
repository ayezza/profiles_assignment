from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
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
    model_name: str = "model2",
    scale_type: str = "0-1",
    mcap_function: str = "sum"
):
    try:
        logger.info("="*50)
        logger.info("Début du traitement MCAP")
        logger.info(f"Paramètres reçus:")
        logger.info(f"- model_name: {model_name}")
        logger.info(f"- scale_type: {scale_type}")
        logger.info(f"- mcap_function: {mcap_function}")
        
        # Process files
        await mca_file.seek(0)
        await mcp_file.seek(0)
        mca_df = pd.read_csv(io.StringIO((await mca_file.read()).decode('utf-8')), index_col=0)
        mcp_df = pd.read_csv(io.StringIO((await mcp_file.read()).decode('utf-8')), index_col=0)
        
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
        
        results = processor.process()
        
        response_data = {
            "success": True,
            "ranking_matrix": results['ranking_matrix'].to_dict(),
            "result_matrix": results['result_matrix'].to_dict()
        }
        
        return JSONResponse(response_data)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@router.get("/models/")
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

@router.get("/scale-types/")
def get_scale_types():
    return {
        "scale_types": [
            {"id": "0-1", "name": "Échelle [0,1]"},
            {"id": "free", "name": "Échelle libre"}
        ]
    }

@router.get("/mcap-functions/")
def get_mcap_functions():
    return {
        "mcap_functions": [
            {"id": "sum", "name": "Somme"},
            {"id": "mean", "name": "Moyenne"},
            {"id": "sqrt", "name": "Racine carrée"}
        ]
    }