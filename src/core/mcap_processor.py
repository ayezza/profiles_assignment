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
from src.models.mcap_functions import McapFunctions  # Add this import at the top

class McapProcessor:
    def __init__(self, logger, mca_matrix, mcp_matrix, model_function, mcap_function='mean', 
                 normalize=True, norm='l2', axis=1, copy=False, return_norm=False, 
                 scale_type='0-1', is_web_request=False):  # Add is_web_request parameter with default False
        self.logger = logger
        self.mca_matrix = pd.DataFrame(mca_matrix)
        self.mcp_matrix = pd.DataFrame(mcp_matrix)
        self.model_function = model_function
        self.mcap_function = mcap_function.lower()
        self.normalize = normalize
        self.scale_type = scale_type.lower()
        self.norm = norm
        self.axis = axis
        self.is_web_request = is_web_request  # Store the flag

        # Validation des paramètres
        valid_mcap_functions = ['sum', 'mean', 'sqrt']
        if self.mcap_function not in valid_mcap_functions:
            raise ValueError(f"mcap_function doit être l'un des suivants: {valid_mcap_functions}")

        valid_scale_types = ['0-1', 'free']
        if self.scale_type not in valid_scale_types:
            raise ValueError(f"scale_type doit être l'un des suivants: {valid_scale_types}")

        # Adjust root directory based on request type
        if is_web_request:
            self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        else:
            self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        self.output_dir = os.path.join(self.root_dir, 'data', 'output')
        self.figures_dir = os.path.join(self.output_dir, 'figures')
        os.makedirs(self.figures_dir, exist_ok=True)

        # Initialize figures dictionary
        self.figures = {}  # Add this line to initialize the figures attribute

        self.logger.info(f"Initialized processor with parameters:")
        self.logger.info(f"- mcap_function: {self.mcap_function}")
        self.logger.info(f"- scale_type: {self.scale_type}")
        self.logger.info(f"- normalize: {self.normalize}")
        self.logger.info(f"- norm: {self.norm}")
        self.logger.info(f"- axis: {self.axis}")
        self.logger.info(f"- is_web_request: {self.is_web_request}")

    def _normalize_matrix(self, matrix):
        """Normalize matrix based on scale type"""
        try:
            if self.scale_type == '0-1':
                self.logger.info("Applying 0-1 scaling")
                min_val = matrix.min().min()
                max_val = matrix.max().max()
                if max_val - min_val == 0:
                    self.logger.warning("Matrix has zero range, returning original matrix")
                    return matrix
                return (matrix - min_val) / (max_val - min_val)
            else:  # 'free'
                if self.normalize:
                    self.logger.info(f"Applying normalization with norm={self.norm}, axis={self.axis}")
                    # Vérifier si les données sont appropriées pour la normalisation
                    if matrix.std().min() == 0:
                        self.logger.warning("Standard deviation is zero, skipping normalization")
                        return matrix
                    normalized = (matrix - matrix.mean()) / matrix.std()
                    return pd.DataFrame(
                        preprocessing.normalize(normalized, norm=self.norm, axis=self.axis),
                        index=matrix.index,
                        columns=matrix.columns
                    )
                return matrix
        except Exception as e:
            self.logger.error(f"Error during normalization: {str(e)}")
            raise

    def plot_results(self, result_matrix, kind="bar"):
        """Génère un graphique des résultats"""
        # Create figure with larger size and tighter layout
        fig = plt.figure(figsize=(15, 8))
        ax = fig.add_subplot(111)
        
        # Plot transposed data for better visualization
        result_matrix.T.plot(kind=kind, ax=ax, stacked=False)
        
        plt.title("Matrice d'affectation - Poids des profils par activité")
        plt.xlabel('Profils')
        plt.ylabel('Poids')
        
        # Adjust legend position and size
        plt.legend(
            title='Activités',
            bbox_to_anchor=(1.05, 1),
            loc='upper left',
            borderaxespad=0,
            fontsize='small'
        )
        
        # Add grid and adjust layout
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Store figure in figures dictionary with specific layout adjustments
        fig.subplots_adjust(right=0.85)  # Make room for legend
        self.figures['bar_plot'] = fig
        
        # Save to file with high quality settings
        output_file = os.path.join(self.figures_dir, f'affectation_bar_{uuid.uuid4()}.png')
        plt.savefig(
            output_file,
            dpi=150,  # Lower DPI for better web display
            bbox_inches='tight',
            pad_inches=0.5,
            format='png'
        )
        plt.close()

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
            
            # Store the figure in the figures dictionary
            self.figures[f'radar_plot_{activity}'] = fig  # Add this line to store each radar plot
            
            # Sauvegarder le graphique
            output_file = os.path.join(self.figures_dir, f'radar_pentagon_{activity}_{uuid.uuid4()}.png')
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()

    def generate_mcap_matrix(self):
        """Generate MCAP matrix using current parameters"""
        try:
            self.logger.info("=== MCAP Matrix Generation ===")
            self.logger.info(f"Using model function: {self.model_function.__name__ if hasattr(self.model_function, '__name__') else 'lambda'}")
            self.logger.info(f"Using MCAP function: {self.mcap_function}")
            self.logger.info(f"Using scale type: {self.scale_type}")

            # Créer la matrice avec Activities en lignes et Profiles en colonnes
            result = pd.DataFrame(
                index=self.mca_matrix.index,     # Activities en lignes
                columns=self.mcp_matrix.index,    # Profiles en colonnes
                dtype=float
            )

            # Normaliser les matrices si nécessaire
            mca_normalized = self._normalize_matrix(self.mca_matrix.copy())
            mcp_normalized = self._normalize_matrix(self.mcp_matrix.copy())

            # Use McapFunctions directly
            mcap_fun = McapFunctions.get_mcap_function(self.mcap_function)

            # Pour chaque activité (lignes)
            for activity in mca_normalized.index:
                # Pour chaque profil (colonnes)
                for profile in mcp_normalized.index:
                    scores = []
                    # Pour chaque compétence
                    for comp in mca_normalized.columns:
                        mcp_value = float(mcp_normalized.loc[profile, comp])
                        mca_value = float(mca_normalized.loc[activity, comp])
                        score = self.model_function(mcp_value, mca_value)
                        scores.append(score)
                    
                    # Calculer le score final selon la fonction MCAP choisie
                    if self.mcap_function == 'mean':
                        result.loc[activity, profile] = np.mean(scores)
                    elif self.mcap_function == 'sum':
                        result.loc[activity, profile] = np.sum(scores)
                    elif self.mcap_function == 'sqrt':
                        result.loc[activity, profile] = np.sqrt(np.sum(np.square(scores)))
                    else:
                        result.loc[activity, profile] = self.model_function(scores)

            self.logger.info(f"Generated matrix shape: {result.shape}")
            self.logger.info(f"Matrix orientation: Activities (rows) x Profiles (columns)")
            return result

        except Exception as e:
            self.logger.error(f"Error generating MCAP matrix: {str(e)}", exc_info=True)
            raise

    def process(self):
        try:
            self.logger.info("Starting MCAP processing")
            self.logger.info(f"Using parameters:")
            self.logger.info(f"- MCAP function: {self.mcap_function}")
            self.logger.info(f"- Scale type: {self.scale_type}")
            self.logger.info(f"- Normalization: {self.normalize}")
            
            # Vérification des données
            if self.mca_matrix.empty or self.mcp_matrix.empty:
                raise ValueError("Les matrices MCA ou MCP sont vides")
            
            self.logger.info(f"Dimensions MCA: {self.mca_matrix.shape}")
            self.logger.info(f"Dimensions MCP: {self.mcp_matrix.shape}")
            self.logger.info(f"Type d'échelle: {self.scale_type}")
            
            # Vérifier les dimensions des matrices
            if self.mca_matrix.shape[1] != self.mcp_matrix.shape[1]:
                raise ValueError(f"Les dimensions des matrices ne correspondent pas: MCA={self.mca_matrix.shape}, MCP={self.mcp_matrix.shape}")
            
            # Vérifier les valeurs NaN
            if self.mca_matrix.isna().any().any() or self.mcp_matrix.isna().any().any():
                raise ValueError("Les matrices contiennent des valeurs NaN")
            
            # Afficher les plages de valeurs avant normalisation
            self.logger.info(f"Plage de valeurs MCA: [{self.mca_matrix.values.min():.2f}, {self.mca_matrix.values.max():.2f}]")
            self.logger.info(f"Plage de valeurs MCP: [{self.mcp_matrix.values.min():.2f}, {self.mcp_matrix.values.max():.2f}]")
            
            # Normaliser les matrices si demandé
            if self.normalize:
                self.logger.info("Normalisation des matrices")
                self.mca_matrix = self._normalize_matrix(self.mca_matrix)
                self.mcp_matrix = self._normalize_matrix(self.mcp_matrix)
            
            # Calculer la matrice de résultats (Activities x Profiles)
            result = self.generate_mcap_matrix()
            
            # Ne PAS transposer la matrice - garder Activities x Profiles
            result_without_stats = result.copy()
            
            # Ajouter les colonnes supplémentaires
            result['max_value'] = result.max(axis=1)
            result['first_best_profile'] = result.idxmax(axis=1)
            
            # Créer la matrice de classement
            ranking_matrix = pd.DataFrame(index=result.index, columns=['Top1', 'Top2', 'Top3'])
            for activity in result.index:
                scores = pd.to_numeric(result.loc[activity, result.columns[:-2]])
                sorted_scores = scores.sort_values(ascending=False)
                top3_indices = sorted_scores.index[:3]
                top3_values = sorted_scores.values[:3]
                ranking_matrix.loc[activity] = [
                    f"{top3_indices[0]} ({top3_values[0]:.3f})",
                    f"{top3_indices[1]} ({top3_values[1]:.3f})",
                    f"{top3_indices[2]} ({top3_values[2]:.3f})"
                ]
            
            # Sauvegarder la matrice dans le format Activities x Profiles
            matrix_file = os.path.join(self.output_dir, 'mcap_matrix.txt')
            with open(matrix_file, 'w', encoding='utf-8') as f:
                f.write("Matrice de résultats (Activités x Profils)\n")
                f.write("=====================================\n\n")
                f.write(result_without_stats.to_string(float_format=lambda x: '{:.3f}'.format(x)))
                f.write('\n')
            
            self.logger.info(f"Matrice MCAP sauvegardée dans: {matrix_file}")
            
            # Générer les graphiques avec la matrice Activities x Profiles
            result_without_stats = result.drop(['max_value', 'first_best_profile'], axis=1)
            self.plot_results(result_without_stats)
            self.plot_radar(result_without_stats)
            
            # Create detailed ranking results string
            ranking_results = []
            for activity in result.index:
                scores = pd.to_numeric(result.loc[activity, result.columns[:-2]])
                sorted_scores = scores.sort_values(ascending=False)
                
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
            
            # Final formatted string
            ranking_results_str = "\n".join(ranking_results)
            
            # Return all results including ranking_results
            return {
                'ranking_matrix': ranking_matrix,
                'result_matrix': result_without_stats,
                'ranking_results': ranking_results_str  # Add this line
            }
            
        except Exception as e:
            self.logger.error(f"MCAP processing error: {str(e)}")
            raise  # Propager l'erreur pour plus de détails