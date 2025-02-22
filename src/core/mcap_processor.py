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
        self.is_web_request = is_web_request  # Store the flag telling if this is a web request

        # Parameters validation
        valid_mcap_functions = ['sum', 'mean', 'sqrt']
        if self.mcap_function not in valid_mcap_functions:
            raise ValueError(f"mcap_function doit être l'un des suivants: {valid_mcap_functions}")

        valid_scale_types = ['0-1', 'free']
        if self.scale_type not in valid_scale_types:
            raise ValueError(f"scale_type doit être l'un des suivants: {valid_scale_types}")

        # Adjust root directory based on request type
        if is_web_request:
            # For web requests, navigate up one directory less
            self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        else:
            # For command-line/local requests, use the standard path
            self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        logger.info(f"Root directory: {self.root_dir}")
        

        self.output_dir = os.path.join(self.root_dir, 'data', 'output')
        logger.info(f"Output directory: {self.output_dir}")
        self.figures_dir = os.path.join(self.output_dir, 'figures')
        os.makedirs(self.figures_dir, exist_ok=True)
        logger.info(f"Figures directory: {self.figures_dir}")
        self.mcap_matrix_path = os.path.join(self.output_dir, 'mcap_matrix.csv')
        self.ranking_matrix_path = os.path.join(self.output_dir, 'ranking_matrix.csv')
        # clear output directory
        self._purge_output()

        # Initialize figures dictionary
        self.figures = {}  # Add this line to initialize the figures attribute

        # log parameters
        self.logger.info(f"Initialized processor with parameters:")
        self.logger.info(f"- mca_matrix shape: {self.mca_matrix.shape}")
        self.logger.info(f"- mcp_matrix: {self.mcp_matrix.head(10)}")
        self.logger.info(f"- mcp_matrix shape: {self.mcp_matrix.shape}")
        self.logger.info(f"- mcp_matrix: {self.mcp_matrix.head(10)}")
        self.logger.info(f"- model_function: {self.model_function.__name__}")
        self.logger.info(f"- scale_type: {self.scale_type}")
        self.logger.info(f"- mcap_function: {self.mcap_function}")
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
        
        # Plot data as bar chart
        result_matrix.plot(kind=kind, ax=ax, stacked=False)
        
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

            # Initialize result matrix with Activities as rows and Profiles as columns
            result = pd.DataFrame(
                np.zeros((len(self.mca_matrix.index), len(self.mcp_matrix.index))),
                index=self.mca_matrix.index,     
                columns=self.mcp_matrix.index,    
                dtype=float
            )

            # Calculate matrix values
            for activity in self.mca_matrix.index:
                for profile in self.mcp_matrix.index:
                    scores = []
                    for comp in self.mca_matrix.columns:
                        mca_value = float(self.mca_matrix.loc[activity, comp])
                        mcp_value = float(self.mcp_matrix.loc[profile, comp])
                        score = self.model_function(mcp_value, mca_value)
                        scores.append(score)
                    
                    # Calculate final score based on MCAP function
                    if self.mcap_function == 'mean':
                        final_score = np.mean(scores)
                    elif self.mcap_function == 'sum':
                        final_score = np.sum(scores)
                    elif self.mcap_function == 'sqrt':
                        final_score = np.sqrt(np.sum(np.square(scores)))
                    elif self.mcap_function == 'custom':
                        final_score = self.mcap_function(scores)
                    else:
                        raise ValueError(f"Unknown MCAP function: {self.mcap_function}")
                    
                    
                    result.loc[activity, profile] = final_score

            # Save matrix immediately after generation
            self._save_mcap_matrix(result)
            return result

        except Exception as e:
            self.logger.error(f"Error generating MCAP matrix: {str(e)}", exc_info=True)
            raise

    def _save_mcap_matrix(self, mcap_matrix):
        """Internal method to save MCAP matrix"""
        try:
            output_path = os.path.join(self.output_dir, 'mcap_matrix.txt')
            
            # Format matrix for output
            header = "Matrice MCAP (Activités x Profils)\n"
            header += "=" * 100 + "\n\n"
            
            # Convert matrix to string with proper formatting
            matrix_str = mcap_matrix.round(3).to_string(
                float_format=lambda x: '{:.3f}'.format(x),
                justify='right'
            )
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(header)
                f.write(matrix_str)
                f.write('\n')
            
            self.logger.info(f"Matrice MCAP sauvegardée dans: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving MCAP matrix: {str(e)}")
            raise
        

    def _save_ranking_matrix(self, mcap_matrix):
        """Generate and save ranking matrix showing top 3 profiles for each activity"""
        try:
            # Get top 3 profiles for each activity
            ranking_data = []
            for idx, activity in enumerate(mcap_matrix.index):
                row = mcap_matrix.loc[activity]
                # Sort profiles by score in descending order
                top_profiles = row.sort_values(ascending=False).head(3)
                
                # Format data for this activity
                activity_data = {
                    'Activity': activity,
                    'Rank 1': f"{top_profiles.index[0]} ({top_profiles.values[0]:.3f})",
                    'Rank 2': f"{top_profiles.index[1]} ({top_profiles.values[1]:.3f})",
                    'Rank 3': f"{top_profiles.index[2]} ({top_profiles.values[2]:.3f})"
                }
                ranking_data.append(activity_data)
            
            # Create DataFrame and save
            ranking_df = pd.DataFrame(ranking_data)
            
            ranking_df.to_csv(os.path.join(self.output_dir, self.ranking_matrix_path), index=False)
            self.logger.info(f"Ranking matrix saved to: {self.ranking_matrix_path}")
            
            return ranking_df
        except Exception as e:
            self.logger.error(f"Error saving ranking matrix: {str(e)}")
            raise

    """ 
    def process(self):
        try:
            self.logger.info("Starting MCAP processing")
            
            # Generate MCAP matrix first
            mcap_matrix = self.generate_mcap_matrix()
            
            if (mcap_matrix.empty):
                raise ValueError("Generated MCAP matrix is empty")
                
            # Create plots using the raw matrix
            self.plot_results(mcap_matrix)
            self.plot_radar(mcap_matrix)
            
            # Save matrices
            mcap_matrix.to_csv(self.mcap_matrix_path)
            self._save_ranking_matrix(mcap_matrix)
            
            return {
                'mcap_matrix': mcap_matrix,
                'ranking_matrix': None  # Remove ranking matrix from output
            }
            
        except Exception as e:
            self.logger.error(f"Error during MCAP processing: {str(e)}")
            raise
    """       
    
    
    def _calculate_rankings(self, mcap_matrix):
        """Calculate rankings for each activity based on MCAP scores"""
        try:
            # Create a DataFrame for storing rankings
            rankings_df = pd.DataFrame(columns=['Activity', 'Rank1', 'Score1', 'Rank2', 'Score2', 'Rank3', 'Score3'])
            
            # For each activity (row in MCAP matrix)
            for idx, activity in enumerate(mcap_matrix.index):
                # Get scores for this activity
                scores = mcap_matrix.iloc[idx]
                # Sort profiles by score in descending order
                sorted_scores = scores.sort_values(ascending=False)
                
                # Get top 3 profiles and their scores
                top3 = {
                    'Activity': activity,
                    'Rank1': sorted_scores.index[0],
                    'Score1': sorted_scores.iloc[0],
                    'Rank2': sorted_scores.index[1],
                    'Score2': sorted_scores.iloc[1],
                    'Rank3': sorted_scores.index[2],
                    'Score3': sorted_scores.iloc[2]
                }
                rankings_df = pd.concat([rankings_df, pd.DataFrame([top3])], ignore_index=True)
            
            # Save rankings to CSV
            output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                                     'data', 'output', 'ranking_matrix.csv')
            rankings_df.to_csv(output_path, index=False)
            self.logger.info(f"Rankings matrix saved to: {output_path}")
            
            return rankings_df
            
        except Exception as e:
            self.logger.error(f"Error calculating rankings: {str(e)}")
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
            self.logger.info(f"Fonction modèle: {self.model_function.__name__}")
            self.logger.info(f"Type d'échelle: {self.scale_type}")
            self.logger.info(f"Fonction MCAP: {self.mcap_function}")
            
            
            # Vérifier les dimensions des matrices (same competencies for both MCA and MCP)
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
            
            # save ranking matrix
            self._save_ranking_matrix(result_without_stats)
            self.logger.info(f"Ranking matrix saved to: {self.ranking_matrix_path}")
            
            # Sauvegarder la matrice dans le format Activities x Profiles
            matrix_file = os.path.join(self.output_dir, 'mcap_matrix.txt')
            with open(matrix_file, 'w', encoding='utf-8') as f:
                f.write("Matrice de résultats (Activités x Profils)\n")
                f.write("=====================================\n\n")
                f.write(result_without_stats.to_string(float_format=lambda x: '{:.3f}'.format(x)))
                f.write('\n')
            
            self.logger.info(f"Matrice MCAP sauvegardée dans: {matrix_file}")
            # save mcap matrix
            self._save_mcap_matrix(result_without_stats)
            self.logger.info(f"MCAP matrix saved to: {self.mcap_matrix_path}")
            
            
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
        
        
    def _purge_output(self):
        """cleanup output files"""
        try:
            os.removedirs(self.figures_dir)
            #os.removedirs(self.output_dir)
            self.logger.info("Output files and figures purged successfully")
        except Exception as e:
            self.logger.error(f"Error purging output files: {str(e)}")