"""
Visualizations Component
Handles rendering of different chart types
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, List
import pandas as pd
from utils.chart_generator import ChartGenerator


def render_visualizations(viz_data: Dict[str, Any]):
    """
    Render all visualizations from the visualization agent
    
    Args:
        viz_data: Dictionary containing visualization specifications
    """
    chart_specs = viz_data.get('chart_specifications', [])
    
    if not chart_specs:
        st.warning("No visualizations to display")
        return
    
    st.subheader(f"📊 Generated Visualizations ({len(chart_specs)})")
    
    # Determine layout
    viz_plan = viz_data.get('visualization_plan', {})
    layout = viz_plan.get('layout', 'grid')
    
    if layout == 'grid' and len(chart_specs) > 1:
        render_grid_layout(chart_specs)
    else:
        render_stacked_layout(chart_specs)


def render_grid_layout(chart_specs: List[Dict[str, Any]]):
    """
    Render charts in a grid layout
    
    Args:
        chart_specs: List of chart specifications
    """
    # Determine grid layout based on number of charts
    num_charts = len(chart_specs)
    
    if num_charts == 1:
        cols = [1]
    elif num_charts == 2:
        cols = st.columns(2)
    elif num_charts == 3:
        cols = st.columns(3)
    elif num_charts == 4:
        cols = st.columns(2)
    else:
        cols = st.columns(3)
    
    for idx, spec in enumerate(chart_specs):
        if num_charts <= 3:
            col_idx = idx % len(cols)
        else:
            col_idx = idx % 3 if num_charts > 4 else idx % 2
        
        with cols[col_idx] if isinstance(cols, list) else st.container():
            render_single_chart(spec, idx)


def render_stacked_layout(chart_specs: List[Dict[str, Any]]):
    """
    Render charts in a stacked (vertical) layout
    
    Args:
        chart_specs: List of chart specifications
    """
    for idx, spec in enumerate(chart_specs):
        render_single_chart(spec, idx)
        if idx < len(chart_specs) - 1:
            st.markdown("---")


def render_single_chart(spec: Dict[str, Any], idx: int):
    """
    Render a single chart from specification
    
    Args:
        spec: Chart specification
        idx: Chart index
    """
    try:
        chart_type = spec.get('chart_type', 'bar_chart')
        config = spec.get('config', {})
        title = config.get('title', f'Chart {idx + 1}')
        
        # Display chart title
        st.markdown(f"**{title}**")
        
        # Generate the chart
        fig = ChartGenerator.create_chart_from_spec(spec)
        
        if fig:
            # Display the chart
            st.plotly_chart(fig, use_container_width=True, key=f"chart_{idx}")
            
            # Add download button
            with st.expander("📥 Export Options"):
                col1, col2 = st.columns(2)
                
                with col1:
                    # Download as HTML
                    html_bytes = fig.to_html().encode()
                    st.download_button(
                        label="Download as HTML",
                        data=html_bytes,
                        file_name=f"{title.replace(' ', '_').lower()}.html",
                        mime="text/html",
                        key=f"download_html_{idx}"
                    )
                
                with col2:
                    # Download as PNG (requires kaleido)
                    st.info("PNG export requires kaleido package")
                
                # Show data used for chart
                if 'data' in spec and isinstance(spec['data'], pd.DataFrame):
                    if st.checkbox("Show data", key=f"show_data_{idx}"):
                        st.dataframe(spec['data'], use_container_width=True)
        else:
            st.error(f"Could not generate chart: {chart_type}")
            
    except Exception as e:
        st.error(f"Error rendering chart: {str(e)}")
        with st.expander("Debug Info"):
            st.write("Spec:", spec)
            st.exception(e)


def render_chart_controls(spec: Dict[str, Any], idx: int) -> Dict[str, Any]:
    """
    Render interactive controls for chart customization
    
    Args:
        spec: Chart specification
        idx: Chart index
        
    Returns:
        Updated configuration
    """
    config = spec.get('config', {}).copy()
    
    with st.expander("⚙️ Customize Chart"):
        # Title
        config['title'] = st.text_input(
            "Title",
            value=config.get('title', ''),
            key=f"title_{idx}"
        )
        
        # Height
        config['height'] = st.slider(
            "Height",
            300, 800, config.get('height', 400), 50,
            key=f"height_{idx}"
        )
        
        # Show legend
        config['show_legend'] = st.checkbox(
            "Show Legend",
            value=config.get('show_legend', True),
            key=f"legend_{idx}"
        )
        
        # Color scheme
        color_schemes = ['plotly', 'viridis', 'plasma', 'inferno', 'magma', 'cividis']
        config['colorscale'] = st.selectbox(
            "Color Scheme",
            color_schemes,
            index=0,
            key=f"color_{idx}"
        )
    
    return config


def render_comparison_view(specs: List[Dict[str, Any]]):
    """
    Render multiple charts for comparison
    
    Args:
        specs: List of chart specifications
    """
    st.subheader("📊 Comparison View")
    
    tabs = st.tabs([f"Chart {i+1}" for i in range(len(specs))])
    
    for idx, (tab, spec) in enumerate(zip(tabs, specs)):
        with tab:
            render_single_chart(spec, idx)


def render_data_table(df: pd.DataFrame, title: str = "Data Table"):
    """
    Render an interactive data table
    
    Args:
        df: Dataframe to display
        title: Table title
    """
    st.subheader(title)
    
    # Search/filter
    search = st.text_input("🔍 Search", key=f"search_{title}")
    
    if search:
        # Simple search across all columns
        mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
        df = df[mask]
    
    # Display options
    col1, col2 = st.columns([1, 3])
    with col1:
        rows_to_show = st.selectbox(
            "Rows per page",
            [10, 25, 50, 100],
            key=f"rows_{title}"
        )
    
    # Display dataframe
    st.dataframe(
        df.head(rows_to_show),
        use_container_width=True,
        height=400
    )
    
    # Export options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download CSV",
            csv,
            f"{title.replace(' ', '_').lower()}.csv",
            "text/csv",
            key=f"download_csv_{title}"
        )
    
    with col2:
        excel_bytes = df.to_excel(index=False)
        st.download_button(
            "📥 Download Excel",
            excel_bytes,
            f"{title.replace(' ', '_').lower()}.xlsx",
            "application/vnd.ms-excel",
            key=f"download_excel_{title}"
        )


def render_summary_cards(data: Dict[str, Any]):
    """
    Render summary metric cards
    
    Args:
        data: Dictionary of metrics
    """
    metrics = list(data.items())
    
    if len(metrics) <= 4:
        cols = st.columns(len(metrics))
    else:
        cols = st.columns(4)
    
    for idx, (key, value) in enumerate(metrics):
        col_idx = idx % len(cols)
        with cols[col_idx]:
            if isinstance(value, (int, float)):
                st.metric(key.replace('_', ' ').title(), f"{value:,.2f}" if isinstance(value, float) else f"{value:,}")
            else:
                st.metric(key.replace('_', ' ').title(), str(value))


def render_insights_panel(insights: List[str]):
    """
    Render insights in an attractive panel
    
    Args:
        insights: List of insight strings
    """
    st.subheader("💡 AI-Generated Insights")
    
    for i, insight in enumerate(insights, 1):
        st.info(f"**Insight {i}:** {insight}")


def render_error_state(error_message: str):
    """
    Render error state with helpful information
    
    Args:
        error_message: Error message to display
    """
    st.error("❌ Visualization Error")
    
    with st.expander("Error Details"):
        st.code(error_message)
        
        st.markdown("""
        **Possible Solutions:**
        - Check if your data has the required columns
        - Ensure numeric columns contain valid numbers
        - Try rephrasing your query
        - Upload a different dataset
        """)


def render_loading_state(message: str = "Generating visualizations..."):
    """
    Render loading state
    
    Args:
        message: Loading message
    """
    with st.spinner(message):
        st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h3>🤖 AI is working on your request...</h3>
            <p>This may take a few moments</p>
        </div>
        """, unsafe_allow_html=True)
