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
    @staticmethod 
    def get_model_function(model_name):
        """Return model function with proper name"""
        
        # Define model functions with proper naming
        def model1(x, y):
            return max(x, y)
        model1.__name__ = 'model1'
        
        def model2(x, y):
            return x if x >= y else x - y
        model2.__name__ = 'model2'
            
        def model3(x, y):
            return x - y
        model3.__name__ = 'model3'
            
        def model4(x, y):
            return math.sqrt(x*x + y*y)
        model4.__name__ = 'model4'
            
        def model5(x, y):
            return 0.7 * x + 0.3 * y
        model5.__name__ = 'model5'

        models = {
            'model1': model1,
            'model2': model2, 
            'model3': model3,
            'model4': model4,
            'model5': model5
        }
        
        if model_name not in models:
            raise ValueError(f"Unknown model: {model_name}")
            
        return models[model_name]

    def model_function_custom(self, profile_value, activity_value):
        """
        Implémente la fonction de modèle personnalisée pour le traitement MCAP
        """
        return self.custom_model(profile_value, activity_value)

    @staticmethod
    def get_model_function_with_name(model_name):
        """Return model function with name attribute"""
        if model_name == 'model1':
            def model1(mcp, mca):
                # Model 1 implementation
                return mcp * mca
            model1.__name__ = 'model1'  # Set function name
            return model1

        elif model_name == 'model2':
            def model2(mcp, mca):
                # Model 2 implementation
                return mcp + mca
            model2.__name__ = 'model2'
            return model2

        # ... other models ...

        else:
            raise ValueError(f"Unknown model: {model_name}")