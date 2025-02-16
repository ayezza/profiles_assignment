import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Créer le dossier de logs s'il n'existe pas
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'output')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'mylog.log')
    
    # Configuration du logger
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    
    # Logger principal
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger
