import logging
import logging.config
import os

class LoggerSetup:
    @staticmethod
    def setup_logger(config_path, logger_name, log_file_path):
        try:
            # Vérifier si le fichier de configuration existe
            if not os.path.exists(config_path):
                print(f"Erreur: Le fichier de configuration {config_path} n'existe pas")
                return None
            
            # Créer le répertoire des logs s'il n'existe pas
            log_dir = os.path.dirname(log_file_path)
            os.makedirs(log_dir, exist_ok=True)
            
            # S'assurer que le fichier de log est accessible en écriture
            try:
                with open(log_file_path, 'a') as f:
                    pass
            except Exception as e:
                print(f"Erreur: Impossible d'écrire dans le fichier de log {log_file_path}: {str(e)}")
                return None
            
            # Convertir le chemin du fichier de log en chemin absolu
            abs_log_path = os.path.abspath(log_file_path)
            
            # Charger la configuration du logger avec le chemin absolu
            try:
                # Lire le contenu du fichier de configuration
                with open(config_path, 'r') as f:
                    config_str = f.read()
                
                # Remplacer le chemin relatif par le chemin absolu
                config_str = config_str.replace("args=('data/output/mylog.log',)", f"args=('{abs_log_path.replace(os.sep, '/')}',)")
                
                # Créer un fichier de configuration temporaire
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ini') as temp_config:
                    temp_config.write(config_str)
                    temp_config_path = temp_config.name
                
                try:
                    # Charger la configuration depuis le fichier temporaire
                    logging.config.fileConfig(temp_config_path, disable_existing_loggers=False)
                finally:
                    # Supprimer le fichier temporaire
                    os.unlink(temp_config_path)
                    
            except Exception as e:
                print(f"Erreur lors du chargement de la configuration: {str(e)}")
                return None
                
            logger = logging.getLogger(logger_name)
            
            # Vérifier si le logger a été correctement configuré
            if not logger.handlers:
                print(f"Erreur: Aucun handler n'a été configuré pour le logger {logger_name}")
                return None
            
            return logger
            
        except Exception as e:
            print(f"Erreur lors de la configuration du logger: {str(e)}")
            return None 