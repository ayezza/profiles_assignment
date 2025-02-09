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

class McapProcessor:
    def __init__(self, logger, mca_matrix, mcp_matrix, model_function, mcap_function='sum', 
                 normalize=True, scale_type='0-1'):
        self.logger = logger
        self.mca_matrix = pd.DataFrame(mca_matrix)
        self.mcp_matrix = pd.DataFrame(mcp_matrix)
        self.model_function = model_function
        self.mcap_function = mcap_function
        self.normalize = normalize
        self.scale_type = scale_type
        
        # Add missing attributes
        self.norm = 'l2'  # Default normalization method
        self.axis = 1     # Default axis for normalization

        # Setup directories
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.output_dir = os.path.join(self.root_dir, 'data', 'output')
        self.figures_dir = os.path.join(self.output_dir, 'figures')
        os.makedirs(self.figures_dir, exist_ok=True)

        self.logger.info(f"Initialized processor: mcap={mcap_function}, scale={scale_type}, norm={self.norm}")

    def _normalize_matrix(self, matrix):
        """Normalize matrix based on scale type"""
        if self.scale_type == '0-1':
            # Min-max scaling to [0,1]
            return (matrix - matrix.min()) / (matrix.max() - matrix.min())
        else:  # 'free'
            if self.normalize:
                # Standard normalization
                normalized = (matrix - matrix.mean()) / matrix.std()
                return pd.DataFrame(
                    preprocessing.normalize(normalized, norm=self.norm, axis=self.axis),
                    index=matrix.index,
                    columns=matrix.columns
                )
            return matrix

    def plot_results(self, result_matrix, kind="bar"):
        """Génère un graphique des résultats"""
        plt.figure(figsize=(12, 7))
        result_matrix.plot(kind=kind, stacked=False)
        plt.title("Matrice d'affectation - Poids des profils par activité")
        plt.xlabel('Activités')
        plt.ylabel('Poids des profils')
        plt.legend(title='Profils', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Utiliser le chemin absolu pour sauvegarder
        output_file = os.path.join(self.figures_dir, f'affectation_bar_{uuid.uuid4()}.png')
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
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
            
            # Sauvegarder le graphique
            output_file = os.path.join(self.figures_dir, f'radar_pentagon_{activity}_{uuid.uuid4()}.png')
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()

    def generate_mcap_matrix(self):
        """Generate MCAP matrix using current parameters"""
        self.logger.info(f"Generating MCAP matrix with function: {self.mcap_function}")
        
        result = pd.DataFrame(
            np.zeros((self.mca_matrix.shape[0], self.mcp_matrix.shape[0])),
            index=self.mca_matrix.index,
            columns=self.mcp_matrix.index
        )
        
        # Apply scaling if needed
        if self.scale_type == '0-1':
            self.mca_matrix = (self.mca_matrix - self.mca_matrix.min()) / (self.mca_matrix.max() - self.mca_matrix.min())
            self.mcp_matrix = (self.mcp_matrix - self.mcp_matrix.min()) / (self.mcp_matrix.max() - self.mcp_matrix.min())

        for i in self.mca_matrix.index:
            for j in self.mcp_matrix.index:
                scores = []
                for comp in self.mca_matrix.columns:
                    score = self.model_function(
                        float(self.mcp_matrix.loc[j, comp]),
                        float(self.mca_matrix.loc[i, comp])
                    )
                    scores.append(score)
                
                # Apply selected MCAP function
                if self.mcap_function == 'mean':
                    result.loc[i, j] = np.mean(scores)
                elif self.mcap_function == 'sum':
                    result.loc[i, j] = np.sum(scores)
                elif self.mcap_function == 'sqrt':
                    result.loc[i, j] = np.sqrt(np.sum(np.square(scores)))

        return result

    def process(self):
        try:
            self.logger.info("Début du traitement MCAP")
            
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
            
            # Calculer la matrice de résultats
            result = pd.DataFrame(
                np.zeros((self.mca_matrix.shape[0], self.mcp_matrix.shape[0])),
                index=self.mca_matrix.index,
                columns=self.mcp_matrix.index
            )
            
            result = self.generate_mcap_matrix()

            # Ajouter les colonnes supplémentaires
            result['max_value'] = result.max(axis=1)
            result['first_best_profile'] = result.idxmax(axis=1)
            
            # Trier les profils par score pour chaque activité
            self.logger.info("\nClassement des profils par activité:")
            for activity in result.index:
                scores = pd.to_numeric(result.loc[activity, result.columns[:-2]])  # Conversion en numérique
                sorted_scores = scores.sort_values(ascending=False)
                
                self.logger.info(f"\nActivité {activity}:")
                for rank, (profile, score) in enumerate(sorted_scores.items(), 1):
                    self.logger.info(f"  {rank}. {profile}: {score:.3f}")
            
            # Créer une matrice de classement
            ranking_matrix = pd.DataFrame(index=result.index, columns=['Top1', 'Top2', 'Top3'])
            for activity in result.index:
                scores = pd.to_numeric(result.loc[activity, result.columns[:-2]])  # Conversion en numérique
                sorted_scores = scores.sort_values(ascending=False)
                top3_indices = sorted_scores.index[:3]
                top3_values = sorted_scores.values[:3]
                ranking_matrix.loc[activity] = [
                    f"{top3_indices[0]} ({top3_values[0]:.3f})",
                    f"{top3_indices[1]} ({top3_values[1]:.3f})",
                    f"{top3_indices[2]} ({top3_values[2]:.3f})"
                ]
            
            # Sauvegarder la matrice de classement
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Sauvegarder en CSV
            ranking_file = os.path.join(self.output_dir, 'ranking_matrix.csv')
            ranking_matrix.to_csv(ranking_file)
            self.logger.info(f"\nMatrice de classement sauvegardée dans: {ranking_file}")
            
            # Sauvegarder en format texte plus lisible
            text_file = os.path.join(self.output_dir, 'ranking_results.txt')
            with open(text_file, 'w') as f:
                f.write("Classement des profils par activité\n")
                f.write("==================================\n\n")
                for activity in result.index:
                    f.write(f"Activité: {activity}\n")
                    f.write("-" * 40 + "\n")
                    scores = result.loc[activity, result.columns[:-2]]
                    sorted_scores = scores.sort_values(ascending=False)
                    for rank, (profile, score) in enumerate(sorted_scores.items(), 1):
                        f.write(f"{rank}. {profile}: {score:.3f}\n")
                    f.write("\n")
            
            self.logger.info(f"Résultats détaillés sauvegardés dans: {text_file}")
            
            # Générer les graphiques
            try:
                os.makedirs(self.figures_dir, exist_ok=True)
            except Exception as e:
                self.logger.error(f"Erreur lors de la création du dossier: {self.figures_dir}")
                raise
            self.logger.info("\nGénération des graphiques...")
            result_without_stats = result.drop(['max_value', 'first_best_profile'], axis=1)

            self.logger.info(f"Données passées à plot_results: {result_without_stats}")
            self.plot_results(result_without_stats)

            self.logger.info(f"Données passées à plot_radar: {result_without_stats}")
            self.plot_radar(result_without_stats)
            
            return {'ranking_matrix': ranking_matrix, 'result_matrix': result_without_stats}
            
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement MCAP: {str(e)}")
            raise  # Propager l'erreur pour plus de détails