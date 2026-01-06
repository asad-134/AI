"""
AI-Powered Dashboard System
Main Streamlit Application
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import Settings
from database.sqlite_manager import SQLiteManager
from agents.orchestrator_agent import OrchestratorAgent
from ui.sidebar import render_sidebar, process_uploaded_file
from ui.dashboard import (
    render_dashboard,
    render_datasets_page,
    render_history_page,
    render_settings_page
)

# Page configuration
st.set_page_config(
    page_title=Settings.APP_NAME,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_app():
    """Initialize application components"""
    # Validate settings
    if not Settings.validate():
        st.error("""
            ⚠️ **Configuration Error**
            
            Google API key not found. Please:
            1. Copy `.env.example` to `.env`
            2. Add your Google API key to the `.env` file
            3. Restart the application
        """)
        st.stop()
    
    # Ensure directories exist
    Settings.ensure_directories()
    
    # Initialize session state
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.db_manager = SQLiteManager(Settings.DATABASE_PATH)
        st.session_state.orchestrator = OrchestratorAgent(
            model_name=Settings.MODEL_NAME,
            temperature=Settings.MODEL_TEMPERATURE
        )
        st.session_state.current_dataset = None
        st.session_state.current_df = None


def main():
    """Main application entry point"""
    
    # Initialize app
    initialize_app()
    
    # Get components from session state
    db_manager = st.session_state.db_manager
    orchestrator = st.session_state.orchestrator
    
    # Render sidebar and get UI state
    sidebar_state = render_sidebar(db_manager)
    
    # Handle file upload
    if sidebar_state['uploaded_file']:
        result = process_uploaded_file(
            sidebar_state['uploaded_file'],
            db_manager,
            orchestrator
        )
        
        if result and result['success']:
            st.success(f"✅ {result['dataset_name']} uploaded successfully!")
            
            # Show cleaning report
            with st.expander("📋 Data Cleaning Report"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Original Rows", result['original_shape'][0])
                    st.metric("Cleaned Rows", result['cleaned_shape'][0])
                
                with col2:
                    st.metric("Rows Removed", result['report']['rows_removed'])
                    st.metric("Columns Removed", result['report']['columns_removed'])
                
                with col3:
                    st.metric("Missing Before", result['report']['missing_values_before'])
                    st.metric("Missing After", result['report']['missing_values_after'])
            
            # Update current dataset
            st.session_state.current_dataset = result['dataset_id']
            st.session_state.current_df = result['cleaned_data']
            
            st.rerun()
    
    # Load selected dataset
    if sidebar_state['selected_dataset_id']:
        if (st.session_state.current_dataset != sidebar_state['selected_dataset_id'] or 
            st.session_state.current_df is None):
            
            df = db_manager.get_dataset(sidebar_state['selected_dataset_id'])
            if df is not None:
                st.session_state.current_dataset = sidebar_state['selected_dataset_id']
                st.session_state.current_df = df
    
    # Route to appropriate page
    page = sidebar_state['page']
    
    if page == "📊 Dashboard":
        render_dashboard(
            st.session_state.current_df,
            orchestrator,
            db_manager,
            st.session_state.current_dataset
        )
    
    elif page == "📁 Datasets":
        render_datasets_page(db_manager)
    
    elif page == "📈 History":
        render_history_page(db_manager)
    
    elif page == "⚙️ Settings":
        render_settings_page()


if __name__ == "__main__":
    main()
