import logging
import logging.config
import os
import shutil

class LoggerSetup:
    @staticmethod
    def setup_logger(config_path, logger_name, log_file_path):
        """
        Configure et retourne un logger
        """
        try:
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Le fichier de configuration {config_path} n'existe pas")

            # S'assurer que le répertoire du fichier de log existe
            log_dir = os.path.dirname(log_file_path)
            os.makedirs(log_dir, exist_ok=True)

            # Copier le fichier de configuration vers un fichier temporaire
            temp_config_path = os.path.join(log_dir, 'temp_logger.ini')
            shutil.copy2(config_path, temp_config_path)

            # Modifier le chemin du fichier de log dans la configuration temporaire
            with open(temp_config_path, 'r') as f:
                config_content = f.read()
            
            config_content = config_content.replace(
                "args=('mylog.log'",
                f"args=('{log_file_path.replace(os.sep, '/')}'")

            with open(temp_config_path, 'w') as f:
                f.write(config_content)

            # Lire la configuration depuis le fichier temporaire
            logging.config.fileConfig(
                temp_config_path,
                disable_existing_loggers=False
            )

            # Supprimer le fichier temporaire
            os.remove(temp_config_path)

            # Obtenir le logger
            logger = logging.getLogger(logger_name)
            logger.info(f"Logger initialisé avec succès. Fichier de log: {log_file_path}")
            
            return logger

        except Exception as e:
            print(f"Erreur lors de la configuration du logger: {str(e)}")
            raise  # Remonter l'exception pour une meilleure gestion des erreurs 