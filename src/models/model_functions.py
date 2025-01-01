"""
Author : Abdel YEZZA (Ph.D)
Date :  july 2021
LicenseMIT License
NOTE : This code is completely free and can be modified with only one condition, DOT NOT REMOVE author's name
"""

import numpy as np
import pandas as pd
import math

class ModelFunctions:
    @staticmethod
    def model_function1(profile_value, activity_value):
        """
        Implémente la fonction de modèle 3 pour le traitement MCAP
        """
        return max(profile_value, activity_value)

    @staticmethod
    def model_function2(profile_value, activity_value):
        """
        Implémente la fonction de modèle 2 pour le traitement MCAP
        """
        return (profile_value if profile_value >= activity_value 
                else profile_value - activity_value) 

    @staticmethod
    def model_function3(profile_value, activity_value):
        """
        Implémente la fonction de modèle 3 pour le traitement MCAP
        """
        return profile_value - activity_value
    
    @staticmethod
    def model_function4(profile_value, activity_value):
        """
        Implémente la fonction de modèle 4 pour le traitement MCAP
        """
        return math.sqrt(profile_value*profile_value + activity_value*activity_value)

    @staticmethod
    def model_function5(profile_value, activity_value, profile_weight=0.7, activity_weight=0.3):
        """
        Implémente la fonction de modèle 5 pour le traitement MCAP
        Calcule une moyenne pondérée entre le profil et l'activité
        
        Args:
            profile_value: Valeur du profil
            activity_value: Valeur de l'activité
            profile_weight: Poids pour le profil (défaut: 0.7)
            activity_weight: Poids pour l'activité (défaut: 0.3)
        """
        return profile_weight * profile_value + activity_weight * activity_value
