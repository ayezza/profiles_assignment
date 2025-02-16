import argparse
import pandas as pd
import os
import sys
import logging
from src.core.mcap_processor import McapProcessor
from src.models.model_functions import ModelFunctions

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Process MCAP matrices")
    parser.add_argument("--mca", required=True, help="Path to MCA matrix file")
    parser.add_argument("--mcp", required=True, help="Path to MCP matrix file")
    parser.add_argument("--model", default="model2", help="Model function to use")
    parser.add_argument("--scale", default="0-1", help="Scale type (0-1 or free)")
    parser.add_argument("--mcap", default="sum", help="MCAP function (sum, mean, sqrt)")
    
    args = parser.parse_args()
    
    try:
        # Vérifier l'existence des fichiers
        if not os.path.exists(args.mca) or not os.path.exists(args.mcp):
            raise FileNotFoundError("Les fichiers MCA ou MCP n'existent pas")
            
        # Charger les matrices
        mca_df = pd.read_csv(args.mca, index_col=0)
        mcp_df = pd.read_csv(args.mcp, index_col=0)
        
        # Obtenir la fonction modèle
        model_function = ModelFunctions.get_model_function(args.model)
        
        # Créer le processeur
        processor = McapProcessor(
            logger=logger,
            mca_matrix=mca_df,
            mcp_matrix=mcp_df,
            model_function=model_function,
            mcap_function=args.mcap,
            scale_type=args.scale,
            normalize=True,
            is_web_request=False
        )
        
        # Traiter et obtenir les résultats
        results = processor.process()
        
        logger.info("Traitement terminé avec succès")
        return 0
        
    except Exception as e:
        logger.error(f"Erreur: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())