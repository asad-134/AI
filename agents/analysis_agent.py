"""
Analysis Agent
Performs data analysis and statistical operations
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from .base_agent import BaseAgent


class AnalysisAgent(BaseAgent):
    """Agent responsible for analyzing data and extracting insights"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analysis_prompt = """
        You are a data analysis expert. Analyze the following dataset information:
        
        Dataset Overview:
        - Shape: {shape}
        - Columns: {columns}
        - Numeric Columns: {numeric_columns}
        - Categorical Columns: {categorical_columns}
        - Statistics: {statistics}
        
        User Query: {user_query}
        
        Based on the user query and data, provide a JSON response with:
        1. relevant_columns: List of columns relevant to the query
        2. analysis_type: Type of analysis needed (correlation, distribution, comparison, trend, etc.)
        3. grouping_columns: Columns to group by (if applicable)
        4. aggregation_method: How to aggregate data (sum, mean, count, etc.)
        5. filters: Any filters to apply to the data
        6. insights: Key insights about the data
        
        Response must be valid JSON only.
        """
        
    def execute(self, df: pd.DataFrame, user_query: str) -> Dict[str, Any]:
        """
        Analyze data based on user query
        
        Args:
            df: Dataframe to analyze
            user_query: User's natural language query
            
        Returns:
            Analysis results and recommendations
        """
        self.log(f"Analyzing data for query: {user_query}")
        
        # Get data profile
        profile = self._profile_data(df)
        
        # Get AI analysis recommendations
        analysis_plan = self._get_analysis_plan(profile, user_query)
        
        # Perform analysis
        analysis_results = self._perform_analysis(df, analysis_plan)
        
        # Generate insights
        insights = self._generate_insights(df, analysis_results, analysis_plan)
        
        self.log("Analysis completed")
        
        return {
            "analysis_plan": analysis_plan,
            "results": analysis_results,
            "insights": insights,
            "data_profile": profile
        }
    
    def _profile_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Profile the dataset"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Get basic statistics
        stats = {}
        if numeric_cols:
            stats = df[numeric_cols].describe().to_dict()
        
        return {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols,
            "statistics": stats,
            "dtypes": df.dtypes.astype(str).to_dict()
        }
    
    def _get_analysis_plan(self, profile: Dict[str, Any], user_query: str) -> Dict[str, Any]:
        """Get AI-powered analysis plan"""
        try:
            chain = self.create_chain(self.analysis_prompt)
            response = chain.invoke({
                "shape": profile["shape"],
                "columns": profile["columns"],
                "numeric_columns": profile["numeric_columns"],
                "categorical_columns": profile["categorical_columns"],
                "statistics": profile["statistics"],
                "user_query": user_query
            })
            
            import json
            response_text = response.content if hasattr(response, 'content') else str(response)
            plan = json.loads(response_text)
            return plan
        except Exception as e:
            self.log(f"Error getting analysis plan: {e}", "WARNING")
            return self._get_default_plan(profile, user_query)
    
    def _get_default_plan(self, profile: Dict[str, Any], user_query: str) -> Dict[str, Any]:
        """Provide default analysis plan"""
        return {
            "relevant_columns": profile["numeric_columns"][:3] if profile["numeric_columns"] else profile["columns"][:3],
            "analysis_type": "distribution",
            "grouping_columns": profile["categorical_columns"][:1] if profile["categorical_columns"] else [],
            "aggregation_method": "mean",
            "filters": {},
            "insights": ["Standard analysis performed"]
        }
    
    def _perform_analysis(self, df: pd.DataFrame, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Perform the actual analysis"""
        results = {}
        
        relevant_cols = plan.get("relevant_columns", [])
        grouping_cols = plan.get("grouping_columns", [])
        agg_method = plan.get("aggregation_method", "mean")
        
        # Apply filters if any
        filtered_df = df.copy()
        for col, condition in plan.get("filters", {}).items():
            if col in filtered_df.columns:
                # Simple equality filter for now
                filtered_df = filtered_df[filtered_df[col] == condition]
        
        results["filtered_data"] = filtered_df
        
        # Perform grouping and aggregation
        if grouping_cols and relevant_cols:
            valid_group_cols = [col for col in grouping_cols if col in filtered_df.columns]
            valid_rel_cols = [col for col in relevant_cols if col in filtered_df.columns]
            
            if valid_group_cols and valid_rel_cols:
                grouped = filtered_df.groupby(valid_group_cols)[valid_rel_cols]
                
                if agg_method == "mean":
                    results["aggregated_data"] = grouped.mean().reset_index()
                elif agg_method == "sum":
                    results["aggregated_data"] = grouped.sum().reset_index()
                elif agg_method == "count":
                    results["aggregated_data"] = grouped.count().reset_index()
                elif agg_method == "median":
                    results["aggregated_data"] = grouped.median().reset_index()
                else:
                    results["aggregated_data"] = grouped.mean().reset_index()
        
        # Calculate correlations for numeric columns
        numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) > 1:
            results["correlations"] = filtered_df[numeric_cols].corr().to_dict()
        
        # Get value counts for categorical columns
        categorical_cols = filtered_df.select_dtypes(include=['object', 'category']).columns.tolist()
        results["value_counts"] = {}
        for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
            results["value_counts"][col] = filtered_df[col].value_counts().head(10).to_dict()
        
        return results
    
    def _generate_insights(self, df: pd.DataFrame, results: Dict[str, Any], 
                          plan: Dict[str, Any]) -> List[str]:
        """Generate insights from analysis results"""
        insights = []
        
        # Add insights from the plan
        if "insights" in plan:
            insights.extend(plan["insights"])
        
        # Add data-driven insights
        if "aggregated_data" in results and not results["aggregated_data"].empty:
            agg_df = results["aggregated_data"]
            numeric_cols = agg_df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) > 0:
                for col in numeric_cols:
                    max_val = agg_df[col].max()
                    max_idx = agg_df[col].idxmax()
                    grouping_col = plan.get("grouping_columns", ["group"])[0]
                    
                    if grouping_col in agg_df.columns:
                        max_group = agg_df.loc[max_idx, grouping_col]
                        insights.append(f"Highest {col}: {max_val:.2f} in {max_group}")
        
        # Correlation insights
        if "correlations" in results:
            # Find strongest correlations
            for col1, corr_dict in results["correlations"].items():
                for col2, corr_val in corr_dict.items():
                    if col1 != col2 and abs(corr_val) > 0.7:
                        insights.append(f"Strong correlation between {col1} and {col2}: {corr_val:.2f}")
        
        return insights if insights else ["Analysis completed successfully"]
