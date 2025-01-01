import logging
import logging.config
import os

class LoggerSetup:
    @staticmethod
    def setup_logger(config_path, logger_name, log_file_path):
        try:
            # Créer le répertoire des logs s'il n'existe pas
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            
            # Charger la configuration du logger
            logging.config.fileConfig(config_path)
            logger = logging.getLogger(logger_name)
            
            # Ajouter un handler pour le fichier
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(file_handler)
            
            return logger
        except Exception as e:
            print(f"Erreur lors de la configuration du logger: {str(e)}")
            return None 