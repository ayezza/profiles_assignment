import pandas as pd
import numpy as np

class FileUtils:
    @staticmethod
    def load_csv_file(file_path):
        try:
            # Essayer différentes configurations de lecture
            for sep in [',', ';']:
                for decimal in ['.', ',']:
                    try:
                        df = pd.read_csv(file_path, 
                                       index_col=0, 
                                       sep=sep, 
                                       decimal=decimal,
                                       thousands=None)
                        
                        # Vérifier si les colonnes de données contiennent des valeurs numériques
                        numeric_data = df.select_dtypes(include=[np.number])
                        if not numeric_data.empty and numeric_data.shape[1] == df.shape[1]:
                            return df
                    except:
                        continue
            
            # Si aucune tentative n'a réussi
            raise ValueError("La matrice doit contenir uniquement des valeurs numériques (sauf la colonne d'index)")
                
        except Exception as e:
            raise Exception(f"Erreur lors du chargement du fichier {file_path}: {str(e)}") 