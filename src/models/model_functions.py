import numpy as np
import pandas as pd

class ModelFunctions:
    @staticmethod
    def model_function2(profile_value, activity_value):
        """
        Implémente la fonction de modèle 2 pour le traitement MCAP
        """
        return (profile_value if profile_value >= activity_value 
                else profile_value - activity_value) 