"""
Author : Abdel YEZZA (Ph.D)
Date :  july 2021
License: MIT License
NOTE : This code is completely free and can be modified with only one condition, DOT NOT REMOVE author's name
"""

import numpy as np
from typing import List, Callable
import logging

logger = logging.getLogger(__name__)

class McapFunctions:
    """
    Classe contenant les différentes fonctions d'agrégation MCAP
    et un mécanisme pour les récupérer dynamiquement
    """
    
    @staticmethod
    def sum_function(scores: List[float]) -> float:
        """Somme simple des scores"""
        return float(np.sum(scores))
    
    @staticmethod
    def sqrt_function(scores: List[float]) -> float:
        """Racine carrée de la somme des carrés"""
        return float(np.sqrt(np.sum(np.square(scores))))
        
    @staticmethod
    def mean_function(scores: List[float]) -> float:
        """Moyenne des scores"""
        return float(np.mean(scores))

    # Dictionnaire associant les noms des fonctions à leur implémentation
    _functions = {
        'sum': sum_function,
        'sqrt': sqrt_function,
        'mean': mean_function
    }

    @classmethod
    def get_mcap_function(cls, function_name: str, custom_function: Callable = None) -> Callable:
        """
        Récupère une fonction MCAP par son nom ou utilise une fonction personnalisée
        
        Args:
            function_name (str): Nom de la fonction ('sum', 'sqrt', 'mean', 'custom')
            custom_function (Callable, optional): Fonction personnalisée à utiliser si function_name est 'custom'
            
        Returns:
            Callable: La fonction correspondante
            
        Raises:
            ValueError: Si la fonction n'existe pas ou si la fonction personnalisée est invalide
        """
        try:
            if function_name == 'custom' and custom_function is not None:
                if not callable(custom_function):
                    raise ValueError("La fonction personnalisée doit être callable")
                    
                # Test de la fonction personnalisée avec des valeurs simples
                test_scores = [0.5, 0.7, 0.3]
                try:
                    result = custom_function(test_scores)
                    if not isinstance(result, (int, float)):
                        raise ValueError("La fonction personnalisée doit retourner un nombre")
                except Exception as e:
                    raise ValueError(f"Erreur lors du test de la fonction personnalisée: {str(e)}")
                    
                return custom_function
                
            if function_name not in cls._functions:
                logger.error(f"Fonction MCAP inconnue: {function_name}")
                raise ValueError(f"Fonction MCAP non reconnue: {function_name}")
                
            logger.debug(f"Récupération de la fonction MCAP: {function_name}")
            return cls._functions[function_name]
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la fonction MCAP: {str(e)}")
            raise ValueError(f"Erreur lors de la récupération de la fonction MCAP: {str(e)}")

    @classmethod
    def get_available_functions(cls) -> List[str]:
        """
        Retourne la liste des noms de fonctions disponibles
        
        Returns:
            List[str]: Liste des noms de fonctions
        """
        return list(cls._functions.keys())

    @classmethod
    def register_function(cls, name: str, function: Callable):
        """
        Enregistre une nouvelle fonction MCAP
        
        Args:
            name (str): Nom de la fonction
            function (Callable): La fonction à enregistrer
            
        Raises:
            ValueError: Si le nom existe déjà ou si la fonction est invalide
        """
        if name in cls._functions:
            raise ValueError(f"Une fonction nommée '{name}' existe déjà")
            
        if not callable(function):
            raise ValueError("L'argument function doit être une fonction callable")
            
        cls._functions[name] = function