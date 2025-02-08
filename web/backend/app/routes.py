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
        logger.info("="*50)
        logger.info("Début du traitement MCAP")
        logger.info(f"Paramètres reçus:")
        logger.info(f"- model_name: {model_name}")
        logger.info(f"- scale_type: {scale_type}")
        logger.info(f"- mcap_function: {mcap_function}")
        logger.info(f"- mca_file: {mca_file.filename}")
        logger.info(f"- mcp_file: {mcp_file.filename}")
        
        # Lecture des fichiers CSV
        logger.info("\nLecture du fichier MCA...")
        mca_content = await mca_file.read()
        try:
            mca_df = pd.read_csv(io.StringIO(mca_content.decode('utf-8')), index_col=0)
            logger.info(f"MCA file shape: {mca_df.shape}")
            logger.info(f"MCA colonnes: {mca_df.columns.tolist()}")
            logger.info(f"MCA index: {mca_df.index.tolist()}")
            logger.debug(f"MCA premières lignes:\n{mca_df.head()}")
            logger.debug(f"MCA types des colonnes:\n{mca_df.dtypes}")
        except Exception as e:
            logger.error(f"Erreur lecture MCA: {str(e)}")
            logger.error(f"Contenu MCA reçu:\n{mca_content.decode('utf-8')[:500]}")
            raise HTTPException(status_code=400, detail=f"Erreur lecture MCA: {str(e)}")
        
        logger.info("\nLecture du fichier MCP...")
        mcp_content = await mcp_file.read()
        try:
            mcp_df = pd.read_csv(io.StringIO(mcp_content.decode('utf-8')), index_col=0)
            logger.info(f"MCP file shape: {mcp_df.shape}")
            logger.info(f"MCP colonnes: {mcp_df.columns.tolist()}")
            logger.info(f"MCP index: {mcp_df.index.tolist()}")
            logger.debug(f"MCP premières lignes:\n{mcp_df.head()}")
            logger.debug(f"MCP types des colonnes:\n{mcp_df.dtypes}")
        except Exception as e:
            logger.error(f"Erreur lecture MCP: {str(e)}")
            logger.error(f"Contenu MCP reçu:\n{mcp_content.decode('utf-8')[:500]}")
            raise HTTPException(status_code=400, detail=f"Erreur lecture MCP: {str(e)}")
        
        # Vérification de la compatibilité des matrices
        logger.info("\nVérification de la compatibilité des matrices...")
        mca_cols = set(mca_df.columns)
        mcp_cols = set(mcp_df.columns)
        if not mca_cols.issubset(mcp_cols):
            missing_cols = mca_cols - mcp_cols
            error_msg = f"Colonnes manquantes dans MCP: {missing_cols}"
            logger.error(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Configuration du logger MCAP
        logger.info("\nConfiguration du logger MCAP...")
        try:
            mcap_logger = LoggerSetup.setup_logger(
                config_path,
                'myLogger',
                log_path
            )
            if not mcap_logger:
                raise Exception("Logger setup returned None")
        except Exception as e:
            logger.error(f"Erreur configuration logger: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erreur configuration logger: {str(e)}")
        
        # Obtention de la fonction de modèle
        logger.info("\nObtention de la fonction de modèle...")
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
        
        # Test de la fonction de modèle
        logger.info("Test de la fonction de modèle...")
        try:
            test_result = model_function(0.5, 0.5)
            logger.info(f"Test de la fonction réussi: {test_result}")
        except Exception as e:
            logger.error(f"Test de la fonction échoué: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Fonction de modèle invalide: {str(e)}")
        
        # Traitement MCAP
        logger.info("\nInitialisation du processeur MCAP...")
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
            logger.error(f"Erreur initialisation processeur: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erreur initialisation: {str(e)}")
        
        logger.info("\nTraitement MCAP...")
        try:
            results = processor.process()
            logger.info(f"Type des résultats: {type(results)}")
            logger.debug(f"Contenu des résultats: {results}")
            
            if not isinstance(results, dict):
                logger.error(f"Type de résultats invalide: {type(results)}")
                raise ValueError(f"Format invalide: attendu dict, reçu {type(results)}")
            
            if 'ranking_matrix' not in results:
                logger.error("ranking_matrix manquant dans les résultats")
                raise ValueError("ranking_matrix manquant")
            
            if not isinstance(results['ranking_matrix'], pd.DataFrame):
                logger.error(f"Type de ranking_matrix invalide: {type(results['ranking_matrix'])}")
                raise ValueError(f"ranking_matrix doit être un DataFrame")
            
            if results['ranking_matrix'].empty:
                logger.warning("Matrice de classement vide")
            else:
                logger.info("Traitement terminé avec succès")
                
        except Exception as e:
            logger.error(f"Erreur traitement MCAP: {str(e)}")
            logger.exception("Traceback complet:")
            raise HTTPException(status_code=500, detail=f"Erreur traitement: {str(e)}")
        
        # Récupération des graphiques
        logger.info("\nRécupération des graphiques...")
        figures_data = {}
        try:
            figures_dir = os.path.join(processor.output_dir, 'figures')
            if os.path.exists(figures_dir):
                for filename in os.listdir(figures_dir):
                    if filename.endswith('.png'):
                        file_path = os.path.join(figures_dir, filename)
                        with open(file_path, 'rb') as f:
                            image_data = f.read()
                            figures_data[filename] = base64.b64encode(image_data).decode()
            else:
                logger.warning("Répertoire des figures inexistant")
        except Exception as e:
            logger.error(f"Erreur récupération graphiques: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erreur graphiques: {str(e)}")
        
        logger.info("\nPréparation de la réponse...")
        response_data = {
            "success": True,
            "figures": figures_data
        }
        
        try:
            response_data.update({
                "ranking_matrix": results['ranking_matrix'].to_dict() if not results['ranking_matrix'].empty else {},
                "ranking_results": results.get('ranking_results', ''),
                "result_matrix": results['result_matrix'].to_dict() if not results['result_matrix'].empty else {}
            })
        except Exception as e:
            logger.error(f"Erreur formatage résultats: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erreur formatage: {str(e)}")
        
        logger.info("Traitement terminé avec succès")
        logger.info("="*50)
        return JSONResponse(response_data)
        
    except HTTPException as he:
        logger.error(f"HTTP Exception: {str(he.detail)}")
        return JSONResponse({
            "success": False,
            "error": str(he.detail)
        }, status_code=he.status_code)
    except Exception as e:
        error_msg = f"Erreur générale: {str(e)}\n{traceback.format_exc()}"
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