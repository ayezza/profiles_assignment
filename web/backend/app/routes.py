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

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

# Obtenir les chemins absolus
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(backend_dir, 'config', 'mylogger.ini')
log_path = os.path.join(backend_dir, 'data', 'output', 'mylog.log')

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
        logger.info(f"Starting process_mcap with model={model_name}, scale_type={scale_type}, mcap_function={mcap_function}")
        
        # Lecture des fichiers CSV
        logger.info("Reading MCA file...")
        mca_content = await mca_file.read()
        try:
            mca_df = pd.read_csv(io.StringIO(mca_content.decode('utf-8')), index_col=0)
            logger.info(f"MCA file shape: {mca_df.shape}")
            logger.debug(f"MCA columns: {mca_df.columns.tolist()}")
            logger.debug(f"MCA index: {mca_df.index.tolist()}")
        except Exception as e:
            logger.error(f"Error reading MCA file: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Erreur de lecture du fichier MCA: {str(e)}")
        
        logger.info("Reading MCP file...")
        mcp_content = await mcp_file.read()
        try:
            mcp_df = pd.read_csv(io.StringIO(mcp_content.decode('utf-8')), index_col=0)
            logger.info(f"MCP file shape: {mcp_df.shape}")
            logger.debug(f"MCP columns: {mcp_df.columns.tolist()}")
            logger.debug(f"MCP index: {mcp_df.index.tolist()}")
        except Exception as e:
            logger.error(f"Error reading MCP file: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Erreur de lecture du fichier MCP: {str(e)}")
        
        # Vérification de la compatibilité des matrices
        if not set(mca_df.columns).issubset(set(mcp_df.columns)):
            missing_cols = set(mca_df.columns) - set(mcp_df.columns)
            error_msg = f"Les colonnes suivantes sont manquantes dans MCP: {missing_cols}"
            logger.error(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Configuration du logger MCAP
        logger.info(f"Setting up MCAP logger with config_path={config_path}, log_path={log_path}")
        try:
            mcap_logger = LoggerSetup.setup_logger(
                config_path,
                'myLogger',
                log_path
            )
            if not mcap_logger:
                raise Exception("Logger setup returned None")
        except Exception as e:
            logger.error(f"Error setting up MCAP logger: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erreur de configuration du logger MCAP: {str(e)}")
        
        # Obtention de la fonction de modèle
        logger.info(f"Getting model function for {model_name}")
        model_mapping = {
            'model1': ModelFunctions.model_function1,
            'model2': ModelFunctions.model_function2,
            'model3': ModelFunctions.model_function3,
            'model4': ModelFunctions.model_function4,
            'model5': ModelFunctions.model_function5
        }
        
        model_function = model_mapping.get(model_name)
        if not model_function:
            error_msg = f"Modèle non valide: {model_name}"
            logger.error(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Traitement MCAP
        logger.info("Initializing McapProcessor...")
        try:
            processor = McapProcessor(
                logger=mcap_logger,
                mca_matrix=mca_df,
                mcp_matrix=mcp_df,
                model_function=model_function,
                mcap_function=mcap_function,
                normalize=True,
                scale_type=scale_type
            )
        except Exception as e:
            logger.error(f"Error initializing McapProcessor: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erreur d'initialisation du processeur MCAP: {str(e)}")
        
        logger.info("Processing MCAP...")
        try:
            results = processor.process()
            logger.debug(f"Results type: {type(results)}")
            logger.debug(f"Results content: {results}")
            
            if not isinstance(results, dict):
                logger.error(f"Invalid results type: {type(results)}")
                raise ValueError(f"Format de résultats invalide: attendu dict, reçu {type(results)}")
            
            if 'ranking_matrix' not in results:
                logger.error("Missing ranking_matrix in results")
                raise ValueError("Format de résultats invalide: ranking_matrix manquant")
            
            if not isinstance(results['ranking_matrix'], pd.DataFrame):
                logger.error(f"Invalid ranking_matrix type: {type(results['ranking_matrix'])}")
                raise ValueError(f"Format de résultats invalide: ranking_matrix doit être un DataFrame")
            
            if results['ranking_matrix'].empty:
                logger.warning("Empty ranking matrix")
            else:
                logger.info("MCAP processing completed successfully")
                
        except Exception as e:
            logger.error(f"Error in MCAP processing: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erreur lors du traitement MCAP: {str(e)}")
        
        # Récupération des résultats et graphiques
        logger.info("Generating figures...")
        figures_data = {}
        try:
            # Parcourir les fichiers dans le répertoire des figures
            figures_dir = os.path.join(processor.output_dir, 'figures')
            if os.path.exists(figures_dir):
                for filename in os.listdir(figures_dir):
                    if filename.endswith('.png'):
                        file_path = os.path.join(figures_dir, filename)
                        with open(file_path, 'rb') as f:
                            image_data = f.read()
                            figures_data[filename] = base64.b64encode(image_data).decode()
            else:
                logger.warning("Figures directory does not exist")
        except Exception as e:
            logger.error(f"Error generating figures: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erreur lors de la génération des graphiques: {str(e)}")
        
        logger.info("Process completed successfully")
        response_data = {
            "success": True,
            "figures": figures_data
        }
        
        # Ajouter les résultats s'ils existent
        try:
            response_data.update({
                "ranking_matrix": results['ranking_matrix'].to_dict() if not results['ranking_matrix'].empty else {},
                "ranking_results": results.get('ranking_results', ''),
                "result_matrix": results['result_matrix'].to_dict() if not results['result_matrix'].empty else {}
            })
        except Exception as e:
            logger.error(f"Error formatting results: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erreur lors du formatage des résultats: {str(e)}")
        
        return JSONResponse(response_data)
        
    except HTTPException as he:
        logger.error(f"HTTP Exception: {str(he.detail)}")
        return JSONResponse({
            "success": False,
            "error": str(he.detail)
        }, status_code=he.status_code)
    except Exception as e:
        error_msg = f"Error in process_mcap: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return JSONResponse({
            "success": False,
            "error": str(e),
            "details": error_msg
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