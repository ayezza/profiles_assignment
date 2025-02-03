"""
Fonctions de modèle pour le traitement MCAP
"""

import numpy as np
import logging

logger = logging.getLogger(__name__)

class ModelFunctions:
    @staticmethod
    def model_function1(profile_value, activity_value):
        """
        Modèle 1 : Retourne le maximum entre les deux valeurs
        """
        try:
            return float(max(float(profile_value), float(activity_value)))
        except Exception as e:
            logger.error(f"Erreur dans model_function1: {str(e)}")
            raise ValueError(f"Erreur dans model_function1: {str(e)}")
    
    @staticmethod
    def model_function2(profile_value, activity_value):
        """
        Modèle 2 : Différence conditionnelle
        Si le profil >= activité : retourne profil
        Sinon : retourne profil - (activité - profil)
        """
        try:
            profile_value = float(profile_value)
            activity_value = float(activity_value)
            if profile_value >= activity_value:
                return float(profile_value)
            else:
                return float(profile_value - (activity_value - profile_value))
        except Exception as e:
            logger.error(f"Erreur dans model_function2: {str(e)}")
            raise ValueError(f"Erreur dans model_function2: {str(e)}")
    
    @staticmethod
    def model_function3(profile_value, activity_value):
        """
        Modèle 3 : Différence simple
        Retourne profil - |activité - profil|
        """
        try:
            profile_value = float(profile_value)
            activity_value = float(activity_value)
            return float(profile_value - abs(activity_value - profile_value))
        except Exception as e:
            logger.error(f"Erreur dans model_function3: {str(e)}")
            raise ValueError(f"Erreur dans model_function3: {str(e)}")
    
    @staticmethod
    def model_function4(profile_value, activity_value):
        """
        Modèle 4 : Distance euclidienne
        Retourne 1 - sqrt((activité - profil)²)
        """
        try:
            profile_value = float(profile_value)
            activity_value = float(activity_value)
            return float(1 - np.sqrt((activity_value - profile_value) ** 2))
        except Exception as e:
            logger.error(f"Erreur dans model_function4: {str(e)}")
            raise ValueError(f"Erreur dans model_function4: {str(e)}")
    
    @staticmethod
    def model_function5(profile_value, activity_value):
        """
        Modèle 5 : Moyenne pondérée
        Retourne (2 * profil + activité) / 3
        """
        try:
            profile_value = float(profile_value)
            activity_value = float(activity_value)
            return float((2 * profile_value + activity_value) / 3)
        except Exception as e:
            logger.error(f"Erreur dans model_function5: {str(e)}")
            raise ValueError(f"Erreur dans model_function5: {str(e)}")

    @classmethod
    def get_model_function(cls, model_name):
        """
        Retourne la fonction de modèle correspondant au nom donné
        """
        model_mapping = {
            'model1': cls.model_function1,
            'model2': cls.model_function2,
            'model3': cls.model_function3,
            'model4': cls.model_function4,
            'model5': cls.model_function5
        }
        if model_name not in model_mapping:
            raise ValueError(f"Modèle non valide: {model_name}")
        return model_mapping[model_name] 