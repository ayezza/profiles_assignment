import sys
import os
from io import StringIO  # Add this import

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Configuration de Matplotlib
import matplotlib
matplotlib.use('Agg')  # Utiliser le backend Agg qui est thread-safe
import matplotlib.pyplot as plt
plt.style.use('default')  # Utiliser le style par défaut

# Configuration des polices
matplotlib.rcParams['font.family'] = ['Arial']
matplotlib.rcParams['font.sans-serif'] = ['Arial']
matplotlib.rcParams['font.size'] = 10
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['axes.labelsize'] = 10
matplotlib.rcParams['xtick.labelsize'] = 8
matplotlib.rcParams['ytick.labelsize'] = 8
matplotlib.rcParams['legend.fontsize'] = 8

import streamlit as st
import pandas as pd
from src.core.mcap_processor import McapProcessor
from src.models.model_functions import ModelFunctions
from src.utils.logger import LoggerSetup
import logging
import logging.config
import osfrom io import StringIO
import time

def run_streamlit_app():
    # Configuration du loggerpath.abspath(__file__))))
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_path = os.path.join(root_dir, 'config', 'mylogger.ini')log_file_path = os.path.join(root_dir, 'data', 'output', 'mylog.log')
    log_file_path = os.path.join(root_dir, 'data', 'output', 'mylog.log')
    
    def display_graphs(figures_dir):te"""
        """Fonction pour afficher les graphiques de manière cohérente"""igures_dir) and os.listdir(figures_dir):
        if os.path.exists(figures_dir) and os.listdir(figures_dir):
            st.markdown("""
            <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin: 20px 0;'>2 style='color: #0066cc; margin: 0; font-family: Arial, sans-serif;'>📊 Visualisations des résultats</h2>
                <h2 style='color: #0066cc; margin: 0; font-family: Arial, sans-serif;'>📊 Visualisations des résultats</h2>
            </div>""", unsafe_allow_html=True)
            """, unsafe_allow_html=True)
            
            radar_graphs = sorted([f for f in graph_files if f.startswith('radar_pentagon_')])
            radar_graphs = sorted([f for f in graph_files if f.startswith('radar_pentagon_')])bar_graphs = sorted([f for f in graph_files if f.startswith('affectation_bar_')])
            bar_graphs = sorted([f for f in graph_files if f.startswith('affectation_bar_')])
            graphiques radar
            # Affichage des graphiques radar
            if radar_graphs:sans-serif;'>📊 Graphiques Radar</h3>", unsafe_allow_html=True)
                cols = st.columns(min(len(radar_graphs), 2))s-serif;'>📊 Graphiques Radar</h3>", unsafe_allow_html=True)
                for idx, radar_file in enumerate(radar_graphs):en(radar_graphs), 2))
                for idx, radar_file in enumerate(radar_graphs): % 2]:
                    with cols[idx % 2]:
                        st.image(
                            os.path.join(figures_dir, radar_file),
                            width=None,  # Let Streamlit determine the width   caption=f"Radar - {radar_file.replace('radar_pentagon_', '').replace('.png', '')}"
                            caption=f"Radar - {radar_file.replace('radar_pentagon_', '').replace('.png', '')}"            )
                        )
            s graphiques en barres
            # Affichage des graphiques en barres
            if bar_graphs:, sans-serif;'>📈 Graphiques en barres</h3>", unsafe_allow_html=True)
                cols = st.columns(min(len(bar_graphs), 2)) sans-serif;'>📈 Graphiques en barres</h3>", unsafe_allow_html=True)
                cols = st.columns(min(len(bar_graphs), 2))umerate(bar_graphs):
                for idx, bar_file in enumerate(bar_graphs): % 2]:
                    with cols[idx % 2]:
                        st.image(
                            os.path.join(figures_dir, bar_file),
                            width=None,  # Let Streamlit determine the width   caption=f"Graphique - {bar_file.replace('affectation_bar_', '').replace('.png', '')}"
                            caption=f"Graphique - {bar_file.replace('affectation_bar_', '').replace('.png', '')}"                    )
                        )
    
    try:
        os.makedirs(os.path.join(root_dir, 'data', 'output'), exist_ok=True)up.setup_logger(config_path, 'myLogger', log_file_path)
        logger = LoggerSetup.setup_logger(config_path, 'myLogger', log_file_path):
        if logger is None:
            st.error(f""" la configuration du logger.
            Erreur lors de la configuration du logger.
            Vérifiez que :
            1. Le fichier {config_path} existe
            2. Le dossier data/output est accessible en écrituree fichier {log_file_path} est accessible en écriture
            3. Le fichier {log_file_path} est accessible en écriture
            """)
            return
    except Exception as e:or(f"Erreur inattendue lors de la configuration du logger : {str(e)}")
        st.error(f"Erreur inattendue lors de la configuration du logger : {str(e)}")        return
        return
la page en mode large
    # Configuration de la page en mode large
    st.set_page_config(ectation des Profils",
        page_title="Affectation des Profils",,
        page_icon="📊",
        layout="wide",   initial_sidebar_state="expanded"
        initial_sidebar_state="expanded")
    )
    st.cache_data.clear()
    st.cache_data.clear()
    
    # Titre dans la sidebar
    st.sidebar.markdown("""ffectation des profils aux activités
    # Affectation des profils aux activités
    ---""")
    """)
    
    # Sélecteur de page.radio(
    page = st.sidebar.radio(
        "Navigation",'accueil", "Tester l'application", "Saisie manuelle"],
        ["Page d'accueil", "Tester l'application", "Saisie manuelle"],
        index=0,   key="navigation"
        key="navigation")
    )
    
    if page == "Page d'accueil":
        # Contenu de la page d'accueilst.title("Affectation des Profils")
        st.title("Affectation des Profils")
        mé dans un conteneur avec style
        # Ajout du résumé dans un conteneur avec style
        st.markdown(""" Arial, sans-serif;font-size: 1.1em;color: #333;'>
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 25px; font-family: Arial, sans-serif;font-size: 1.1em;color: #333;'>rgin-bottom: 15px;'>📋 À propos de cette application</h2>
            <h2 style='color: #0066cc; font-size: 1.5em; margin-bottom: 15px;'>📋 À propos de cette application</h2>
            <p style='font-size: 1.1em; line-height: 1.5;'>es profils à des activités en fonction de leurs compétences respectives.
                Cette application permet d'affecter des profils à des activités en fonction de leurs compétences respectives. utilise deux matrices d'entrée :
                Elle utilise deux matrices d'entrée :
                <ul></li>
                    <li><strong>MCA</strong> (Matrice des Compétences requises des Activités) : définit les compétences requises pour chaque activité</li>li><strong>MCP</strong> (Matrice des Compétences acquises des Profils) : définit les compétences acquises par chaque profil</li>
                    <li><strong>MCP</strong> (Matrice des Compétences acquises des Profils) : définit les compétences acquises par chaque profil</li>>
                </ul>
                <br>
                L'application propose 5 modèles différents d'affectation (modèle1, ..., modèle5) et deux types d'échelles de données (0-1, free).<br>Les résultats sont présentés sous forme de classements, graphiques radar et visualisations en barres ainsi que textuellement dans une zone texte dédiée.
                Les résultats sont présentés sous forme de classements, graphiques radar et visualisations en barres ainsi que textuellement dans une zone texte dédiée.p>
            </p>
        </div>""", unsafe_allow_html=True)
        """, unsafe_allow_html=True)
        
        # Ajout de l'exemple concretst.header("💡 Exemple concret", divider="orange")
        st.header("💡 Exemple concret", divider="orange")
        s pour MCA et MCP
        # Création de deux colonnes pour MCA et MCPcol1, col2 = st.columns(2)
        col1, col2 = st.columns(2)
        
        with col1:és)")
            st.subheader("MCA (2 Activités)")me({
            mca_example = pd.DataFrame({
                'Comp1': [0.8, 0.5],,
                'Comp2': [0.6, 0.9],
                'Comp3': [0.4, 0.7]
            }, index=['Act1', 'Act2'])    st.dataframe(mca_example, use_container_width=True)
            st.dataframe(mca_example, use_container_width=True)
        
        with col2:)")
            st.subheader("MCP (2 Profils)")me({
            mcp_example = pd.DataFrame({
                'Comp1': [0.9, 0.7],,
                'Comp2': [0.5, 0.8],
                'Comp3': [0.3, 0.6]
            }, index=['Prof1', 'Prof2'])    st.dataframe(mcp_example, use_container_width=True)
            st.dataframe(mcp_example, use_container_width=True)
        
        # Description et résultats pour chaque modèlest.subheader("Application des différents modèles")
        st.subheader("Application des différents modèles")
        
        # Modèle 1 (max)ax(profile_value, activity_value)")
        st.markdown("#### Modèle 1 : max(profile_value, activity_value)")me({
        result_model1 = pd.DataFrame({,
            'Prof1': [0.95, 0.92],
            'Prof2': [0.89, 0.94]
        }, index=['Act1', 'Act2'])
        st.dataframe(result_model1, use_container_width=True)st.caption("→ Act1: Profil 1 meilleur (0.95), Act2: Profil 2 meilleur (0.94)")
        st.caption("→ Act1: Profil 1 meilleur (0.95), Act2: Profil 2 meilleur (0.94)")
        
        # Modèle 2 (différence conditionnelle)rofile_value si ≥ activity_value, sinon différence")
        st.markdown("#### Modèle 2 : profile_value si ≥ activity_value, sinon différence")me({
        result_model2 = pd.DataFrame({,
            'Prof1': [0.88, 0.75],
            'Prof2': [0.82, 0.90]
        }, index=['Act1', 'Act2'])
        st.dataframe(result_model2, use_container_width=True)st.caption("→ Act1: Profil 1 meilleur (0.88), Act2: Profil 2 meilleur (0.90)")
        st.caption("→ Act1: Profil 1 meilleur (0.88), Act2: Profil 2 meilleur (0.90)")
        
        # Modèle 3 (différence simple)rofile_value - activity_value")
        st.markdown("#### Modèle 3 : profile_value - activity_value")me({
        result_model3 = pd.DataFrame({,
            'Prof1': [0.15, 0.10],
            'Prof2': [0.20, 0.25]
        }, index=['Act1', 'Act2'])
        st.dataframe(result_model3, use_container_width=True)st.caption("→ Act1: Profil 2 meilleur (0.20), Act2: Profil 2 meilleur (0.25)")
        st.caption("→ Act1: Profil 2 meilleur (0.20), Act2: Profil 2 meilleur (0.25)")
        
        # Modèle 4 (distance euclidienne)qrt(profile_value² + activity_value²)")
        st.markdown("#### Modèle 4 : sqrt(profile_value² + activity_value²)")me({
        result_model4 = pd.DataFrame({,
            'Prof1': [1.15, 1.20],
            'Prof2': [1.10, 1.30]
        }, index=['Act1', 'Act2'])
        st.dataframe(result_model4, use_container_width=True)st.caption("→ Act1: Profil 1 meilleur (1.15), Act2: Profil 2 meilleur (1.30)")
        st.caption("→ Act1: Profil 1 meilleur (1.15), Act2: Profil 2 meilleur (1.30)")
        
        # Modèle 5 (moyenne pondérée)oyenne pondérée (0.7 × MCP + 0.3 × MCA)")
        st.markdown("#### Modèle 5 : moyenne pondérée (0.7 × MCP + 0.3 × MCA)")me({
        result_model5 = pd.DataFrame({,
            'Prof1': [0.85, 0.78],
            'Prof2': [0.92, 0.95]
        }, index=['Act1', 'Act2'])
        st.dataframe(result_model5, use_container_width=True)st.caption("→ Act1: Profil 2 meilleur (0.92), Act2: Profil 2 meilleur (0.95)")
        st.caption("→ Act1: Profil 2 meilleur (0.92), Act2: Profil 2 meilleur (0.95)")
        
    elif page == "Tester l'application":st.title("Traitement des données")
        st.title("Traitement des données")
        
        # Configurationst.sidebar.header("Configuration")
        st.sidebar.header("Configuration")
        
        # Upload des fichiers
        mca_file = st.sidebar.file_uploader("Charger le fichier MCA", type=['csv'])mcp_file = st.sidebar.file_uploader("Charger le fichier MCP", type=['csv'])
        mcp_file = st.sidebar.file_uploader("Charger le fichier MCP", type=['csv'])
        dèle
        # Sélection du modèle
        model_options = {
            'Modèle 1': 'model1',
            'Modèle 2': 'model2',
            'Modèle 3': 'model3',,
            'Modèle 4': 'model4',   'Modèle 5': 'model5'
            'Modèle 5': 'model5'
        }bar.selectbox(
        selected_model = st.sidebar.selectbox(
            "Choisir le modèle",   options=list(model_options.keys())
            options=list(model_options.keys()))
        )
        chelle
        # Sélection du type d'échellen("""
        st.sidebar.markdown("""
        ### Type d'échelle 0 et 1
        - **0-1** : Les données doivent déjà être normalisées entre 0 et 1free** : Les données seront automatiquement normalisées
        - **free** : Les données seront automatiquement normalisées""")
        """)
        ar.selectbox(
        scale_type = st.sidebar.selectbox(
            "Type d'échelle",
            options=['free', '0-1'],
            index=0,  # Sélectionner 'free' par défaut   help="Choisissez 'free' si vos données ne sont pas déjà normalisées"
            help="Choisissez 'free' si vos données ne sont pas déjà normalisées")
        )
        n MCAP
        # Sélection de la fonction MCAPns = {
        mcap_function_options = {
            'Somme': 'sum',
            'Moyenne': 'mean',   'Racine carrée': 'sqrt'
            'Racine carrée': 'sqrt'
        }ebar.selectbox(
        selected_mcap_function = st.sidebar.selectbox(
            "Choisir la fonction MCAP",   options=list(mcap_function_options.keys())
            options=list(mcap_function_options.keys()))
        )
        ile and mcp_file:
        if mca_file and mcp_file:
            try:de paramètres
                # Lecture des fichiers avec plus de paramètres
                mca_data = pd.read_csv(mca_file, =0,
                                     index_col=0,
                                     sep=None,on',
                                     engine='python',',
                                     decimal=',',
                                     dtype=str)
                mcp_data = pd.read_csv(mcp_file,=0,
                                     index_col=0,
                                     sep=None,on',
                                     engine='python',',
                                     decimal=',',                     dtype=str)
                                     dtype=str)
                
                # Vérifier le minimum de 3 lignese[0] < 3 or mcp_data.shape[0] < 3:
                if mca_data.shape[0] < 3 or mcp_data.shape[0] < 3:
                    st.error("""doivent avoir au moins 3 lignes chacune.
                    ⚠️ Les matrices doivent avoir au moins 3 lignes chacune.
                    - MCA: {} lignes
                    - MCP: {} lignesrmat(mca_data.shape[0], mcp_data.shape[0]))
                    """.format(mca_data.shape[0], mcp_data.shape[0]))    return
                    return
                e
                # Conversion propre en numériqueata]:
                for df in [mca_data, mcp_data]:
                    for col in df.columns:
                        df[col] = (df[col]
                                 .str.strip()
                                 .str.replace(',', '.')
                                 .str.replace(' ', ''))        df[col] = pd.to_numeric(df[col], errors='coerce')
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                e des valeurs pour l'échelle 0-1
                # Vérification préalable des valeurs pour l'échelle 0-1
                if scale_type == '0-1':r 
                    if ((mca_data.values < 0).any() or (mca_data.values > 1).any() or lues < 0).any() or (mcp_data.values > 1).any()):
                        (mcp_data.values < 0).any() or (mcp_data.values > 1).any()):
                        st.error("""
                        ⚠️ Les données ne sont pas dans l'intervalle [0,1]. ces données, utilisez l'option 'free' qui normalisera automatiquement les valeurs.
                        Pour ces données, utilisez l'option 'free' qui normalisera automatiquement les valeurs.
                        """)        return
                        return
                es plages de valeurs
                # Afficher les plages de valeurs
                st.info(f"""
                Plages de valeurs actuelles :
                - MCA : [{mca_data.values.min():.2f}, {mca_data.values.max():.2f}]P : [{mcp_data.values.min():.2f}, {mcp_data.values.max():.2f}]
                - MCP : [{mcp_data.values.min():.2f}, {mcp_data.values.max():.2f}]""")
                """)
                éussi
                # Vérifier si la conversion a réussi
                if mca_data.isna().any().any():
                    st.warning("Certaines valeurs dans MCA ont été converties en NaN. Vérifiez vos données.")    st.write("Colonnes avec des NaN dans MCA:", mca_data.columns[mca_data.isna().any()].tolist())
                    st.write("Colonnes avec des NaN dans MCA:", mca_data.columns[mca_data.isna().any()].tolist())
                
                if mcp_data.isna().any().any():
                    st.warning("Certaines valeurs dans MCP ont été converties en NaN. Vérifiez vos données.")te("Colonnes avec des NaN dans MCP:", mcp_data.columns[mcp_data.isna().any()].tolist())
                    st.write("Colonnes avec des NaN dans MCP:", mcp_data.columns[mcp_data.isna().any()].tolist())    return
                    return
                les logs Streamlit
                # Créer un conteneur pour les logs Streamlitt.empty()
                log_container = st.empty()log_messages = []
                log_messages = []
                
                # Handler pour les logs Streamlitr):
                class StreamlitHandler(logging.Handler):sage_list):
                    def __init__(self, message_list):
                        super().__init__()    self.message_list = message_list
                        self.message_list = message_list
                    
                    def emit(self, record):        self.message_list.append(record.getMessage())
                        self.message_list.append(record.getMessage())
                
                # Ajouter le handler Streamlit au logger existant(log_messages)
                streamlit_handler = StreamlitHandler(log_messages)logger.addHandler(streamlit_handler)
                logger.addHandler(streamlit_handler)
                
                # Nettoyer le dossier des figuresata', 'output', 'figures')
                figures_dir = os.path.join(root_dir, 'data', 'output', 'figures')=True)
                os.makedirs(figures_dir, exist_ok=True)s_dir):
                for f in os.listdir(figures_dir):
                    if f.endswith('.png'):        os.remove(os.path.join(figures_dir, f))
                        os.remove(os.path.join(figures_dir, f))
                
                # Traitement MCAPtions.get_model_function(model_options[selected_model])
                model_function = ModelFunctions.get_model_function(model_options[selected_model])ocessor(
                processor = McapProcessor(
                    logger=logger,
                    mca_matrix=mca_data,
                    mcp_matrix=mcp_data,
                    model_function=model_function,nction_options[selected_mcap_function],
                    mcap_function=mcap_function_options[selected_mcap_function],   scale_type=scale_type
                    scale_type=scale_type)
                )
                processor.process()
                processor.process()
                ogs après le traitement
                # Afficher les logs après le traitement
                if log_messages:"📋 Logs de traitement", expanded=False):
                    with st.expander("📋 Logs de traitement", expanded=False):
                        st.text_area(
                            "Détails du traitement",join(log_messages),
                            value="\n".join(log_messages),
                            height=200,
                            disabled=True,   key=f"log_display_{time.time_ns()}"
                            key=f"log_display_{time.time_ns()}"        )
                        )
                st.success("Traitement terminé avec succès!")
                st.success("Traitement terminé avec succès!")
                
                # Affichage des résultats dans la page principale.csv')
                ranking_matrix_path = os.path.join(root_dir, 'data', 'output', 'ranking_matrix.csv')mcap_matrix_path = os.path.join(root_dir, 'data', 'output', 'mcap_matrix.txt')
                mcap_matrix_path = os.path.join(root_dir, 'data', 'output', 'mcap_matrix.txt')
                ces
                # Create columns for matricescol1, col2 = st.columns(2)
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("TOP 3 par Activité")path):
                    if os.path.exists(ranking_matrix_path):
                        # Force fresh read of resultsrix_path, index_col=None)
                        results = pd.read_csv(ranking_matrix_path, index_col=None)
                        if 'Activity' in results.columns:et_index('Activity', inplace=True)
                            results.set_index('Activity', inplace=True)
                        st.dataframe(t(None)  # Prevent auto-formatting
                            results.style.format(None)  # Prevent auto-formatting
                            .set_properties(**{wrap',
                                'white-space': 'pre-wrap', 'text-align': 'left'
                                'text-align': 'left'
                            }),   use_container_width=True
                            use_container_width=True)
                        )
                        
                        # Display parameters useding='utf-8') as f:
                        with open(mcap_matrix_path, 'r', encoding='utf-8') as f:p()
                            params_line = f.readline().strip()
                                st.caption(f"Parameters used: {params_line[2:]}")
                
                with col2:
                    st.subheader("Matrice MCAP (Activités x Profils)")
                    if os.path.exists(mcap_matrix_path):
                        try:
                            # Try different methods to read the file
                            try:
                                # First attempt - standard reading
                                mcap_matrix = pd.read_csv(mcap_matrix_path, index_col=0)
                                if mcap_matrix.empty:
                                    raise ValueError("Empty matrix")
                            except Exception:
                                # Second attempt - explicit parameters
                                mcap_matrix = pd.read_csv(
                                    mcap_matrix_path,
                                    index_col=0,
                                    sep=',',
                                    encoding='utf-8',
                                    decimal='.'
                                )
                            
                            # Check if matrix loaded correctly
                            if mcap_matrix.empty:
                                st.error("La matrice MCAP est vide!")
                                with st.expander("Afficher les détails de débogage"):
                                    st.write("Contenu brut du fichier:")
                                    with open(mcap_matrix_path, 'r', encoding='utf-8') as f:
                                        content = f.read()
                                    st.code(content)
                                    
                                    try:
                                        # Try to parse and display as DataFrame
                                        df = pd.read_csv(
                                            StringIO(content), 
                                            index_col=0,
                                            sep=None,  # Let pandas detect the separator
                                            engine='python'
                                        )
                                        st.write("Parsed content as DataFrame:")
                                        st.write(df)
                                    except Exception as e:
                                        st.write(f"Could not parse as DataFrame: {str(e)}")
                            else:
                                # Round values for display
                                mcap_matrix = mcap_matrix.round(3)
                                
                                # Display matrix with formatting
                                st.dataframe(
                                    mcap_matrix.style.format("{:.3f}").highlight_max(axis=1),
                                    use_container_width=True
                                )
                                
                                st.caption(f"Dimensions de la matrice: {mcap_matrix.shape}")
                            
                        except Exception as e:
                            st.error(f"Erreur lors de la lecture de la matrice MCAP: {str(e)}")
                            with st.expander("Détails de l'erreur"):
                                st.write("Chemin du fichier:", mcap_matrix_path)
                                st.write("Le fichier existe:", os.path.exists(mcap_matrix_path))
                                try:
                                    with open(mcap_matrix_path, 'r', encoding='utf-8') as f:
                                        st.code(f.read())
                                except Exception as e2:
                                    st.write("Impossible de lire le contenu:", str(e2))
                    else:
                        st.warning("Fichier de la matrice MCAP non trouvé")
                
                # Affichage des résultats détaillés
                ranking_results_path = os.path.join(root_dir, 'data', 'output', 'ranking_results.txt')
                if os.path.exists(ranking_results_path):
                    try:
                        try:
                            with open(ranking_results_path, 'r', encoding='utf-8') as f:
                                results_text = f.read()
                        except UnicodeDecodeError:
                            with open(ranking_results_path, 'r', encoding='cp1252') as f:
                                results_text = f.read()
                    
                        with st.expander("📊 Résultats détaillés par activité", expanded=False):
                            st.markdown(
                                """
                                <div style='background-color: #0066cc; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                                    <h3 style='color: white; margin: 0; font-family: Arial, sans-serif;'>Classement détaillé des profils</h3>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            st.text_area(
                                "",
                                value=results_text,
                                height=200,
                                disabled=True,
                                key=f"results_text_{time.time_ns()}"
                            )
                    except Exception as e:
                        st.error(f"Erreur lors de la lecture du fichier de résultats : {str(e)}")
                
                # Affichage des graphiques
                figures_dir = os.path.join(root_dir, 'data', 'output', 'figures')
                display_graphs(figures_dir)
                
                # Après l'affichage des graphiques
                if os.path.exists(ranking_matrix_path):
                    st.markdown("---")
                    st.subheader("📥 Exporter les résultats")
                    
                    if st.button("📦 Exporter tous les résultats", key="export_all_results"):
                        try:
                            # Créer un dossier pour les exports
                            export_dir = os.path.join(root_dir, 'data', 'output', 'export_manual')
                            os.makedirs(export_dir, exist_ok=True)
                            
                            # Timestamp pour les noms de fichiers
                            timestamp = time.strftime("%Y%m%d-%H%M%S")
                            
                            # Copier les fichiers
                            import shutil
                            
                            # Matrice de résultats
                            shutil.copy2(
                                ranking_matrix_path,
                                os.path.join(export_dir, f'resultats_{timestamp}.csv')
                            )
                            
                            # Résultats détaillés
                            if os.path.exists(ranking_results_path):
                                shutil.copy2(
                                    ranking_results_path,
                                    os.path.join(export_dir, f'details_{timestamp}.txt')
                                )
                            
                            # Copier les graphiques
                            figures_export_dir = os.path.join(export_dir, f'figures_{timestamp}')
                            os.makedirs(figures_export_dir, exist_ok=True)
                            
                            for f in os.listdir(figures_dir):
                                if f.endswith('.png'):
                                    shutil.copy2(
                                        os.path.join(figures_dir, f),
                                        os.path.join(figures_export_dir, f)
                                    )
                            
                            st.success(f"""
                            ✅ Résultats exportés avec succès dans :
                            - {os.path.join(export_dir, f'resultats_{timestamp}.csv')}
                            - {os.path.join(export_dir, f'details_{timestamp}.txt')}
                            - {figures_export_dir}/
                            """)
                        except Exception as e:
                            st.error(f"Erreur lors de l'export : {str(e)}")

            except Exception as e:
                st.error("Une erreur s'est produite pendant le traitement")
                st.error(f"Détails de l'erreur : {str(e)}")
                import traceback
                st.error(f"Traceback complet :")
                st.code(traceback.format_exc())
                return

    else:  # page == "Saisie manuelle"
        st.title("Saisie manuelle des données")
        
        # Configuration des dimensions
        col1, col2 = st.columns(2)
        with col1:
            n_activities = st.number_input(
                "Nombre d'activités",
                min_value=3,  # Forcer minimum 3
                max_value=10,
                value=3
            )
            n_competencies = st.number_input(
                "Nombre de compétences",
                min_value=1,
                max_value=10,
                value=3
            )
        with col2:
            n_profiles = st.number_input(
                "Nombre de profils",
                min_value=3,  # Forcer minimum 3
                max_value=10,
                value=3
            )
        
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
        
        # Sélection de la fonction MCAP
        mcap_function_options = {
            'Somme': 'sum',
            'Moyenne': 'mean',
            'Racine carrée': 'sqrt'
        }
        selected_mcap_function = st.sidebar.selectbox(
            "Choisir la fonction MCAP",
            options=list(mcap_function_options.keys())
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
        
        st.write(f"Dimensions de la matrice MCA : {edited_mca.shape}")
        st.write(f"Dimensions de la matrice MCP : {edited_mcp.shape}")
        
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
                
                # Créer un conteneur pour les logs Streamlit
                log_container = st.empty()
                log_messages = []
                
                # Handler pour les logs Streamlit
                class StreamlitHandler(logging.Handler):
                    def __init__(self, message_list):
                        super().__init__()
                        self.message_list = message_list
                    
                    def emit(self, record):
                        self.message_list.append(record.getMessage())
                
                # Ajouter le handler Streamlit au logger existant
                streamlit_handler = StreamlitHandler(log_messages)
                logger.addHandler(streamlit_handler)
                
                # Nettoyer le dossier des figures
                figures_dir = os.path.join(root_dir, 'data', 'output', 'figures')
                os.makedirs(figures_dir, exist_ok=True)
                for f in os.listdir(figures_dir):
                    if f.endswith('.png'):
                        os.remove(os.path.join(figures_dir, f))
                
                # Traitement MCAP
                model_function = ModelFunctions.get_model_function(model_options[selected_model])
                processor = McapProcessor(
                    logger=logger,
                    mca_matrix=edited_mca,
                    mcp_matrix=edited_mcp,
                    model_function=model_function,
                    mcap_function = mcap_function_options[selected_mcap_function],
                    scale_type=scale_type
                )
                st.write("Traitement en cours...")
                #st.write("model_function:", model_function)
                #st.write("scale_type:", scale_type)
                #st.write("mcap_function:", mcap_function_options[selected_mcap_function])
                
                
                
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
                ranking_matrix_path = os.path.join(root_dir, 'data', 'output', 'ranking_matrix.csv')
                if os.path.exists(ranking_matrix_path):
                    results = pd.read_csv(ranking_matrix_path)
                    st.write("Résultats de l'affectation :")
                    st.dataframe(results)
                
                # Affichage des résultats détaillés
                ranking_results_path = os.path.join(root_dir, 'data', 'output', 'ranking_results.txt')
                if os.path.exists(ranking_results_path):
                    try:
                        try:
                            with open(ranking_results_path, 'r', encoding='utf-8') as f:
                                results_text = f.read()
                        except UnicodeDecodeError:
                            with open(ranking_results_path, 'r', encoding='cp1252') as f:
                                results_text = f.read()
                    
                        with st.expander("📊 Résultats détaillés par activité", expanded=False):
                            st.markdown(
                                """
                                <div style='background-color: #0066cc; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                                    <h3 style='color: white; margin: 0; font-family: Arial, sans-serif;'>Classement détaillé des profils</h3>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            st.text_area(
                                "",
                                value=results_text,
                                height=200,
                                disabled=True,
                                key=f"results_text_{time.time_ns()}"
                            )
                    except Exception as e:
                        st.error(f"Erreur lors de la lecture du fichier de résultats : {str(e)}")
                
                # Affichage des graphiques
                figures_dir = os.path.join(root_dir, 'data', 'output', 'figures')
                display_graphs(figures_dir)
                
                # Après l'affichage des graphiques
                if os.path.exists(ranking_matrix_path):
                    st.markdown("---")
                    st.subheader("📥 Exporter les résultats")
                    
                    if st.button("📦 Exporter tous les résultats", key="export_all_results"):
                        try:
                            # Créer un dossier pour les exports
                            export_dir = os.path.join(root_dir, 'data', 'output', 'export_manual')
                            os.makedirs(export_dir, exist_ok=True)
                            
                            # Timestamp pour les noms de fichiers
                            timestamp = time.strftime("%Y%m%d-%H%M%S")
                            
                            # Copier les fichiers
                            import shutil
                            
                            # Matrice de résultats
                            shutil.copy2(
                                ranking_matrix_path,
                                os.path.join(export_dir, f'resultats_{timestamp}.csv')
                            )
                            
                            # Résultats détaillés
                            if os.path.exists(ranking_results_path):
                                shutil.copy2(
                                    ranking_results_path,
                                    os.path.join(export_dir, f'details_{timestamp}.txt')
                                )
                            
                            # Copier les graphiques
                            figures_export_dir = os.path.join(export_dir, f'figures_{timestamp}')
                            os.makedirs(figures_export_dir, exist_ok=True)
                            
                            for f in os.listdir(figures_dir):
                                if f.endswith('.png'):
                                    shutil.copy2(
                                        os.path.join(figures_dir, f),
                                        os.path.join(figures_export_dir, f)
                                    )
                            
                            st.success(f"""
                            ✅ Résultats exportés avec succès dans :
                            - {os.path.join(export_dir, f'resultats_{timestamp}.csv')}
                            - {os.path.join(export_dir, f'details_{timestamp}.txt')}
                            - {figures_export_dir}/
                            """)
                        except Exception as e:
                            st.error(f"Erreur lors de l'export : {str(e)}")

            except Exception as e:
                st.error(f"Erreur lors du traitement : {str(e)}")

if __name__ == "__main__":
    run_streamlit_app()