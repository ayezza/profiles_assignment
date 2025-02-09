"""
Author : Abdel YEZZA (Ph.D)
Date :  july 2021
License: MIT License
NOTE : This code is completely free and can be modified with only one condition, DOT NOT REMOVE author's name
"""

import numpy as np
import pandas as pd
import math

class ModelFunctions:
    MODEL_MAPPING = {
        'model1': lambda x, y: max(x, y),
        'model2': lambda x, y: x if x >= y else x - y,
        'model3': lambda x, y: x - y,
        'model4': lambda x, y: math.sqrt(x*x + y*y),
        'model5': lambda x, y: 0.7 * x + 0.3 * y
    }

    @classmethod
    def get_model_function(cls, model_name: str):
        """Get model function by name"""
        if model_name not in cls.MODEL_MAPPING:
            raise ValueError(f"Invalid model: {model_name}. Available models: {list(cls.MODEL_MAPPING.keys())}")
        return cls.MODEL_MAPPING[model_name]

    def model_function_custom(self, profile_value, activity_value):
        """
        Implémente la fonction de modèle personnalisée pour le traitement MCAP
        """
        return self.custom_model(profile_value, activity_value)