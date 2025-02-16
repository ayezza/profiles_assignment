"""
Fonctions d'agrégation MCAP
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
    def get_mcap_function(cls, function_name: str) -> Callable:
        """
        Récupère une fonction MCAP par son nom
        
        Args:
            function_name (str): Nom de la fonction ('sum', 'sqrt', 'mean')
            
        Returns:
            Callable: La fonction correspondante
            
        Raises:
            ValueError: Si la fonction n'existe pas
        """
        if function_name not in cls._functions:
            raise ValueError(f"Fonction MCAP non reconnue: {function_name}")
        return cls._functions[function_name]
