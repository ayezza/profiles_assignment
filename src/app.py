import streamlit as st
import pandas as pd
import os
import logging
from core.mcap_processor import McapProcessor
from models.model_functions import get_model_function
from utils.logger import setup_logger

# Set up logging
logger = setup_logger()

# Clear cache and session state at startup
def clear_session():
    """Clear all session state and cache"""
    # Clear Streamlit cache
    if hasattr(st, 'cache_data'):
        st.cache_data.clear()
    if hasattr(st, 'cache_resource'):
        st.cache_resource.clear()
    
    # Clear all session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def load_data():
    """Load input matrices from CSV files"""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        mca_path = os.path.join(base_dir, 'data', 'input', 'mca.csv')
        mcp_path = os.path.join(base_dir, 'data', 'input', 'mcp.csv')
        
        mca = pd.read_csv(mca_path, index_col=0)
        mcp = pd.read_csv(mcp_path, index_col=0)
        return mca, mcp
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

def main():
    # Force reinitialization with a button
    if st.sidebar.button("Reset Application"):
        clear_session()
        st.rerun()
    
    # Initialize on first run
    if 'initialized' not in st.session_state:
        clear_session()
        st.session_state.initialized = True
        try:
            st.session_state.mca_matrix, st.session_state.mcp_matrix = load_data()
        except Exception as e:
            st.error(f"Error loading initial data: {str(e)}")
            return

    st.title("MCAP Matrix Generator")
    
    try:
        # Create input columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            model_options = {
                'Model 1': 'model1',
                'Model 2': 'model2',
                'Model 3': 'model3',
                'Model 4': 'model4',
                'Model 5': 'model5'
            }
            selected_model = st.selectbox(
                'Select Model Function',
                options=list(model_options.keys()),
                key=f'model_select_{st.session_state.get("counter", 0)}'
            )
            
        with col2:
            mcap_function = st.selectbox(
                'Select MCAP Function',
                options=['sum', 'mean', 'sqrt'],
                key=f'mcap_select_{st.session_state.get("counter", 0)}'
            )
            
        with col3:
            scale_type = st.selectbox(
                'Select Scale Type',
                options=['0-1', 'free'],
                key=f'scale_select_{st.session_state.get("counter", 0)}'
            )

        # Process data automatically when parameters change or button is clicked
        should_process = False
        
        # Check if parameters changed
        current_params = f"{selected_model}_{mcap_function}_{scale_type}"
        if 'last_params' not in st.session_state or st.session_state.last_params != current_params:
            should_process = True
            st.session_state.last_params = current_params

        # Add process button as well
        if st.button('Reprocess Data', type='primary', use_container_width=True):
            should_process = True

        if should_process and hasattr(st.session_state, 'mca_matrix'):
            with st.spinner('Processing data...'):
                processor = McapProcessor(
                    logger=logger,
                    mca_matrix=st.session_state.mca_matrix,
                    mcp_matrix=st.session_state.mcp_matrix,
                    model_function=get_model_function(model_options[selected_model]),
                    mcap_function=mcap_function,
                    scale_type=scale_type,
                    normalize=True,
                    is_web_request=True  # Set to True for web interface
                )
                
                results = processor.process()
                
                # Store results in session state
                st.session_state.mcap_matrix = results['mcap_matrix']  # Updated key name
                st.session_state.ranking_matrix = results['ranking_matrix']
                st.session_state.ranking_results = results['ranking_results']
                st.session_state.counter = st.session_state.get('counter', 0) + 1

        # Always display results if they exist in session state
        if hasattr(st.session_state, 'mcap_matrix'):
            st.subheader("MCAP Matrix")
            st.dataframe(st.session_state.mcap_matrix)
            
            st.subheader("Rankings")
            st.dataframe(st.session_state.ranking_matrix)
            
            st.subheader("Detailed Rankings")
            st.text(st.session_state.ranking_results)
            
            # Display debug info in sidebar
            st.sidebar.write("Debug Info:")
            st.sidebar.write(f"Matrix Shape: {st.session_state.mcap_matrix.shape}")
            st.sidebar.write(f"Current Parameters: {current_params}")
            
            # Display plots if available
            if hasattr(processor, 'figures') and processor.figures:
                st.subheader("Visualizations")
                for name, fig in processor.figures.items():
                    st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Error in Streamlit app: {str(e)}", exc_info=True)
        st.sidebar.error("Debug: Check error in sidebar")
        st.sidebar.write(str(e))

if __name__ == "__main__":
    main()
