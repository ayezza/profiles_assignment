"""
Author : Abdel YEZZA (Ph.D)
Date :  july 2021
License: MIT License
NOTE : This code is completely free and can be modified with only one condition, DOT NOT REMOVE author's name
"""

import numpy as np
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt
import uuid
import os
import math
import logging
from models.mcap_functions import McapFunctions

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class McapProcessor:
    def __init__(self, logger, mca_matrix, mcp_matrix, model_function, mcap_function='mean', 
                 custom_mcap_function=None, normalize=True, norm='l2', axis=1, 
                 copy=False, return_norm=False, scale_type='0-1', is_web_request=False):
        """
        Initialise le processeur MCAP
        Args:
            model_function: Fonction qui prend deux paramètres (mcp_value, mca_value) et retourne un float
            mcap_function: Nom de la fonction MCAP ('sum', 'sqrt', 'mean', 'custom')
            custom_mcap_function: Fonction personnalisée à utiliser si mcap_function est 'custom'
            is_web_request: Boolean indiquant si l'appel vient de l'API web
        """
        self.logger = logger
        self.mca_matrix = pd.DataFrame(mca_matrix)
        self.mcp_matrix = pd.DataFrame(mcp_matrix)
        
        # Valider la fonction de modèle
        if not callable(model_function):
            raise ValueError("model_function doit être une fonction callable")
        
        # Tester la fonction avec des valeurs simples
        try:
            test_result = model_function(0.5, 0.5)
            if not isinstance(test_result, (int, float)) or not math.isfinite(test_result):
                raise ValueError("model_function doit retourner un nombre fini")
            self.model_function = model_function
        except Exception as e:
            raise ValueError(f"model_function invalide: {str(e)}")
            
        self.mcap_function = mcap_function
        self.custom_mcap_function = custom_mcap_function
        self.normalize = normalize
        self.norm = norm
        self.axis = axis
        self.copy = copy
        self.return_norm = return_norm
        self.scale_type = scale_type
        self.is_web_request = is_web_request
        
        # Adapter le chemin racine selon le contexte (web ou local)
        if is_web_request:
            self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) 
        else:
            self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
        self.output_dir = os.path.join(self.root_dir, 'data', 'output')
        self.figures_dir = os.path.join(self.output_dir, 'figures')
        os.makedirs(self.figures_dir, exist_ok=True)
        
        # Initialiser les attributs pour les résultats
        self.figures = {}
        self.ranking_matrix = pd.DataFrame()
        self.ranking_results = ""
        
        # Valider les matrices
        if self.mca_matrix.empty or self.mcp_matrix.empty:
            raise ValueError("Les matrices MCA et MCP ne peuvent pas être vides")
            
        # Valider les dimensions
        if self.mca_matrix.shape[1] != self.mcp_matrix.shape[1]:
            raise ValueError(f"Les dimensions des matrices ne correspondent pas: MCA={self.mca_matrix.shape}, MCP={self.mcp_matrix.shape}")
            
        # Vérifier les valeurs NaN
        if self.mca_matrix.isna().any().any() or self.mcp_matrix.isna().any().any():
            raise ValueError("Les matrices contiennent des valeurs NaN")

    def _apply_model_function(self, mcp_value, mca_value):
        """
        Applique la fonction de modèle de manière sécurisée
        """
        try:
            # Vérifier les valeurs d'entrée
            if not isinstance(mcp_value, (int, float)) or not isinstance(mca_value, (int, float)):
                self.logger.error(f"Valeurs d'entrée invalides: mcp={mcp_value} ({type(mcp_value)}), mca={mca_value} ({type(mca_value)})")
                raise ValueError("Les valeurs d'entrée doivent être numériques")
                
            if not (math.isfinite(float(mcp_value)) and math.isfinite(float(mca_value))):
                self.logger.error(f"Valeurs non finies: mcp={mcp_value}, mca={mca_value}")
                raise ValueError("Les valeurs d'entrée doivent être finies")
            
            # Appliquer la fonction de modèle
            result = self.model_function(float(mcp_value), float(mca_value))
            
            # Vérifier le résultat
            if not isinstance(result, (int, float)):
                self.logger.error(f"La fonction de modèle a retourné un type invalide: {type(result)}")
                raise ValueError(f"La fonction de modèle doit retourner un nombre, pas {type(result)}")
                
            if not math.isfinite(float(result)):
                self.logger.error(f"La fonction de modèle a retourné une valeur non finie: {result}")
                raise ValueError("La fonction de modèle doit retourner une valeur finie")
            
            return float(result)
            
        except Exception as e:
            self.logger.error(f"Erreur dans la fonction de modèle: {str(e)}")
            raise ValueError(f"Erreur dans la fonction de modèle: {str(e)}")

    def _normalize_matrix(self, matrix):
        """
        Normalise la matrice selon le type d'échelle choisi
        
        Args:
            matrix (pd.DataFrame): Matrice à normaliser
            
        Returns:
            pd.DataFrame: Matrice normalisée
            
        Raises:
            ValueError: Si la normalisation échoue
        """
        try:
            if self.scale_type == '0-1':
                # Vérifier si les valeurs sont entre 0 et 1
                if (matrix.values < 0).any() or (matrix.values > 1).any():
                    self.logger.error("Les valeurs doivent être entre 0 et 1 pour l'échelle 0-1")
                    raise ValueError("Les valeurs doivent être entre 0 et 1 pour l'échelle 0-1")
                
                if self.normalize:
                    self.logger.info("Normalisation avec l'échelle 0-1")
                    try:
                        normalized = pd.DataFrame(
                            preprocessing.normalize(matrix, norm=self.norm, axis=self.axis),
                            index=matrix.index,
                            columns=matrix.columns
                        )
                        self.logger.debug(f"Matrice normalisée avec succès. Shape: {normalized.shape}")
                        return normalized
                    except Exception as e:
                        self.logger.error(f"Erreur lors de la normalisation 0-1: {str(e)}")
                        raise ValueError(f"Erreur lors de la normalisation 0-1: {str(e)}")
                return matrix
            else:  # 'free'
                self.logger.info("Normalisation avec l'échelle libre")
                try:
                    # Normalisation min-max pour ramener à l'échelle [0,1]
                    scaler = preprocessing.MinMaxScaler()
                    normalized = pd.DataFrame(
                        scaler.fit_transform(matrix),
                        index=matrix.index,
                        columns=matrix.columns
                    )
                    
                    if self.normalize:
                        self.logger.info("Application de la normalisation supplémentaire")
                        normalized = pd.DataFrame(
                            preprocessing.normalize(normalized, norm=self.norm, axis=self.axis),
                            index=matrix.index,
                            columns=matrix.columns
                        )
                    self.logger.debug(f"Matrice normalisée avec succès. Shape: {normalized.shape}")
                    return normalized
                except Exception as e:
                    self.logger.error(f"Erreur lors de la normalisation libre: {str(e)}")
                    raise ValueError(f"Erreur lors de la normalisation libre: {str(e)}")
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la normalisation de la matrice: {str(e)}")
            raise ValueError(f"Erreur lors de la normalisation de la matrice: {str(e)}")

    def plot_results(self, result_matrix, kind="bar"):
        """Génère un graphique des résultats"""
        fig = plt.figure(figsize=(12, 7))
        result_matrix.plot(kind=kind, stacked=False)
        plt.title("Matrice d'affectation - Poids des profils par activité")
        plt.xlabel('Activités')
        plt.ylabel('Poids des profils')
        plt.legend(title='Profils', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Sauvegarder la figure dans le dictionnaire
        self.figures['bar_plot'] = fig
        
        # Sauvegarder aussi dans un fichier
        output_file = os.path.join(self.figures_dir, f'affectation_bar_{uuid.uuid4()}.png')
        plt.savefig(output_file, dpi=300, bbox_inches='tight')

    def plot_radar(self, result_matrix):
        """Génère un graphique radar pentagonal pour chaque activité"""
        # Nettoyer result_matrix
        if 'max_value' in result_matrix.columns:
            result_matrix = result_matrix.drop(['max_value'], axis=1)
        if 'first_best_profile' in result_matrix.columns:
            result_matrix = result_matrix.drop(['first_best_profile'], axis=1)
        
        # Pour chaque activité
        for activity in result_matrix.index:
            # Créer une figure
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(111, projection='polar')
            
            # Obtenir les scores pour cette activité
            scores = result_matrix.loc[activity]
            
            # Sélectionner les 5 meilleurs scores pour le pentagone
            scores = scores.nlargest(5)
            
            # Calculer la valeur maximale pour l'échelle
            max_value = scores.max()
            
            # Nombre fixe de points pour le pentagone
            num_vars = 5
            
            # Calculer les angles pour chaque point du pentagone
            angles = [n / float(num_vars) * 2 * np.pi for n in range(num_vars)]
            angles += angles[:1]  # Fermer le pentagone en répétant le premier point
            
            # Préparer les données pour le tracé
            values = scores.values.flatten().tolist()
            values += values[:1]  # Fermer le pentagone en répétant la première valeur
            
            # Tracer les lignes de la grille pentagonale
            for level in [0.2, 0.4, 0.6, 0.8, 1.0]:
                pentagon_points = []
                for angle in angles[:-1]:  # Ne pas inclure le point de fermeture
                    x = level * max_value * np.cos(angle)
                    y = level * max_value * np.sin(angle)
                    pentagon_points.append((x, y))
                
                # Tracer les lignes du pentagone pour ce niveau
                pentagon_points.append(pentagon_points[0])  # Fermer le pentagone
                xs, ys = zip(*pentagon_points)
                ax.plot(angles, [level * max_value] * len(angles), color='gray', alpha=0.2)
                
                # Ajouter des lignes du centre vers les sommets
                for angle in angles[:-1]:
                    ax.plot([0, angle], [0, max_value], color='gray', alpha=0.2)
            
            # Tracer le pentagone principal
            ax.plot(angles, values, 'o-', linewidth=2, label=activity, color='b', alpha=0.25)
            ax.fill(angles, values, alpha=0.25)
            
            # Configurer les étiquettes
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(scores.index)
            
            # Configurer les limites et le style
            ax.set_ylim(0, max_value)
            plt.title(f'Radar Plot - {activity}', y=1.05)
            
            # Supprimer les cercles de la grille polaire
            ax.grid(False)
            
            # Sauvegarder la figure dans le dictionnaire
            self.figures[f'radar_plot_{activity}'] = fig
            
            # Sauvegarder aussi dans un fichier
            output_file = os.path.join(self.figures_dir, f'radar_pentagon_{activity}_{uuid.uuid4()}.png')
            plt.savefig(output_file, dpi=300, bbox_inches='tight')

    def generate_mcap_matrix(self):
        """
        Génère la matrice MCAP en appliquant la fonction de modèle entre les matrices MCA et MCP
        
        Returns:
            pd.DataFrame: Matrice MCAP résultante
            
        Raises:
            ValueError: Si la génération échoue
        """
        try:
            result = pd.DataFrame(
                np.zeros((self.mca_matrix.shape[0], self.mcp_matrix.shape[0])),
                index=self.mca_matrix.index,
                columns=self.mcp_matrix.index
            )
            
            # Obtenir la fonction MCAP
            mcap_fun = McapFunctions.get_mcap_function(
                self.mcap_function, 
                custom_function=self.custom_mcap_function
            )

            for i in range(self.mca_matrix.shape[0]):
                activity = self.mca_matrix.index[i]
                for j in range(self.mcp_matrix.shape[0]):
                    profile = self.mcp_matrix.index[j]
                    scores = []
                    
                    for k in range(self.mca_matrix.shape[1]):
                        mcp_value = self.mcp_matrix.iloc[j, k]
                        mca_value = self.mca_matrix.iloc[i, k]
                        
                        score = self._apply_model_function(mcp_value, mca_value)
                        if score is None:
                            raise ValueError(f"Échec du calcul pour {activity}/{profile}")
                        scores.append(score)
                    
                    # Calculer le score final
                    try:
                        final_score = mcap_fun(scores)
                        
                        if not math.isfinite(final_score):
                            raise ValueError(f"Score final non fini pour {activity}/{profile}")
                            
                        result.iloc[i, j] = final_score
                        
                    except Exception as e:
                        raise ValueError(f"Erreur lors du calcul final pour {activity}/{profile}: {str(e)}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la génération de la matrice MCAP: {str(e)}")
            raise ValueError(f"Erreur lors de la génération de la matrice MCAP: {str(e)}")

    def process(self):
        """
        Traite les matrices MCA et MCP pour générer les résultats MCAP
        Returns:
            dict: Dictionnaire contenant les résultats du traitement avec les clés suivantes :
                - ranking_matrix (pd.DataFrame): Matrice de classement
                - ranking_results (str): Résultats détaillés au format texte
                - result_matrix (pd.DataFrame): Matrice de résultats complète
        Raises:
            ValueError: Si le traitement échoue
        """
        result = None
        try:
            self.logger.info("Début du traitement MCAP")
            
            # Vérifications initiales
            if self.mca_matrix.empty or self.mcp_matrix.empty:
                raise ValueError("Les matrices MCA ou MCP sont vides")
            
            if self.mca_matrix.shape[1] != self.mcp_matrix.shape[1]:
                raise ValueError(f"Les dimensions des matrices ne correspondent pas: MCA={self.mca_matrix.shape}, MCP={self.mcp_matrix.shape}")
            
            if self.mca_matrix.isna().any().any() or self.mcp_matrix.isna().any().any():
                raise ValueError("Les matrices contiennent des valeurs NaN")
            
            self.logger.info(f"Dimensions MCA: {self.mca_matrix.shape}")
            self.logger.info(f"Dimensions MCP: {self.mcp_matrix.shape}")
            
            # Normalisation
            if self.normalize:
                self.logger.info("Normalisation des matrices")
                self.mca_matrix = self._normalize_matrix(self.mca_matrix)
                self.mcp_matrix = self._normalize_matrix(self.mcp_matrix)
            
            # Génération de la matrice MCAP
            self.logger.info("Génération de la matrice MCAP")
            result = self.generate_mcap_matrix()
            if result is None or result.empty:
                raise ValueError("Échec de la génération de la matrice MCAP")
            
            # Traitement des résultats
            result['max_value'] = result.max(axis=1)
            result['first_best_profile'] = result.idxmax(axis=1)
            
            # Création de la matrice de classement
            self.ranking_matrix = pd.DataFrame(index=result.index, columns=['Top1', 'Top2', 'Top3'])
            ranking_results = []
            
            for activity in result.index:
                scores = pd.to_numeric(result.loc[activity, result.columns[:-2]])
                sorted_scores = scores.sort_values(ascending=False)
                
                top3_indices = sorted_scores.index[:3]
                top3_values = sorted_scores.values[:3]
                
                self.ranking_matrix.loc[activity] = [
                    f"{top3_indices[0]} ({top3_values[0]:.3f})",
                    f"{top3_indices[1]} ({top3_values[1]:.3f})",
                    f"{top3_indices[2]} ({top3_values[2]:.3f})"
                ]
                
                activity_results = [
                    f"Activité: {activity}",
                    "-" * 40
                ]
                activity_results.extend(
                    f"{rank}. {profile}: {score:.3f}"
                    for rank, (profile, score) in enumerate(sorted_scores.items(), 1)
                )
                activity_results.append("")
                ranking_results.append("\n".join(activity_results))
            
            self.ranking_results = "\n".join(ranking_results)
            
            # Sauvegarde des résultats
            os.makedirs(self.output_dir, exist_ok=True)
            self.ranking_matrix.to_csv(os.path.join(self.output_dir, 'ranking_matrix.csv'))
            
            with open(os.path.join(self.output_dir, 'ranking_results.txt'), 'w') as f:
                f.write("Classement des profils par activité\n")
                f.write("==================================\n\n")
                f.write(self.ranking_results)
            
            # Génération des graphiques
            result_without_stats = result.drop(['max_value', 'first_best_profile'], axis=1)
            self.plot_results(result_without_stats)
            self.plot_radar(result_without_stats)
            
            # Retour des résultats
            results_dict = {
                'ranking_matrix': self.ranking_matrix,
                'ranking_results': self.ranking_results,
                'result_matrix': result
            }
            
            self.logger.info("Traitement MCAP terminé avec succès")
            return results_dict
            
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement MCAP: {str(e)}")
            self.logger.exception(e)
            # Créer un dictionnaire de résultats vide mais valide
            empty_results = {
                'ranking_matrix': pd.DataFrame(),
                'ranking_results': str(e),
                'result_matrix': pd.DataFrame() if result is None else result
            }
            raise ValueError(f"Erreur lors du traitement MCAP: {str(e)}")