# %%
"""
Author : Abdel YEZZA (Ph.D)
Date :  july 2021
NOTE : This code is completely free and can be modified with only one condition, DOT NOT REMOVE author's name
"""

import os
import sys
import argparse
from src.utils.logger import LoggerSetup
from src.utils.file_utils import FileUtils
from src.core.mcap_processor import McapProcessor
from src.models.model_functions import ModelFunctions

def get_default_paths():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return {
        'mca_file': os.path.join(base_dir, 'data', 'input', 'mca_01.csv'),  # défaut pour échelle [0,1]
        'mcp_file': os.path.join(base_dir, 'data', 'input', 'mcp_01.csv'),
        'log_file': os.path.join(base_dir, 'data', 'output', 'mylog.log'),
        'logger_config': os.path.join(base_dir, 'config', 'mylogger.ini')
    }

def get_model_function(model_name):
    """Retourne la fonction de modèle selon le nom"""
    model_mapping = {
        'model2': ModelFunctions.model_function2,
        # Ajouter d'autres modèles ici si nécessaire
    }
    return model_mapping.get(model_name, ModelFunctions.model_function2)

def main(mca_file=None, mcp_file=None, model_name='model2', scale_type='0-1'):
    # Obtenir les chemins par défaut
    paths = get_default_paths()
    
    # Remplacer par les chemins fournis si spécifiés
    if mca_file:
        paths['mca_file'] = mca_file
    if mcp_file:
        paths['mcp_file'] = mcp_file
    
    # Créer les répertoires nécessaires
    os.makedirs(os.path.dirname(paths['log_file']), exist_ok=True)
    
    # Configuration du logger
    logger = LoggerSetup.setup_logger(
        paths['logger_config'], 
        'myLogger', 
        paths['log_file']
    )

    if not logger:
        print('Problème de configuration du logger')
        return 1

    logger.info('Démarrage du traitement')
    logger.info(f'Fichier MCA: {paths["mca_file"]}')
    logger.info(f'Fichier MCP: {paths["mcp_file"]}')
    logger.info(f'Modèle: {model_name}')
    logger.info(f'Type d\'échelle: {scale_type}')

    # Vérification et chargement des fichiers
    try:
        mca_csv = FileUtils.load_csv_file(paths['mca_file'])
        mcp_csv = FileUtils.load_csv_file(paths['mcp_file'])
        logger.info(f"Matrices chargées avec succès")
    except Exception as e:
        logger.error(f"Erreur lors du chargement des fichiers: {str(e)}")
        return 1

    # Obtenir la fonction de modèle
    model_function = get_model_function(model_name)

    # Utilisation du processeur MCAP
    processor = McapProcessor(
        logger=logger,
        mca_matrix=mca_csv,
        mcp_matrix=mcp_csv,
        model_function=model_function,
        normalize=True,
        scale_type=scale_type
    )

    return processor.process()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Traitement MCAP avec paramètres configurables')
    parser.add_argument('--mca', help='Chemin vers le fichier MCA')
    parser.add_argument('--mcp', help='Chemin vers le fichier MCP')
    parser.add_argument('--model', default='model2', help='Nom du modèle à utiliser')
    parser.add_argument('--scale', default='0-1', choices=['0-1', 'free'], 
                        help='Type d\'échelle (0-1 ou libre)')
    
    args = parser.parse_args()
    
    sys.exit(main(
        mca_file=args.mca,
        mcp_file=args.mcp,
        model_name=args.model,
        scale_type=args.scale
    ))

