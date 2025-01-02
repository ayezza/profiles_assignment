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

class McapProcessor:
    def __init__(self, logger, mca_matrix, mcp_matrix, model_function, normalize=True, 
                 norm='l2', axis=1, copy=False, return_norm=False, scale_type='0-1'):
        self.logger = logger
        self.mca_matrix = pd.DataFrame(mca_matrix)
        self.mcp_matrix = pd.DataFrame(mcp_matrix)
        self.model_function = model_function
        self.normalize = normalize
        self.norm = norm
        self.axis = axis
        self.copy = copy
        self.return_norm = return_norm
        self.scale_type = scale_type  # '0-1' ou 'free'

    def _normalize_matrix(self, matrix):
        """Normalise la matrice selon le type d'échelle"""
        if self.scale_type == '0-1':
            # Vérifier si les valeurs sont entre 0 et 1
            if (matrix.values < 0).any() or (matrix.values > 1).any():
                raise ValueError("Pour l'échelle 0-1, toutes les valeurs doivent être entre 0 et 1")
            if self.normalize:
                return pd.DataFrame(
                    preprocessing.normalize(matrix, norm=self.norm, axis=self.axis),
                    index=matrix.index,
                    columns=matrix.columns
                )
            return matrix
        else:  # 'free'
            # Normalisation min-max pour ramener à l'échelle [0,1]
            normalized = pd.DataFrame(
                preprocessing.MinMaxScaler().fit_transform(matrix),
                index=matrix.index,
                columns=matrix.columns
            )
            if self.normalize:
                normalized = pd.DataFrame(
                    preprocessing.normalize(normalized, norm=self.norm, axis=self.axis),
                    index=matrix.index,
                    columns=matrix.columns
                )
            return normalized

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
        
        # Utiliser le même style de nom de fichier que pour le radar
        plt.savefig(f'data/output/figures/affectation_bar_{uuid.uuid4()}.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()

    def plot_radar(self, result_matrix):
        """Génère un graphique radar (pentagone) pour chaque activité"""
        # Nettoyer result_matrix en supprimant les colonnes de statistiques
        if 'max_value' in result_matrix.columns:
            result_matrix = result_matrix.drop(['max_value'], axis=1)
        if 'first_best_profile' in result_matrix.columns:
            result_matrix = result_matrix.drop(['first_best_profile'], axis=1)
        
        # Créer le répertoire de sortie
        output_dir = os.path.abspath('data/output/figures')
        os.makedirs(output_dir, exist_ok=True)
        
        # Paramètres pour le graphique radar
        angles = np.linspace(0, 2*np.pi, 5, endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))
        
        # Générer une palette de couleurs en utilisant les noms réels des profils
        colors = {}
        base_colors = [
            '#e74c3c', '#2ecc71', '#3498db', '#f1c40f', '#9b59b6',
            '#e67e22', '#1abc9c', '#34495e', '#d35400', '#27ae60'
        ]
        
        for i, profile in enumerate(result_matrix.columns):
            if i < len(base_colors):
                colors[profile] = base_colors[i]
            else:
                # Générer des couleurs supplémentaires si nécessaire
                hue = i / len(result_matrix.columns)
                rgb = plt.cm.hsv(hue)[:3]
                colors[profile] = rgb
        
        # Créer une figure par activité
        for activity, scores in result_matrix.iterrows():
            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
            
            # Tracer le pentagone pour chaque profil
            for profile in result_matrix.columns:
                profile_score = np.full(5, scores[profile])
                profile_score = np.concatenate((profile_score, [profile_score[0]]))
                
                ax.plot(angles, profile_score, 'o-', 
                       linewidth=1,
                       markersize=3,
                       label=f"{profile} ({scores[profile]:.2f})",
                       color=colors[profile],
                       alpha=0.7)
                ax.fill(angles, profile_score, 
                       alpha=0.05,
                       color=colors[profile])
            
            # Configurer l'apparence
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(['Score\nmoyen', 'Score\nmax', 'Score\nmin', 
                              'Score\nmédian', 'Score\nmoyen'], size=8)
            ax.set_title(f'Activité: {activity}', pad=20, size=10)
            
            # Définir les limites et la grille
            max_value = result_matrix.values.max()
            max_limit = np.ceil(max_value)
            ax.set_ylim(0, max_limit)
            ax.grid(True, alpha=0.3)
            
            # Ajouter les graduations
            ticks = np.linspace(0, max_limit, 5)
            ax.set_rticks(ticks)
            ax.set_yticklabels([f'{tick:.1f}' for tick in ticks], fontsize=8)
            
            # Ajouter la légende
            ax.legend(bbox_to_anchor=(1.2, 1), 
                     loc='upper left', 
                     fontsize=8,
                     title="Profils (scores)")
            
            plt.tight_layout()
            
            # Sauvegarder le graphique
            output_file = os.path.join(output_dir, f'radar_pentagon_{activity}_{uuid.uuid4()}.png')
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close(fig)

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
            
            # Appliquer la fonction de modèle
            for i in range(self.mca_matrix.shape[0]):
                for j in range(self.mcp_matrix.shape[0]):
                    score = 0
                    for k in range(self.mca_matrix.shape[1]):
                        score += self.model_function(
                            self.mcp_matrix.iloc[j, k],
                            self.mca_matrix.iloc[i, k]
                        )
                    result.iloc[i, j] = score
            
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
            output_dir = os.path.abspath('data/output')
            os.makedirs(output_dir, exist_ok=True)
            
            # Sauvegarder en CSV
            ranking_file = os.path.join(output_dir, 'ranking_matrix.csv')
            ranking_matrix.to_csv(ranking_file)
            self.logger.info(f"\nMatrice de classement sauvegardée dans: {ranking_file}")
            
            # Sauvegarder en format texte plus lisible
            text_file = os.path.join(output_dir, 'ranking_results.txt')
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
            self.logger.info("\nGénération des graphiques...")
            result_without_stats = result.drop(['max_value', 'first_best_profile'], axis=1)
            self.plot_results(result_without_stats)
            self.plot_radar(result_without_stats)
            
            return 0
            
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement MCAP: {str(e)}")
            raise  # Propager l'erreur pour plus de détails 