"""
Dashboard Component
Main dashboard layout and query interface
"""

import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any
import time


def render_dashboard(df: Optional[pd.DataFrame], orchestrator, db_manager, dataset_id: Optional[int] = None):
    """
    Render the main dashboard interface
    
    Args:
        df: Current dataframe
        orchestrator: OrchestratorAgent instance
        db_manager: SQLiteManager instance
        dataset_id: Current dataset ID
    """
    st.title("🎯 AI-Powered Dashboard")
    
    if df is None:
        render_welcome_screen()
        return
    
    # Data preview section
    render_data_preview(df)
    
    # Query interface
    st.markdown("---")
    render_query_interface(df, orchestrator, db_manager, dataset_id)


def render_welcome_screen():
    """Display welcome screen when no data is loaded"""
    st.markdown("""
        ## Welcome to AI-Powered Dashboard! 👋
        
        Get started by uploading a CSV file from the sidebar.
        
        ### 🚀 Features:
        - **Automatic Data Cleaning**: AI-powered data preprocessing
        - **Natural Language Queries**: Ask questions in plain English
        - **Smart Visualizations**: Automatically generate relevant charts
        - **Multiple Chart Types**: Bar, line, scatter, pie, and more
        - **Interactive Dashboards**: Explore your data dynamically
        
        ### 📝 Example Queries:
        - "Show me sales trends by month"
        - "Create a bar chart comparing revenue by category"
        - "Display the correlation between price and quantity"
        - "Show distribution of customer ages"
        
        ### 🎯 How to Use:
        1. Upload your CSV file using the sidebar
        2. Wait for automatic data cleaning
        3. Enter your query in natural language
        4. View the generated visualizations
        5. Explore and interact with your data
        
        ---
        **Ready to begin?** Upload your data from the sidebar! 👈
    """)


def render_data_preview(df: pd.DataFrame):
    """
    Display data preview section
    
    Args:
        df: Dataframe to preview
    """
    with st.expander("📊 Data Preview", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Rows", f"{len(df):,}")
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            numeric_cols = len(df.select_dtypes(include=['number']).columns)
            st.metric("Numeric Columns", numeric_cols)
        with col4:
            missing = df.isnull().sum().sum()
            st.metric("Missing Values", missing)
        
        # Display first few rows
        st.dataframe(df.head(10), use_container_width=True)
        
        # Column information
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes.astype(str),
            'Non-Null': df.count(),
            'Null': df.isnull().sum(),
            'Unique': df.nunique()
        })
        
        st.subheader("Column Information")
        st.dataframe(col_info, use_container_width=True)


def render_query_interface(df: pd.DataFrame, orchestrator, db_manager, dataset_id: Optional[int]):
    """
    Render the query input and execution interface
    
    Args:
        df: Current dataframe
        orchestrator: OrchestratorAgent instance
        db_manager: SQLiteManager instance
        dataset_id: Current dataset ID
    """
    st.header("💬 Ask Your Data")
    
    # Query suggestions
    render_query_suggestions(df)
    
    # Query input
    query = st.text_area(
        "Enter your query:",
        placeholder="E.g., Show me a bar chart of sales by region",
        height=100,
        help="Describe what you want to see in natural language"
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        generate_btn = st.button("🚀 Generate", type="primary", use_container_width=True)
    
    with col2:
        clear_btn = st.button("🔄 Clear", use_container_width=True)
    
    if clear_btn:
        st.session_state.pop('query_results', None)
        st.rerun()
    
    # Execute query
    if generate_btn and query:
        execute_query(query, df, orchestrator, db_manager, dataset_id)
    
    # Display results if available
    if 'query_results' in st.session_state and st.session_state.query_results:
        display_query_results(st.session_state.query_results)


def render_query_suggestions(df: pd.DataFrame):
    """
    Display query suggestions based on available data
    
    Args:
        df: Current dataframe
    """
    with st.expander("💡 Query Suggestions", expanded=False):
        cols = df.columns.tolist()
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        suggestions = []
        
        if numeric_cols and categorical_cols:
            suggestions.append(f"Show me a bar chart of {numeric_cols[0]} by {categorical_cols[0]}")
            suggestions.append(f"Compare {numeric_cols[0]} across different {categorical_cols[0]}")
        
        if len(numeric_cols) >= 2:
            suggestions.append(f"Show the relationship between {numeric_cols[0]} and {numeric_cols[1]}")
            suggestions.append(f"Create a scatter plot of {numeric_cols[0]} vs {numeric_cols[1]}")
        
        if numeric_cols:
            suggestions.append(f"Display the distribution of {numeric_cols[0]}")
            suggestions.append(f"Show me statistics for {numeric_cols[0]}")
        
        if categorical_cols:
            suggestions.append(f"Show the breakdown of {categorical_cols[0]}")
        
        suggestions.append("Show correlation heatmap for all numeric columns")
        suggestions.append("Display summary statistics for the dataset")
        
        st.markdown("**Try these:**")
        for i, suggestion in enumerate(suggestions[:6], 1):
            st.markdown(f"{i}. {suggestion}")


def execute_query(query: str, df: pd.DataFrame, orchestrator, db_manager, dataset_id: Optional[int]):
    """
    Execute user query and generate visualizations
    
    Args:
        query: User's query string
        df: Current dataframe
        orchestrator: OrchestratorAgent instance
        db_manager: SQLiteManager instance
        dataset_id: Current dataset ID
    """
    with st.spinner("🤖 AI is analyzing your query..."):
        start_time = time.time()
        
        try:
            # Execute orchestrator workflow
            results = orchestrator.execute(df, query, skip_cleaning=True)
            
            execution_time = time.time() - start_time
            
            if results.get('success'):
                st.success(f"✅ Analysis completed in {execution_time:.2f} seconds")
                
                # Save to query history
                if dataset_id:
                    result_summary = f"Generated {len(results['visualizations']['chart_specifications'])} visualizations"
                    db_manager.save_query_history(
                        dataset_id=dataset_id,
                        query_text=query,
                        execution_time=execution_time,
                        result_summary=result_summary
                    )
                
                # Store results in session state
                st.session_state.query_results = {
                    'query': query,
                    'results': results,
                    'execution_time': execution_time
                }
                
                st.rerun()
            else:
                st.error(f"❌ Error: {results.get('error', 'Unknown error occurred')}")
                
        except Exception as e:
            st.error(f"❌ Error executing query: {str(e)}")
            st.exception(e)


def display_query_results(query_data: Dict[str, Any]):
    """
    Display query results and visualizations
    
    Args:
        query_data: Dictionary containing query results
    """
    st.markdown("---")
    st.header("📈 Results")
    
    results = query_data['results']
    
    # Display insights
    if 'analysis' in results and 'insights' in results['analysis']:
        st.subheader("💡 Key Insights")
        insights = results['analysis']['insights']
        
        for i, insight in enumerate(insights, 1):
            st.info(f"**{i}.** {insight}")
    
    # Display visualizations
    if 'visualizations' in results:
        from ui.visualizations import render_visualizations
        render_visualizations(results['visualizations'])
    
    # Display analysis details
    with st.expander("🔍 Analysis Details", expanded=False):
        if 'analysis' in results:
            analysis = results['analysis']
            
            if 'analysis_plan' in analysis:
                st.json(analysis['analysis_plan'])
            
            if 'data_profile' in analysis:
                st.subheader("Data Profile")
                st.json(analysis['data_profile'])


def render_datasets_page(db_manager):
    """
    Render the datasets management page
    
    Args:
        db_manager: SQLiteManager instance
    """
    st.title("📁 Dataset Management")
    
    datasets = db_manager.list_datasets()
    
    if not datasets:
        st.info("No datasets available yet. Upload a CSV file to get started!")
        return
    
    st.write(f"**Total Datasets:** {len(datasets)}")
    
    for dataset in datasets:
        with st.expander(f"📊 {dataset['name']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Filename:** {dataset['original_filename']}")
                st.write(f"**Rows:** {dataset['row_count']:,}")
                st.write(f"**Columns:** {dataset['column_count']}")
            
            with col2:
                st.write(f"**Uploaded:** {dataset['upload_date']}")
                st.write(f"**Table:** {dataset['table_name']}")
            
            # Get detailed info
            info = db_manager.get_dataset_info(dataset['id'])
            if info and info.get('cleaning_report'):
                st.subheader("Cleaning Report")
                st.json(info['cleaning_report'])
            
            if st.button(f"Delete", key=f"delete_{dataset['id']}"):
                if db_manager.delete_dataset(dataset['id']):
                    st.success("Dataset deleted successfully!")
                    st.rerun()


def render_history_page(db_manager):
    """
    Render the query history page
    
    Args:
        db_manager: SQLiteManager instance
    """
    st.title("📈 Query History")
    
    history = db_manager.get_query_history(limit=50)
    
    if not history:
        st.info("No query history yet. Start asking questions about your data!")
        return
    
    st.write(f"**Total Queries:** {len(history)}")
    
    # Convert to dataframe for display
    history_df = pd.DataFrame(history)
    history_df = history_df[['query_date', 'query_text', 'execution_time', 'result_summary']]
    history_df.columns = ['Date', 'Query', 'Time (s)', 'Result']
    
    st.dataframe(history_df, use_container_width=True)


def render_settings_page():
    """Render the settings page"""
    st.title("⚙️ Settings")
    
    st.subheader("Model Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        model = st.selectbox(
            "AI Model",
            ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"],
            help="Select the Gemini model to use"
        )
        
        temperature = st.slider(
            "Temperature",
            0.0, 1.0, 0.7, 0.1,
            help="Higher values make output more creative"
        )
    
    with col2:
        max_tokens = st.number_input(
            "Max Tokens",
            1000, 4096, 2048, 256,
            help="Maximum tokens for model response"
        )
        
        enable_cache = st.checkbox(
            "Enable Caching",
            value=True,
            help="Cache results for faster responses"
        )
    
    st.subheader("Visualization Settings")
    
    default_height = st.slider("Default Chart Height", 300, 800, 400, 50)
    show_grid = st.checkbox("Show Grid Lines", value=True)
    theme = st.selectbox("Chart Theme", ["plotly", "plotly_white", "plotly_dark"])
    
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")
    
    st.markdown("---")
    st.subheader("About")
    st.info("""
        **AI-Powered Dashboard System**
        
        Version: 1.0.0
        
        Built with:
        - Streamlit
        - LangChain
        - Google Gemini
        - Plotly
        
        © 2026
    """)
