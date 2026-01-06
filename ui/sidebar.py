"""
Sidebar Component
Handles file upload, dataset selection, and navigation
"""

import streamlit as st
import pandas as pd
from typing import Optional
from pathlib import Path
import os


def render_sidebar(db_manager) -> dict:
    """
    Render the sidebar with file upload and dataset management
    
    Args:
        db_manager: SQLiteManager instance
        
    Returns:
        Dictionary with selected dataset and other UI state
    """
    st.sidebar.title("🤖 AI Dashboard System")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["📊 Dashboard", "📁 Datasets", "📈 History", "⚙️ Settings"],
        index=0
    )
    
    st.sidebar.markdown("---")
    
    # File Upload Section
    st.sidebar.header("📤 Upload Data")
    
    uploaded_file = st.sidebar.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload your CSV file to get started"
    )
    
    # Dataset management
    st.sidebar.markdown("---")
    st.sidebar.header("📂 Available Datasets")
    
    # Get list of datasets
    datasets = db_manager.list_datasets()
    
    selected_dataset_id = None
    selected_dataset_name = None
    
    if datasets:
        dataset_options = {f"{ds['name']} ({ds['row_count']} rows)": ds['id'] 
                          for ds in datasets}
        
        selected_option = st.sidebar.selectbox(
            "Select Dataset",
            options=["-- Select --"] + list(dataset_options.keys()),
            index=0
        )
        
        if selected_option != "-- Select --":
            selected_dataset_id = dataset_options[selected_option]
            selected_dataset_name = selected_option.split(" (")[0]
            
            # Show dataset info
            dataset_info = db_manager.get_dataset_info(selected_dataset_id)
            if dataset_info:
                with st.sidebar.expander("📋 Dataset Info"):
                    st.write(f"**Rows:** {dataset_info['row_count']}")
                    st.write(f"**Columns:** {dataset_info['column_count']}")
                    st.write(f"**Uploaded:** {dataset_info['upload_date']}")
                    
                    if st.button("🗑️ Delete Dataset", key="delete_btn"):
                        if db_manager.delete_dataset(selected_dataset_id):
                            st.success("Dataset deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete dataset")
    else:
        st.sidebar.info("No datasets available. Upload a CSV file to get started!")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.8em;'>
        Powered by Gemini 2.0 Flash<br>
        Built with ❤️ using Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )
    
    return {
        'page': page,
        'uploaded_file': uploaded_file,
        'selected_dataset_id': selected_dataset_id,
        'selected_dataset_name': selected_dataset_name,
        'datasets': datasets
    }


def process_uploaded_file(uploaded_file, db_manager, orchestrator) -> dict:
    """
    Process an uploaded CSV file
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        db_manager: SQLiteManager instance
        orchestrator: OrchestratorAgent instance
        
    Returns:
        Processing results
    """
    if uploaded_file is None:
        return None
    
    try:
        # Save uploaded file temporarily
        upload_dir = Path("data/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Process the file
        with st.spinner("🔄 Processing your file..."):
            result = orchestrator.process_uploaded_file(str(file_path))
            
            if result['success']:
                # Save to database
                dataset_name = Path(uploaded_file.name).stem
                dataset_id = db_manager.save_dataset(
                    df=result['cleaned_data'],
                    name=dataset_name,
                    original_filename=uploaded_file.name,
                    cleaning_report=result['report']
                )
                
                result['dataset_id'] = dataset_id
                result['dataset_name'] = dataset_name
        
        # Clean up temp file
        if file_path.exists():
            os.remove(file_path)
        
        return result
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return {'success': False, 'error': str(e)}


def show_dataset_statistics(df: pd.DataFrame):
    """
    Display dataset statistics in the sidebar
    
    Args:
        df: Dataframe to analyze
    """
    st.sidebar.markdown("### 📊 Dataset Statistics")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Rows", f"{len(df):,}")
    with col2:
        st.metric("Columns", len(df.columns))
    
    # Column types
    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    st.sidebar.write(f"**Numeric:** {len(numeric_cols)}")
    st.sidebar.write(f"**Categorical:** {len(categorical_cols)}")
    
    # Missing values
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        st.sidebar.warning(f"⚠️ {missing_count} missing values")
    else:
        st.sidebar.success("✅ No missing values")
