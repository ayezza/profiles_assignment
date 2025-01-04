from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd
from src.core.mcap_processor import McapProcessor
from src.models.model_functions import ModelFunctions

router = APIRouter()

class MatrixData(BaseModel):
    mca: Dict[str, Dict[str, float]]
    mcp: Dict[str, Dict[str, float]]
    model: str
    scale_type: str

@router.post("/process")
async def process_matrices(data: MatrixData):
    try:
        # Conversion des données en DataFrames
        mca_df = pd.DataFrame.from_dict(data.mca, orient='index')
        mcp_df = pd.DataFrame.from_dict(data.mcp, orient='index')
        
        # Récupération de la fonction du modèle
        model_function = getattr(ModelFunctions, f"model_function{data.model[-1]}")
        
        # Création et exécution du processeur
        processor = McapProcessor(
            mca_matrix=mca_df,
            mcp_matrix=mcp_df,
            model_function=model_function,
            scale_type=data.scale_type
        )
        
        processor.process()
        
        # Récupération des résultats
        results = pd.read_csv('data/output/ranking_matrix.csv')
        with open('data/output/ranking_results.txt', 'r') as f:
            details = f.read()
        
        return {
            "results": results.to_dict(orient='index'),
            "details": details,
            "figures": {
                "radar": [f for f in os.listdir('data/output/figures') 
                         if f.startswith('radar_pentagon_')],
                "bar": [f for f in os.listdir('data/output/figures') 
                       if f.startswith('affectation_bar_')]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 