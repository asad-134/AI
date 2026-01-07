"""
Multi-Agent Dashboard - Streamlit Application
Interactive analytics dashboard powered by Ollama Mistral 7B
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Import custom modules
from data_architect import DataArchitect, clean_customer_data
from visualization_agent import VisualizationAgent
from agent_coordinator import AgentCoordinator
import dashboard_templates as templates

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #145a8d;
    }
    .chart-container {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize all session state variables"""
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    
    if 'df_clean' not in st.session_state:
        st.session_state.df_clean = None
    
    if 'history_charts' not in st.session_state:
        st.session_state.history_charts = []
    
    if 'cleaning_report' not in st.session_state:
        st.session_state.cleaning_report = ""
    
    if 'coordinator' not in st.session_state:
        st.session_state.coordinator = AgentCoordinator()
    
    if 'viz_agent' not in st.session_state:
        st.session_state.viz_agent = VisualizationAgent()


def load_and_clean_data(uploaded_file):
    """Load and clean the dataset using Data Architect"""
    try:
        # Load data
        df = pd.read_csv(uploaded_file)
        
        # Clean data using Data Architect
        with st.spinner("🔧 Data Architect is cleaning your data..."):
            architect = DataArchitect()
            df_clean = architect.clean_data(df)
            report = architect.get_cleaning_report()
        
        # Store in session state
        st.session_state.df_clean = df_clean
        st.session_state.cleaning_report = report
        st.session_state.data_loaded = True
        
        return df_clean, report
    
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None, None


def render_sidebar():
    """Render the sidebar with controls and information"""
    with st.sidebar:
        st.markdown("## 🎛️ Dashboard Controls")
        
        # Model status
        with st.expander("🤖 AI Model Status", expanded=True):
            status = st.session_state.coordinator.get_model_status()
            
            if status['llm_available']:
                st.success("✅ OpenRouter Connected")
                st.info(f"**Model:** {status['model_name']}")
                
                if status.get('api_configured'):
                    st.caption("✓ API key configured")
                else:
                    st.warning("⚠️ API key not found - set OPENROUTER_API_KEY")
            else:
                st.warning("⚠️ OpenRouter Not Available")
                st.info(f"Using fallback: {status['fallback_mode']}")
        
        # Data information
        if st.session_state.data_loaded:
            with st.expander("📊 Dataset Info", expanded=False):
                df = st.session_state.df_clean
                st.metric("Total Rows", len(df))
                st.metric("Total Columns", len(df.columns))
                st.metric("Missing Values", df.isnull().sum().sum())
                
                if st.button("View Cleaning Report"):
                    st.text_area("Cleaning Report", 
                               st.session_state.cleaning_report,
                               height=200)
        
        # Quick actions
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🗑️ Clear All Charts"):
            st.session_state.history_charts = []
            st.rerun()
        
        if st.button("💾 Download Clean Data"):
            if st.session_state.df_clean is not None:
                csv = st.session_state.df_clean.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name="cleaned_data.csv",
                    mime="text/csv"
                )
        
        # Dashboard templates
        st.markdown("---")
        st.markdown("### 📋 Pre-built Dashboards")
        
        dashboard_names = templates.get_all_dashboard_names()
        for dashboard_name in dashboard_names:
            if st.button(f"📊 {dashboard_name}", key=f"dash_{dashboard_name}"):
                load_dashboard_prompts(dashboard_name)


def load_dashboard_prompts(dashboard_name: str):
    """Load all prompts from a pre-built dashboard"""
    prompts = templates.get_prompts_for_dashboard(dashboard_name)
    
    if not prompts or st.session_state.df_clean is None:
        st.warning("Please load data first!")
        return
    
    with st.spinner(f"Loading {dashboard_name}..."):
        for prompt_config in prompts:
            prompt = prompt_config['prompt']
            
            # Generate visualization
            code, method = st.session_state.coordinator.generate_visualization_code(
                prompt, st.session_state.df_clean
            )
            
            if code:
                fig = st.session_state.viz_agent.execute_visualization_code(
                    code, st.session_state.df_clean
                )
                
                if fig:
                    # Add to history
                    st.session_state.history_charts.append({
                        'title': prompt_config['title'],
                        'fig': fig,
                        'prompt': prompt
                    })
    
    st.rerun()


def render_main_content():
    """Render the main content area"""
    
    # Header
    st.markdown('<div class="main-header">🤖 Multi-Agent Analytics Dashboard</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Powered by OpenRouter Gemma3 27B | Context-Task-Formatting Framework</div>', 
                unsafe_allow_html=True)
    
    # Data upload section
    if not st.session_state.data_loaded:
        st.markdown("---")
        st.markdown("### 📂 Upload Your Dataset")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            uploaded_file = st.file_uploader(
                "Upload CSV file",
                type=['csv'],
                help="Upload your customer data CSV file"
            )
            
            if uploaded_file is not None:
                df_clean, report = load_and_clean_data(uploaded_file)
                
                if df_clean is not None:
                    st.success("✅ Data loaded and cleaned successfully!")
                    
                    with st.expander("View Cleaning Report", expanded=True):
                        st.text(report)
                    
                    st.rerun()
            
            # Option to use default dataset
            st.markdown("---")
            if st.button("📊 Use Default Dataset (ifood_df.csv)"):
                default_path = Path("ifood_df.csv")
                if default_path.exists():
                    df_clean, report = load_and_clean_data(default_path)
                    if df_clean is not None:
                        st.success("✅ Default dataset loaded!")
                        st.rerun()
                else:
                    st.error("Default dataset not found!")
    
    else:
        # Main dashboard interface
        render_dashboard_interface()


def render_dashboard_interface():
    """Render the main dashboard with visualization interface"""
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["🎨 Create Visualization", "📊 Dashboard Gallery", "🔍 Data Analysis"])
    
    with tab1:
        render_visualization_creator()
    
    with tab2:
        render_chart_gallery()
    
    with tab3:
        render_data_analysis()


def render_visualization_creator():
    """Interactive visualization creator"""
    st.markdown("### 💬 Ask the AI to Create Visualizations")
    
    # Example prompts
    with st.expander("💡 Example Prompts", expanded=False):
        st.markdown("""
        **KPI Cards:**
        - "Calculate the conversion rate using the Response column"
        - "Show me the average income as a KPI"
        
        **Bar Charts:**
        - "Compare average MntTotal across education levels"
        - "Show campaign acceptance by marital status"
        
        **Scatter Plots:**
        - "Plot Income vs MntTotal colored by education"
        - "Show relationship between Age and spending"
        
        **Heatmaps:**
        - "Correlation heatmap of all spending columns"
        - "Show correlations between Income, Recency, and spending"
        
        **Treemaps:**
        - "MntTotal distribution by marital status"
        - "Revenue breakdown by education level"
        """)
    
    # User input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_prompt = st.text_input(
            "Enter your visualization request:",
            placeholder="e.g., Show me a scatter plot of Income vs MntTotal colored by education level",
            key="viz_prompt"
        )
    
    with col2:
        use_llm = st.checkbox("Use AI", value=True, 
                                help="Use OpenRouter for enhanced generation")
    
    if st.button("🎨 Generate Visualization", type="primary"):
        if user_prompt:
            generate_and_display_chart(user_prompt, use_llm)
        else:
            st.warning("Please enter a visualization request!")
    
    # Quick visualization buttons
    st.markdown("---")
    st.markdown("#### ⚡ Quick Visualizations")
    
    quick_viz_cols = st.columns(4)
    
    quick_prompts = [
        ("📊 Spending Overview", "Compare average spending across all Mnt categories"),
        ("👥 Demographics", "Show Age vs Income scatter plot"),
        ("🎯 Campaign Success", "Bar chart of campaign acceptance rates"),
        ("🔗 Correlations", "Heatmap of Income, Recency, MntWines, MntTotal")
    ]
    
    for idx, (label, prompt) in enumerate(quick_prompts):
        with quick_viz_cols[idx]:
            if st.button(label, key=f"quick_{idx}"):
                generate_and_display_chart(prompt, use_llm)


def generate_and_display_chart(prompt: str, use_llm: bool = True):
    """Generate and display chart from prompt"""
    with st.spinner('🎨 Creating visualization...'):
        try:
            # Generate code
            code, method = st.session_state.coordinator.generate_visualization_code(
                prompt, st.session_state.df_clean, use_llm
            )
            
            if code:
                # Execute code to create figure
                fig = st.session_state.viz_agent.execute_visualization_code(
                    code, st.session_state.df_clean
                )
                
                if fig:
                    # Add to history
                    st.session_state.history_charts.append({
                        'title': prompt,
                        'fig': fig,
                        'prompt': prompt,
                        'method': method
                    })
                    
                    st.success(f"✅ Visualization created using: {method}")
                    st.rerun()
                else:
                    st.error("❌ Failed to create visualization. The generated code didn't produce a valid figure.")
                    with st.expander("Debug: View Generated Code"):
                        st.code(code, language="python")
            else:
                st.error("❌ Failed to generate visualization code. Try rephrasing your prompt.")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            import traceback
            with st.expander("Debug: View Error Details"):
                st.code(traceback.format_exc())


def render_chart_gallery():
    """Render all saved charts in a gallery layout"""
    
    if not st.session_state.history_charts:
        st.info("📭 No visualizations yet. Create your first visualization in the 'Create Visualization' tab!")
        return
    
    st.markdown(f"### 📊 Visualization Gallery ({len(st.session_state.history_charts)} charts)")
    
    # Render charts side by side (2 per row)
    charts = st.session_state.history_charts
    
    for i in range(0, len(charts), 2):
        cols = st.columns(2)
        
        # First chart
        with cols[0]:
            chart_data = charts[i]
            st.markdown(f"**{i+1}. {chart_data['title']}**")
            st.plotly_chart(chart_data['fig'], use_container_width=True, key=f"chart_{i}")
            
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.caption(f"Method: {chart_data.get('method', 'N/A')}")
            with col_b:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.history_charts.pop(i)
                    st.rerun()
        
        # Second chart (if exists)
        if i + 1 < len(charts):
            with cols[1]:
                chart_data = charts[i + 1]
                st.markdown(f"**{i+2}. {chart_data['title']}**")
                st.plotly_chart(chart_data['fig'], use_container_width=True, key=f"chart_{i+1}")
                
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.caption(f"Method: {chart_data.get('method', 'N/A')}")
                with col_b:
                    if st.button("🗑️", key=f"del_{i+1}"):
                        st.session_state.history_charts.pop(i + 1)
                        st.rerun()
        
        st.markdown("---")


def render_data_analysis():
    """AI-powered data analysis section"""
    st.markdown("### 🔍 AI Data Analysis")
    
    st.markdown("""
    Ask questions about your data and get AI-powered insights.
    The analysis will be based on the cleaned dataset statistics and patterns.
    """)
    
    # Pre-defined analysis types
    st.markdown("#### 📋 Common Analyses")
    
    analysis_types = templates.get_all_analysis_types()
    
    col1, col2 = st.columns(2)
    
    for idx, analysis_type in enumerate(analysis_types):
        with col1 if idx % 2 == 0 else col2:
            readable_name = analysis_type.replace('_', ' ').title()
            if st.button(f"🔍 {readable_name}", key=f"analysis_{analysis_type}"):
                run_analysis(analysis_type)
    
    st.markdown("---")
    
    # Custom question
    st.markdown("#### 💬 Ask Custom Question")
    
    question = st.text_area(
        "What would you like to know about your customers?",
        placeholder="e.g., What factors most influence customer spending?",
        height=100
    )
    
    if st.button("🤔 Analyze", type="primary"):
        if question:
            with st.spinner("🧠 AI is analyzing your data..."):
                response = st.session_state.coordinator.analyze_data_with_llm(
                    st.session_state.df_clean, question
                )
                
                st.markdown("### 📊 Analysis Results")
                st.markdown(response)
        else:
            st.warning("Please enter a question!")
    
    # Data preview
    st.markdown("---")
    st.markdown("#### 👀 Data Preview")
    
    if st.checkbox("Show dataset"):
        st.dataframe(st.session_state.df_clean.head(100), use_container_width=True)
        
        # Download full dataset
        csv = st.session_state.df_clean.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Dataset",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )


def run_analysis(analysis_type: str):
    """Run a pre-defined analysis"""
    prompt = templates.get_analysis_prompt(analysis_type)
    
    if prompt:
        with st.spinner("🧠 Analyzing..."):
            response = st.session_state.coordinator.analyze_data_with_llm(
                st.session_state.df_clean, prompt
            )
            
            st.markdown(f"### 📊 {analysis_type.replace('_', ' ').title()}")
            st.markdown(response)


def main():
    """Main application entry point"""
    initialize_session_state()
    render_sidebar()
    render_main_content()


if __name__ == "__main__":
    main()
