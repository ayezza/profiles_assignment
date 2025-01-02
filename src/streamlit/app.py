import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import pandas as pd
from src.core.mcap_processor import McapProcessor
from src.models.model_functions import ModelFunctions
import os

def run_streamlit_app():
    # Configuration de la page en mode large
    st.set_page_config(
        page_title="Affectation des Profils",
        page_icon="📊",
        layout="wide",  # Utilise toute la largeur disponible
        initial_sidebar_state="expanded"
    )
    
    st.cache_data.clear()
    st.title("Affectation des Profils")
    
    # Configuration de la page
    st.sidebar.header("Configuration")
    
    # Upload des fichiers
    mca_file = st.sidebar.file_uploader("Charger le fichier MCA", type=['csv'])
    mcp_file = st.sidebar.file_uploader("Charger le fichier MCP", type=['csv'])
    
    # Sélection du modèle
    model_options = {
        'Modèle 1': 'model1',
        'Modèle 2': 'model2',
        'Modèle 3': 'model3',
        'Modèle 4': 'model4',
        'Modèle 5': 'model5'
    }
    selected_model = st.sidebar.selectbox(
        "Choisir le modèle",
        options=list(model_options.keys())
    )
    
    # Sélection du type d'échelle avec explication
    st.sidebar.markdown("""
    ### Type d'échelle
    - **0-1** : Les données doivent déjà être normalisées entre 0 et 1
    - **free** : Les données seront automatiquement normalisées
    """)
    
    scale_type = st.sidebar.selectbox(
        "Choisir le type d'échelle",
        options=['free', '0-1'],  # Mettre 'free' par défaut
        index=0  # Sélectionner 'free' par défaut
    )
    
    if mca_file and mcp_file:
        try:
            # Lecture des fichiers avec plus de paramètres
            mca_data = pd.read_csv(mca_file, 
                                 index_col=0,
                                 sep=None,
                                 engine='python',
                                 decimal=',',
                                 dtype=str)  # Lire toutes les colonnes comme texte d'abord
            mcp_data = pd.read_csv(mcp_file,
                                 index_col=0,
                                 sep=None,
                                 engine='python',
                                 decimal=',',
                                 dtype=str)  # Lire toutes les colonnes comme texte d'abord
            
            # Conversion propre en numérique
            for df in [mca_data, mcp_data]:
                for col in df.columns:
                    # Nettoyer les données avant conversion
                    df[col] = (df[col]
                             .str.strip()  # Enlever les espaces
                             .str.replace(',', '.')  # Remplacer les virgules par des points
                             .str.replace(' ', '')  # Enlever les espaces dans les nombres
                             )
                    # Convertir en numérique
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Vérifier si la conversion a réussi
            if mca_data.isna().any().any():
                st.warning("Certaines valeurs dans MCA ont été converties en NaN. Vérifiez vos données.")
                st.write("Colonnes avec des NaN dans MCA:", mca_data.columns[mca_data.isna().any()].tolist())
            
            if mcp_data.isna().any().any():
                st.warning("Certaines valeurs dans MCP ont été converties en NaN. Vérifiez vos données.")
                st.write("Colonnes avec des NaN dans MCP:", mcp_data.columns[mcp_data.isna().any()].tolist())
                return
            
            # Vérifier et normaliser les données selon le type d'échelle
            if scale_type == '0-1':
                # Vérifier si les données sont déjà entre 0 et 1
                if ((mca_data.values < 0).any() or (mca_data.values > 1).any() or 
                    (mcp_data.values < 0).any() or (mcp_data.values > 1).any()):
                    st.error("""
                    Les données ne sont pas dans l'intervalle [0,1].
                    Pour des données non normalisées, utilisez l'option 'free'.
                    """)
                    return
            else:  # scale_type == 'free'
                # Normaliser les données entre 0 et 1
                from sklearn.preprocessing import MinMaxScaler
                scaler = MinMaxScaler()
                
                # Normaliser MCA
                mca_values = scaler.fit_transform(mca_data)
                mca_data = pd.DataFrame(
                    mca_values,
                    index=mca_data.index,
                    columns=mca_data.columns
                )
                
                # Normaliser MCP
                mcp_values = scaler.fit_transform(mcp_data)
                mcp_data = pd.DataFrame(
                    mcp_values,
                    index=mcp_data.index,
                    columns=mcp_data.columns
                )
                
                st.info("Les données ont été automatiquement normalisées entre 0 et 1")
            
            # Afficher les plages de valeurs après normalisation
            st.write("Plage de valeurs après traitement :")
            st.write(f"MCA : [{mca_data.values.min():.2f}, {mca_data.values.max():.2f}]")
            st.write(f"MCP : [{mcp_data.values.min():.2f}, {mcp_data.values.max():.2f}]")
            
            # Afficher les informations sur les données chargées
            st.write("Aperçu des données MCA :")
            st.write(f"Dimensions MCA : {mca_data.shape}")
            st.write(mca_data.head())
            
            st.write("Aperçu des données MCP :")
            st.write(f"Dimensions MCP : {mcp_data.shape}")
            st.write(mcp_data.head())
            
            # Configuration du logger avec plus de détails
            import logging
            logger = logging.getLogger('streamlit_logger')
            logger.setLevel(logging.INFO)
            
            # Créer un conteneur pour les logs
            log_container = st.expander("Logs de traitement", expanded=False)
            log_text = []
            
            # Ajout d'un handler pour collecter les logs
            class StreamlitHandler(logging.Handler):
                def emit(self, record):
                    log_msg = record.getMessage()
                    log_text.append(log_msg)
                    # Mettre à jour la zone de texte avec tous les logs
                    with log_container:
                        st.text_area(
                            "Détails du traitement",
                            value="\n".join(log_text),
                            height=200,
                            disabled=True
                        )
            
            logger.addHandler(StreamlitHandler())
            
            # Nettoyer le dossier des figures avant le traitement
            figures_dir = 'data/output/figures'
            os.makedirs(figures_dir, exist_ok=True)
            for f in os.listdir(figures_dir):
                if f.endswith('.png'):
                    os.remove(os.path.join(figures_dir, f))
            
            # Traitement MCAP
            model_function = getattr(ModelFunctions, f"model_function{selected_model[-1]}")
            processor = McapProcessor(
                logger=logger,
                mca_matrix=mca_data,
                mcp_matrix=mcp_data,
                model_function=model_function,
                scale_type=scale_type
            )
            
            # Exécution du traitement
            if processor.process() == 0:
                st.success("Traitement terminé avec succès!")
                
                # Affichage des résultats CSV
                if os.path.exists('data/output/ranking_matrix.csv'):
                    results = pd.read_csv('data/output/ranking_matrix.csv')
                    st.write("Résultats de l'affectation :")
                    st.dataframe(results)
                
                # Affichage des résultats détaillés en format texte
                if os.path.exists('data/output/ranking_results.txt'):
                    with open('data/output/ranking_results.txt', 'r') as f:
                        results_text = f.read()
                    
                    # Créer un expander avec un titre coloré
                    results_container = st.expander(
                        "📊 Résultats détaillés par activité",
                        expanded=False
                    )
                    with results_container:
                        st.markdown(
                            """
                            <div style='background-color: #0066cc; padding: 10px; border-radius: 5px;'>
                                <h3 style='color: white; margin: 0;'>Classement détaillé des profils</h3>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        st.text_area(
                            "",
                            value=results_text,
                            height=300,
                            disabled=True
                        )
                
                # Affichage des graphiques
                st.write("## Visualisations des résultats")
                
                # Récupérer et trier les fichiers de graphiques par type
                graph_files = os.listdir('data/output/figures')
                radar_graphs = sorted([f for f in graph_files if f.startswith('radar_pentagon_')])
                bar_graphs = sorted([f for f in graph_files if f.startswith('affectation_bar_')])
                
                # Afficher les graphiques radar
                if radar_graphs:
                    st.markdown("""
                    ### 📊 Graphiques Radar par Activité
                    Visualisation des scores pour chaque profil par activité
                    """)
                    
                    # Calculer le nombre de colonnes en fonction du nombre de graphiques
                    n_cols = min(2, len(radar_graphs))  # Maximum 2 colonnes
                    cols = st.columns(n_cols)
                    
                    for idx, fig_file in enumerate(radar_graphs):
                        with cols[idx % n_cols]:
                            st.image(
                                f'data/output/figures/{fig_file}',
                                use_column_width=True,
                                caption=f"Radar {idx+1}"
                            )
                
                # Afficher le graphique en barres
                if bar_graphs:
                    st.markdown("""
                    ### 📈 Vue d'ensemble des affectations
                    Distribution globale des scores par profil et activité
                    """)
                    for fig_file in bar_graphs:
                        st.image(
                            f'data/output/figures/{fig_file}',
                            use_column_width=True
                        )
            else:
                st.error("Une erreur s'est produite pendant le traitement")
                
        except Exception as e:
            st.error(f"Erreur détaillée : {str(e)}")
            st.error(f"Type d'erreur : {type(e).__name__}")
            import traceback
            st.error(f"Traceback : {traceback.format_exc()}")

if __name__ == "__main__":
    run_streamlit_app()