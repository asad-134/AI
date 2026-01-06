"""
Chart Generator
Utility for generating various types of charts using Plotly
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, Optional
import numpy as np


class ChartGenerator:
    """Generates charts using Plotly"""
    
    @staticmethod
    def create_bar_chart(data: pd.DataFrame, x: str, y: str, 
                        config: Optional[Dict[str, Any]] = None) -> go.Figure:
        """
        Create a bar chart
        
        Args:
            data: Input dataframe
            x: X-axis column
            y: Y-axis column
            config: Additional configuration
            
        Returns:
            Plotly figure
        """
        config = config or {}
        
        fig = px.bar(
            data, 
            x=x, 
            y=y,
            title=config.get('title', f'{y} by {x}'),
            color=config.get('color'),
            height=config.get('height', 400),
            orientation=config.get('orientation', 'v')
        )
        
        fig.update_layout(
            showlegend=config.get('show_legend', True),
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title=y.replace('_', ' ').title()
        )
        
        return fig
    
    @staticmethod
    def create_line_chart(data: pd.DataFrame, x: str, y: str, 
                         config: Optional[Dict[str, Any]] = None) -> go.Figure:
        """
        Create a line chart
        
        Args:
            data: Input dataframe
            x: X-axis column
            y: Y-axis column
            config: Additional configuration
            
        Returns:
            Plotly figure
        """
        config = config or {}
        
        fig = px.line(
            data, 
            x=x, 
            y=y,
            title=config.get('title', f'{y} over {x}'),
            color=config.get('color'),
            height=config.get('height', 400),
            markers=True
        )
        
        fig.update_layout(
            showlegend=config.get('show_legend', True),
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title=y.replace('_', ' ').title()
        )
        
        return fig
    
    @staticmethod
    def create_scatter_plot(data: pd.DataFrame, x: str, y: str, 
                           config: Optional[Dict[str, Any]] = None) -> go.Figure:
        """
        Create a scatter plot
        
        Args:
            data: Input dataframe
            x: X-axis column
            y: Y-axis column
            config: Additional configuration
            
        Returns:
            Plotly figure
        """
        config = config or {}
        
        fig = px.scatter(
            data, 
            x=x, 
            y=y,
            title=config.get('title', f'{y} vs {x}'),
            color=config.get('color'),
            size=config.get('size'),
            height=config.get('height', 400),
            trendline=config.get('trendline')
        )
        
        fig.update_layout(
            showlegend=config.get('show_legend', True),
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title=y.replace('_', ' ').title()
        )
        
        return fig
    
    @staticmethod
    def create_pie_chart(data: pd.DataFrame, names: str, values: str, 
                        config: Optional[Dict[str, Any]] = None) -> go.Figure:
        """
        Create a pie chart
        
        Args:
            data: Input dataframe
            names: Column for pie slice names
            values: Column for pie slice values
            config: Additional configuration
            
        Returns:
            Plotly figure
        """
        config = config or {}
        
        fig = px.pie(
            data, 
            names=names, 
            values=values,
            title=config.get('title', f'{values} Distribution by {names}'),
            height=config.get('height', 400),
            hole=config.get('hole', 0)  # 0 for pie, >0 for donut
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        return fig
    
    @staticmethod
    def create_histogram(data: pd.DataFrame, x: str, 
                        config: Optional[Dict[str, Any]] = None) -> go.Figure:
        """
        Create a histogram
        
        Args:
            data: Input dataframe
            x: Column to plot
            config: Additional configuration
            
        Returns:
            Plotly figure
        """
        config = config or {}
        
        fig = px.histogram(
            data, 
            x=x,
            title=config.get('title', f'Distribution of {x}'),
            nbins=config.get('nbins', 30),
            height=config.get('height', 400),
            color=config.get('color')
        )
        
        fig.update_layout(
            showlegend=config.get('show_legend', True),
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title='Count'
        )
        
        return fig
    
    @staticmethod
    def create_box_plot(data: pd.DataFrame, y: str, 
                       config: Optional[Dict[str, Any]] = None) -> go.Figure:
        """
        Create a box plot
        
        Args:
            data: Input dataframe
            y: Column to plot
            config: Additional configuration
            
        Returns:
            Plotly figure
        """
        config = config or {}
        
        fig = px.box(
            data, 
            y=y,
            x=config.get('x'),
            title=config.get('title', f'Box Plot of {y}'),
            color=config.get('color'),
            height=config.get('height', 400)
        )
        
        fig.update_layout(
            showlegend=config.get('show_legend', True),
            yaxis_title=y.replace('_', ' ').title()
        )
        
        return fig
    
    @staticmethod
    def create_heatmap(data: Dict[str, Dict[str, float]], 
                      config: Optional[Dict[str, Any]] = None) -> go.Figure:
        """
        Create a heatmap (typically for correlations)
        
        Args:
            data: Dictionary of dictionaries (correlation matrix)
            config: Additional configuration
            
        Returns:
            Plotly figure
        """
        config = config or {}
        
        # Convert dict to dataframe if needed
        if isinstance(data, dict):
            df = pd.DataFrame(data)
        else:
            df = data
        
        fig = go.Figure(data=go.Heatmap(
            z=df.values,
            x=df.columns,
            y=df.index,
            colorscale=config.get('colorscale', 'RdBu'),
            zmid=0
        ))
        
        fig.update_layout(
            title=config.get('title', 'Correlation Heatmap'),
            height=config.get('height', 400),
            xaxis_title='Variables',
            yaxis_title='Variables'
        )
        
        return fig
    
    @staticmethod
    def create_area_chart(data: pd.DataFrame, x: str, y: str, 
                         config: Optional[Dict[str, Any]] = None) -> go.Figure:
        """
        Create an area chart
        
        Args:
            data: Input dataframe
            x: X-axis column
            y: Y-axis column
            config: Additional configuration
            
        Returns:
            Plotly figure
        """
        config = config or {}
        
        fig = px.area(
            data, 
            x=x, 
            y=y,
            title=config.get('title', f'{y} over {x}'),
            color=config.get('color'),
            height=config.get('height', 400)
        )
        
        fig.update_layout(
            showlegend=config.get('show_legend', True),
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title=y.replace('_', ' ').title()
        )
        
        return fig
    
    @staticmethod
    def create_chart_from_spec(spec: Dict[str, Any]) -> Optional[go.Figure]:
        """
        Create a chart based on specification
        
        Args:
            spec: Chart specification with type, data, and config
            
        Returns:
            Plotly figure or None
        """
        chart_type = spec.get('chart_type', '').lower()
        data = spec.get('data')
        config = spec.get('config', {})
        
        if data is None or (isinstance(data, pd.DataFrame) and data.empty):
            return None
        
        # Ensure data is a DataFrame
        if isinstance(data, dict) and chart_type != 'heatmap':
            data = pd.DataFrame(data)
        
        try:
            if chart_type == 'bar_chart':
                return ChartGenerator.create_bar_chart(data, config.get('x'), config.get('y'), config)
            elif chart_type == 'line_chart':
                return ChartGenerator.create_line_chart(data, config.get('x'), config.get('y'), config)
            elif chart_type == 'scatter_plot':
                return ChartGenerator.create_scatter_plot(data, config.get('x'), config.get('y'), config)
            elif chart_type == 'pie_chart':
                return ChartGenerator.create_pie_chart(data, config.get('x'), config.get('y'), config)
            elif chart_type == 'histogram':
                return ChartGenerator.create_histogram(data, config.get('x'), config)
            elif chart_type == 'box_plot':
                return ChartGenerator.create_box_plot(data, config.get('y'), config)
            elif chart_type == 'heatmap':
                return ChartGenerator.create_heatmap(data, config)
            elif chart_type == 'area_chart':
                return ChartGenerator.create_area_chart(data, config.get('x'), config.get('y'), config)
            else:
                # Default to bar chart
                if isinstance(data, pd.DataFrame) and len(data.columns) >= 2:
                    return ChartGenerator.create_bar_chart(data, data.columns[0], data.columns[1], config)
        except Exception as e:
            print(f"Error creating chart: {e}")
            return None
        
        return None
