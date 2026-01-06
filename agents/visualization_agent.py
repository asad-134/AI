"""
Visualization Agent
Generates appropriate visualizations based on data and user intent
"""

from typing import Dict, Any, List
import pandas as pd
from .base_agent import BaseAgent


class VisualizationAgent(BaseAgent):
    """Agent responsible for creating data visualizations"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.visualization_prompt = """
        You are a data visualization expert. Based on the following information, recommend visualizations:
        
        Analysis Plan:
        - Analysis Type: {analysis_type}
        - Relevant Columns: {relevant_columns}
        - Grouping Columns: {grouping_columns}
        - Data Shape: {data_shape}
        
        User Query: {user_query}
        
        Available chart types:
        - bar_chart: Compare categories
        - line_chart: Show trends over time
        - scatter_plot: Show relationships between variables
        - pie_chart: Show proportions
        - histogram: Show distributions
        - box_plot: Show statistical distributions
        - heatmap: Show correlations
        - area_chart: Show cumulative values over time
        
        Provide a JSON response with:
        1. primary_chart: Main chart type and configuration
        2. secondary_charts: Additional supporting charts (up to 2)
        3. chart_configs: Specific configurations for each chart (x_axis, y_axis, color, etc.)
        4. layout: Dashboard layout recommendations
        
        Response must be valid JSON only.
        """
        
    def execute(self, analysis_results: Dict[str, Any], user_query: str) -> Dict[str, Any]:
        """
        Generate visualization recommendations
        
        Args:
            analysis_results: Results from the analysis agent
            user_query: User's original query
            
        Returns:
            Visualization specifications
        """
        self.log(f"Generating visualizations for query: {user_query}")
        
        # Get visualization recommendations
        viz_plan = self._get_visualization_plan(analysis_results, user_query)
        
        # Prepare chart specifications
        chart_specs = self._prepare_chart_specs(viz_plan, analysis_results)
        
        self.log(f"Generated {len(chart_specs)} visualizations")
        
        return {
            "visualization_plan": viz_plan,
            "chart_specifications": chart_specs,
            "data": analysis_results.get("results", {})
        }
    
    def _get_visualization_plan(self, analysis_results: Dict[str, Any], 
                                user_query: str) -> Dict[str, Any]:
        """Get AI-powered visualization recommendations"""
        try:
            analysis_plan = analysis_results.get("analysis_plan", {})
            
            # Get data shape from results
            data_shape = "unknown"
            if "results" in analysis_results and "filtered_data" in analysis_results["results"]:
                data_shape = str(analysis_results["results"]["filtered_data"].shape)
            
            chain = self.create_chain(self.visualization_prompt)
            response = chain.invoke({
                "analysis_type": analysis_plan.get("analysis_type", "unknown"),
                "relevant_columns": analysis_plan.get("relevant_columns", []),
                "grouping_columns": analysis_plan.get("grouping_columns", []),
                "data_shape": data_shape,
                "user_query": user_query
            })
            
            import json
            response_text = response.content if hasattr(response, 'content') else str(response)
            plan = json.loads(response_text)
            return plan
        except Exception as e:
            self.log(f"Error getting visualization plan: {e}", "WARNING")
            return self._get_default_viz_plan(analysis_results)
    
    def _get_default_viz_plan(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Provide default visualization plan"""
        analysis_plan = analysis_results.get("analysis_plan", {})
        relevant_cols = analysis_plan.get("relevant_columns", [])
        grouping_cols = analysis_plan.get("grouping_columns", [])
        
        # Determine chart type based on data
        primary_chart_type = "bar_chart"
        if len(relevant_cols) >= 2:
            primary_chart_type = "scatter_plot"
        elif grouping_cols:
            primary_chart_type = "bar_chart"
        
        return {
            "primary_chart": {
                "type": primary_chart_type,
                "x_axis": grouping_cols[0] if grouping_cols else relevant_cols[0] if relevant_cols else "index",
                "y_axis": relevant_cols[0] if relevant_cols else "value"
            },
            "secondary_charts": [
                {
                    "type": "line_chart",
                    "x_axis": grouping_cols[0] if grouping_cols else relevant_cols[0] if relevant_cols else "index",
                    "y_axis": relevant_cols[1] if len(relevant_cols) > 1 else relevant_cols[0] if relevant_cols else "value"
                }
            ],
            "chart_configs": {},
            "layout": "grid"
        }
    
    def _prepare_chart_specs(self, viz_plan: Dict[str, Any], 
                            analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prepare detailed chart specifications"""
        chart_specs = []
        
        # Get the data to visualize
        results = analysis_results.get("results", {})
        
        # Use aggregated data if available, otherwise filtered data
        if "aggregated_data" in results and not results["aggregated_data"].empty:
            data = results["aggregated_data"]
        elif "filtered_data" in results:
            data = results["filtered_data"]
        else:
            self.log("No data available for visualization", "WARNING")
            return chart_specs
        
        # Primary chart
        primary = viz_plan.get("primary_chart", {})
        if primary:
            chart_specs.append({
                "chart_id": "primary_chart",
                "chart_type": primary.get("type", "bar_chart"),
                "data": data,
                "config": {
                    "x": primary.get("x_axis", data.columns[0] if not data.empty else "x"),
                    "y": primary.get("y_axis", data.columns[1] if len(data.columns) > 1 else "y"),
                    "title": f"{primary.get('type', 'Chart').replace('_', ' ').title()}",
                    "color": primary.get("color"),
                    "size": primary.get("size")
                }
            })
        
        # Secondary charts
        for idx, secondary in enumerate(viz_plan.get("secondary_charts", [])[:2]):
            chart_specs.append({
                "chart_id": f"secondary_chart_{idx + 1}",
                "chart_type": secondary.get("type", "line_chart"),
                "data": data,
                "config": {
                    "x": secondary.get("x_axis", data.columns[0] if not data.empty else "x"),
                    "y": secondary.get("y_axis", data.columns[-1] if not data.empty else "y"),
                    "title": f"{secondary.get('type', 'Chart').replace('_', ' ').title()}",
                    "color": secondary.get("color")
                }
            })
        
        # Add correlation heatmap if correlations are available
        if "correlations" in results and results["correlations"]:
            chart_specs.append({
                "chart_id": "correlation_heatmap",
                "chart_type": "heatmap",
                "data": results["correlations"],
                "config": {
                    "title": "Correlation Heatmap",
                    "colorscale": "RdBu"
                }
            })
        
        return chart_specs
