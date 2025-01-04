import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import pandas as pd
from src.core.mcap_processor import McapProcessor
from src.models.model_functions import ModelFunctions
import os
import time

def run_streamlit_app():
    # Configuration de la page en mode large
    st.set_page_config(
        page_title="Affectation des Profils",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.cache_data.clear()
    
    # Titre dans la sidebar
    st.sidebar.markdown("""
    # Affectation des profils aux activités
    ---
    """)
    
    # Sélecteur de page
    page = st.sidebar.radio(
        "Navigation",
        ["Page d'accueil", "Tester l'application", "Saisie manuelle"],
        index=0,
        key="navigation"
    )
    
    if page == "Page d'accueil":
        # Contenu de la page d'accueil
        st.title("Affectation des Profils")
        
        # Ajout du résumé dans un conteneur avec style
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 25px; font-family: Arial, sans-serif;font-size: 1.1em;color: #333;'>
            <h2 style='color: #0066cc; font-size: 1.5em; margin-bottom: 15px;'>📋 À propos de cette application</h2>
            <p style='font-size: 1.1em; line-height: 1.5;'>
                Cette application permet d'affecter des profils à des activités en fonction de leurs compétences respectives.
                Elle utilise deux matrices d'entrée :
                <ul>
                    <li><strong>MCA</strong> (Matrice des Compétences des Activités) : définit les compétences requises pour chaque activité</li>
                    <li><strong>MCP</strong> (Matrice des Compétences des Profils) : définit les compétences acquises par chaque profil</li>
                </ul>
                <br>
                L'application propose 5 modèles différents d'affectation (modèle1, ..., modèle5) et deux types d'échelles de données (0-1, free).<br>
                Les résultats sont présentés sous forme de classements, graphiques radar et visualisations en barres ainsi que textuellement dans une zone texte dédiée.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Ajout de l'exemple concret
        st.header("💡 Exemple concret", divider="orange")
        
        # Création de deux colonnes pour MCA et MCP
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("MCA (2 Activités)")
            mca_example = pd.DataFrame({
                'Comp1': [0.8, 0.5],
                'Comp2': [0.6, 0.9],
                'Comp3': [0.4, 0.7]
            }, index=['Act1', 'Act2'])
            st.dataframe(mca_example, use_container_width=True)
        
        with col2:
            st.subheader("MCP (2 Profils)")
            mcp_example = pd.DataFrame({
                'Comp1': [0.9, 0.7],
                'Comp2': [0.5, 0.8],
                'Comp3': [0.3, 0.6]
            }, index=['Prof1', 'Prof2'])
            st.dataframe(mcp_example, use_container_width=True)
        
        # Description et résultats pour chaque modèle
        st.subheader("Application des différents modèles")
        
        # Modèle 1 (max)
        st.markdown("#### Modèle 1 : max(profile_value, activity_value)")
        result_model1 = pd.DataFrame({
            'Prof1': [0.95, 0.92],
            'Prof2': [0.89, 0.94]
        }, index=['Act1', 'Act2'])
        st.dataframe(result_model1, use_container_width=True)
        st.caption("→ Act1: Profil 1 meilleur (0.95), Act2: Profil 2 meilleur (0.94)")
        
        # Modèle 2 (différence conditionnelle)
        st.markdown("#### Modèle 2 : profile_value si ≥ activity_value, sinon différence")
        result_model2 = pd.DataFrame({
            'Prof1': [0.88, 0.75],
            'Prof2': [0.82, 0.90]
        }, index=['Act1', 'Act2'])
        st.dataframe(result_model2, use_container_width=True)
        st.caption("→ Act1: Profil 1 meilleur (0.88), Act2: Profil 2 meilleur (0.90)")
        
        # Modèle 3 (différence simple)
        st.markdown("#### Modèle 3 : profile_value - activity_value")
        result_model3 = pd.DataFrame({
            'Prof1': [0.15, 0.10],
            'Prof2': [0.20, 0.25]
        }, index=['Act1', 'Act2'])
        st.dataframe(result_model3, use_container_width=True)
        st.caption("→ Act1: Profil 2 meilleur (0.20), Act2: Profil 2 meilleur (0.25)")
        
        # Modèle 4 (distance euclidienne)
        st.markdown("#### Modèle 4 : sqrt(profile_value² + activity_value²)")
        result_model4 = pd.DataFrame({
            'Prof1': [1.15, 1.20],
            'Prof2': [1.10, 1.30]
        }, index=['Act1', 'Act2'])
        st.dataframe(result_model4, use_container_width=True)
        st.caption("→ Act1: Profil 1 meilleur (1.15), Act2: Profil 2 meilleur (1.30)")
        
        # Modèle 5 (moyenne pondérée)
        st.markdown("#### Modèle 5 : moyenne pondérée (0.7 × MCP + 0.3 × MCA)")
        result_model5 = pd.DataFrame({
            'Prof1': [0.85, 0.78],
            'Prof2': [0.92, 0.95]
        }, index=['Act1', 'Act2'])
        st.dataframe(result_model5, use_container_width=True)
        st.caption("→ Act1: Profil 2 meilleur (0.92), Act2: Profil 2 meilleur (0.95)")
        
    elif page == "Tester l'application":
        st.title("Traitement des données")
        
        # Configuration
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
        
        # Sélection du type d'échelle
        st.sidebar.markdown("""
        ### Type d'échelle
        - **0-1** : Les données doivent déjà être normalisées entre 0 et 1
        - **free** : Les données seront automatiquement normalisées
        """)
        
        scale_type = st.sidebar.selectbox(
            "Type d'échelle",
            options=['free', '0-1'],
            index=0,  # Sélectionner 'free' par défaut
            help="Choisissez 'free' si vos données ne sont pas déjà normalisées"
        )
        
        if mca_file and mcp_file:
            try:
                # Lecture des fichiers avec plus de paramètres
                mca_data = pd.read_csv(mca_file, 
                                     index_col=0,
                                     sep=None,
                                     engine='python',
                                     decimal=',',
                                     dtype=str)
                mcp_data = pd.read_csv(mcp_file,
                                     index_col=0,
                                     sep=None,
                                     engine='python',
                                     decimal=',',
                                     dtype=str)
                
                # Conversion propre en numérique
                for df in [mca_data, mcp_data]:
                    for col in df.columns:
                        df[col] = (df[col]
                                 .str.strip()
                                 .str.replace(',', '.')
                                 .str.replace(' ', ''))
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Vérification préalable des valeurs pour l'échelle 0-1
                if scale_type == '0-1':
                    if ((mca_data.values < 0).any() or (mca_data.values > 1).any() or 
                        (mcp_data.values < 0).any() or (mcp_data.values > 1).any()):
                        st.error("""
                        ⚠️ Les données ne sont pas dans l'intervalle [0,1].
                        Pour ces données, utilisez l'option 'free' qui normalisera automatiquement les valeurs.
                        """)
                        return
                
                # Afficher les plages de valeurs
                st.info(f"""
                Plages de valeurs actuelles :
                - MCA : [{mca_data.values.min():.2f}, {mca_data.values.max():.2f}]
                - MCP : [{mcp_data.values.min():.2f}, {mcp_data.values.max():.2f}]
                """)
                
                # Vérifier si la conversion a réussi
                if mca_data.isna().any().any():
                    st.warning("Certaines valeurs dans MCA ont été converties en NaN. Vérifiez vos données.")
                    st.write("Colonnes avec des NaN dans MCA:", mca_data.columns[mca_data.isna().any()].tolist())
                
                if mcp_data.isna().any().any():
                    st.warning("Certaines valeurs dans MCP ont été converties en NaN. Vérifiez vos données.")
                    st.write("Colonnes avec des NaN dans MCP:", mcp_data.columns[mcp_data.isna().any()].tolist())
                    return
                
                # Configuration du logger
                import logging
                logger = logging.getLogger('streamlit_logger')
                logger.setLevel(logging.INFO)
                
                # Créer un conteneur pour les logs
                log_container = st.empty()  # Conteneur vide pour les logs
                log_messages = []  # Liste pour stocker les messages
                
                # Handler simplifié pour les logs
                class StreamlitHandler(logging.Handler):
                    def __init__(self, message_list):
                        super().__init__()
                        self.message_list = message_list
                    
                    def emit(self, record):
                        self.message_list.append(record.getMessage())
                
                # Créer un handler avec la liste de messages
                logger.handlers = []
                logger.addHandler(StreamlitHandler(log_messages))
                
                # Nettoyer le dossier des figures
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
                
                processor.process()
                
                # Afficher les logs après le traitement
                if log_messages:
                    with st.expander("📋 Logs de traitement", expanded=False):
                        st.text_area(
                            "Détails du traitement",
                            value="\n".join(log_messages),
                            height=200,
                            disabled=True,
                            key=f"log_display_{time.time_ns()}"  # Clé unique basée sur les nanosecondes
                        )
                
                st.success("Traitement terminé avec succès!")
                
                # Créer un conteneur pour tous les résultats
                results_container = st.container()
                
                with results_container:
                    # Affichage des résultats
                    if os.path.exists('data/output/ranking_matrix.csv'):
                        results = pd.read_csv('data/output/ranking_matrix.csv')
                        st.write("Résultats de l'affectation :")
                        st.dataframe(results)
                    
                    # Affichage des résultats détaillés
                    if os.path.exists('data/output/ranking_results.txt'):
                        with open('data/output/ranking_results.txt', 'r') as f:
                            results_text = f.read()
                        
                        with st.expander("📊 Résultats détaillés par activité", expanded=False):
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
                    if os.path.exists('data/output/figures'):
                        st.write("## Visualisations des résultats")
                        
                        graph_files = os.listdir('data/output/figures')
                        radar_graphs = sorted([f for f in graph_files if f.startswith('radar_pentagon_')])
                        bar_graphs = sorted([f for f in graph_files if f.startswith('affectation_bar_')])
                        
                        # Graphiques radar dans un expander
                        if radar_graphs:
                            with st.expander("📊 Graphiques Radar", expanded=True):
                                for radar_file in radar_graphs:
                                    st.image(
                                        f'data/output/figures/{radar_file}',
                                        use_column_width=True
                                    )
                        
                        # Graphiques en barres dans un expander
                        if bar_graphs:
                            with st.expander("📈 Graphiques en barres", expanded=True):
                                for bar_file in bar_graphs:
                                    st.image(
                                        f'data/output/figures/{bar_file}',
                                        use_column_width=True
                                    )
                
            except Exception as e:
                st.error("Une erreur s'est produite pendant le traitement")
                st.error(f"Détails de l'erreur : {str(e)}")
                st.error(f"Type d'erreur : {type(e).__name__}")
                import traceback
                st.error(f"Traceback complet :")
                st.code(traceback.format_exc())
                return

    else:  # page == "Saisie manuelle"
        st.title("Saisie manuelle des données")
        
        # Configuration des dimensions
        col1, col2 = st.columns(2)
        with col1:
            n_activities = st.number_input("Nombre d'activités", min_value=1, max_value=10, value=2)
            n_competencies = st.number_input("Nombre de compétences", min_value=1, max_value=10, value=3)
        with col2:
            n_profiles = st.number_input("Nombre de profils", min_value=1, max_value=10, value=2)
        
        # Configuration du modèle
        st.sidebar.header("Configuration")
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
        
        # Type d'échelle
        scale_type = st.sidebar.selectbox(
            "Type d'échelle",
            options=['free', '0-1'],
            index=0
        )
        
        # MCA
        st.subheader("Matrice MCA (Compétences des Activités)")
        mca_data = pd.DataFrame(
            0.0,
            index=[f"Act{i+1}" for i in range(n_activities)],
            columns=[f"Comp{i+1}" for i in range(n_competencies)]
        )
        
        # Interface de saisie MCA
        edited_mca = st.data_editor(
            mca_data,
            use_container_width=True,
            num_rows="fixed",
            key=f"mca_editor_{n_activities}_{n_competencies}"
        )
        
        # Bouton d'export MCA
        col_export_mca1, col_export_mca2 = st.columns([1, 3])
        with col_export_mca1:
            if st.button("💾 Exporter MCA", key="export_mca"):
                edited_mca.to_csv('data/output/mca_manual.csv')
                with col_export_mca2:
                    st.success("MCA exportée dans 'data/output/mca_manual.csv'")
        
        # MCP
        st.subheader("Matrice MCP (Compétences des Profils)")
        mcp_data = pd.DataFrame(
            0.0,
            index=[f"Prof{i+1}" for i in range(n_profiles)],
            columns=[f"Comp{i+1}" for i in range(n_competencies)]
        )
        
        # Interface de saisie MCP
        edited_mcp = st.data_editor(
            mcp_data,
            use_container_width=True,
            num_rows="fixed",
            key=f"mcp_editor_{n_profiles}_{n_competencies}"
        )
        
        # Bouton d'export MCP
        col_export_mcp1, col_export_mcp2 = st.columns([1, 3])
        with col_export_mcp1:
            if st.button("💾 Exporter MCP", key="export_mcp"):
                edited_mcp.to_csv('data/output/mcp_manual.csv')
                with col_export_mcp2:
                    st.success("MCP exportée dans 'data/output/mcp_manual.csv'")
        
        # Bouton de traitement
        if st.button("🚀 Lancer le traitement", key="process_button"):
            try:
                # Vérification des valeurs pour l'échelle 0-1
                if scale_type == '0-1':
                    if ((edited_mca.values < 0).any() or (edited_mca.values > 1).any() or 
                        (edited_mcp.values < 0).any() or (edited_mcp.values > 1).any()):
                        st.error("""
                        ⚠️ Les données ne sont pas dans l'intervalle [0,1].
                        Pour ces données, utilisez l'option 'free'.
                        """)
                        return
                
                # Configuration du logger
                import logging
                logger = logging.getLogger('streamlit_logger')
                logger.setLevel(logging.INFO)
                
                # Créer un conteneur pour les logs
                log_container = st.empty()
                log_messages = []
                
                # Handler pour les logs
                class StreamlitHandler(logging.Handler):
                    def __init__(self, message_list):
                        super().__init__()
                        self.message_list = message_list
                    
                    def emit(self, record):
                        self.message_list.append(record.getMessage())
                
                logger.handlers = []
                logger.addHandler(StreamlitHandler(log_messages))
                
                # Nettoyer le dossier des figures
                figures_dir = 'data/output/figures'
                os.makedirs(figures_dir, exist_ok=True)
                for f in os.listdir(figures_dir):
                    if f.endswith('.png'):
                        os.remove(os.path.join(figures_dir, f))
                
                # Traitement MCAP
                model_function = getattr(ModelFunctions, f"model_function{selected_model[-1]}")
                processor = McapProcessor(
                    logger=logger,
                    mca_matrix=edited_mca,
                    mcp_matrix=edited_mcp,
                    model_function=model_function,
                    scale_type=scale_type
                )
                
                processor.process()
                
                # Afficher les logs
                if log_messages:
                    with st.expander("📋 Logs de traitement", expanded=False):
                        st.text_area(
                            "Détails du traitement",
                            value="\n".join(log_messages),
                            height=200,
                            disabled=True,
                            key=f"log_display_{time.time_ns()}"
                        )
                
                st.success("Traitement terminé avec succès!")
                
                # Affichage des résultats
                if os.path.exists('data/output/ranking_matrix.csv'):
                    results = pd.read_csv('data/output/ranking_matrix.csv')
                    st.write("Résultats de l'affectation :")
                    st.dataframe(results)
                
                # Affichage des résultats détaillés
                if os.path.exists('data/output/ranking_results.txt'):
                    with open('data/output/ranking_results.txt', 'r') as f:
                        results_text = f.read()
                    
                    with st.expander("📊 Résultats détaillés par activité", expanded=False):
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
                            disabled=True,
                            key=f"results_text_{time.time_ns()}"
                        )
                
                # Affichage des graphiques
                if os.path.exists('data/output/figures'):
                    st.write("## Visualisations des résultats")
                    
                    graph_files = os.listdir('data/output/figures')
                    radar_graphs = sorted([f for f in graph_files if f.startswith('radar_pentagon_')])
                    bar_graphs = sorted([f for f in graph_files if f.startswith('affectation_bar_')])
                    
                    if radar_graphs:
                        with st.expander("📊 Graphiques Radar", expanded=True):
                            for radar_file in radar_graphs:
                                st.image(
                                    f'data/output/figures/{radar_file}',
                                    use_column_width=True
                                )
                    
                    if bar_graphs:
                        with st.expander("📈 Graphiques en barres", expanded=True):
                            for bar_file in bar_graphs:
                                st.image(
                                    f'data/output/figures/{bar_file}',
                                    use_column_width=True
                                )
                
                # Après l'affichage des graphiques
                if os.path.exists('data/output/ranking_matrix.csv'):
                    st.markdown("---")
                    st.subheader("📥 Exporter les résultats")
                    
                    if st.button("📦 Exporter tous les résultats", key="export_all_results"):
                        try:
                            # Créer un dossier pour les exports
                            export_dir = 'data/output/export_manual'
                            os.makedirs(export_dir, exist_ok=True)
                            
                            # Timestamp pour les noms de fichiers
                            timestamp = time.strftime("%Y%m%d-%H%M%S")
                            
                            # Copier les fichiers
                            import shutil
                            
                            # Matrice de résultats
                            shutil.copy2(
                                'data/output/ranking_matrix.csv',
                                f'{export_dir}/resultats_{timestamp}.csv'
                            )
                            
                            # Résultats détaillés
                            if os.path.exists('data/output/ranking_results.txt'):
                                shutil.copy2(
                                    'data/output/ranking_results.txt',
                                    f'{export_dir}/details_{timestamp}.txt'
                                )
                            
                            # Copier les graphiques
                            figures_dir = f'{export_dir}/figures_{timestamp}'
                            os.makedirs(figures_dir, exist_ok=True)
                            
                            for f in os.listdir('data/output/figures'):
                                if f.endswith('.png'):
                                    shutil.copy2(
                                        f'data/output/figures/{f}',
                                        f'{figures_dir}/{f}'
                                    )
                            
                            st.success(f"""
                            ✅ Résultats exportés avec succès dans :
                            - {export_dir}/resultats_{timestamp}.csv
                            - {export_dir}/details_{timestamp}.txt
                            - {export_dir}/figures_{timestamp}/
                            """)
                        except Exception as e:
                            st.error(f"Erreur lors de l'export : {str(e)}")

            except Exception as e:
                st.error(f"Erreur lors du traitement : {str(e)}")

if __name__ == "__main__":
    run_streamlit_app()