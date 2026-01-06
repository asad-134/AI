"""
Data Cleaning Agent
Handles data validation, cleaning, and preprocessing
"""

from typing import Dict, Any
import pandas as pd
import numpy as np
from .base_agent import BaseAgent


class DataCleaningAgent(BaseAgent):
    """Agent responsible for cleaning and preprocessing data"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cleaning_prompt = """
        You are a data cleaning expert. Analyze the following data information and provide cleaning recommendations:
        
        Dataset Info:
        - Columns: {columns}
        - Data Types: {dtypes}
        - Missing Values: {missing_values}
        - Sample Data: {sample_data}
        
        Provide a structured JSON response with:
        1. columns_to_drop: List of columns that should be removed (if any)
        2. missing_value_strategy: How to handle missing values for each column
        3. data_type_conversions: Suggested data type conversions
        4. outlier_columns: Columns that might have outliers
        5. recommendations: General cleaning recommendations
        
        Response must be valid JSON only, no additional text.
        """
        
    def execute(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Clean and preprocess the dataframe
        
        Args:
            df: Input dataframe
            
        Returns:
            Dict containing cleaned dataframe and cleaning report
        """
        self.log("Starting data cleaning process")
        
        # Get data profile
        data_profile = self._profile_data(df)
        
        # Get AI recommendations
        recommendations = self._get_cleaning_recommendations(data_profile)
        
        # Apply cleaning
        cleaned_df = self._apply_cleaning(df, recommendations)
        
        # Generate report
        report = self._generate_cleaning_report(df, cleaned_df, recommendations)
        
        self.log("Data cleaning completed")
        
        return {
            "cleaned_data": cleaned_df,
            "report": report,
            "recommendations": recommendations
        }
    
    def _profile_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Profile the dataset to understand its structure"""
        return {
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing_values": {k: int(v) for k, v in df.isnull().sum().items()},
            "sample_data": df.head(3).to_dict(),
            "shape": tuple(df.shape),
            "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
            "categorical_columns": df.select_dtypes(include=['object']).columns.tolist()
        }
    
    def _get_cleaning_recommendations(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI-powered cleaning recommendations"""
        try:
            chain = self.create_chain(self.cleaning_prompt)
            response = chain.invoke({
                "columns": profile["columns"],
                "dtypes": profile["dtypes"],
                "missing_values": profile["missing_values"],
                "sample_data": profile["sample_data"]
            })
            
            # Parse JSON response
            import json
            response_text = response.content if hasattr(response, 'content') else str(response)
            recommendations = json.loads(response_text)
            return recommendations
        except Exception as e:
            self.log(f"Error getting recommendations: {e}", "WARNING")
            return self._get_default_recommendations(profile)
    
    def _get_default_recommendations(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Provide default cleaning recommendations"""
        return {
            "columns_to_drop": [],
            "missing_value_strategy": {
                col: "drop" if profile["missing_values"][col] > len(profile["columns"]) * 0.5 
                else "fill_mean" if col in profile["numeric_columns"] 
                else "fill_mode"
                for col in profile["columns"]
                if profile["missing_values"][col] > 0
            },
            "data_type_conversions": {},
            "outlier_columns": profile["numeric_columns"],
            "recommendations": ["Apply standard cleaning procedures"]
        }
    
    def _apply_cleaning(self, df: pd.DataFrame, recommendations: Dict[str, Any]) -> pd.DataFrame:
        """Apply cleaning operations to the dataframe"""
        cleaned_df = df.copy()
        
        # Drop columns if recommended
        if recommendations.get("columns_to_drop"):
            cleaned_df = cleaned_df.drop(columns=recommendations["columns_to_drop"], errors='ignore')
        
        # Handle missing values
        for col, strategy in recommendations.get("missing_value_strategy", {}).items():
            if col not in cleaned_df.columns:
                continue
                
            if strategy == "drop":
                cleaned_df = cleaned_df.dropna(subset=[col])
            elif strategy == "fill_mean":
                cleaned_df[col].fillna(cleaned_df[col].mean(), inplace=True)
            elif strategy == "fill_median":
                cleaned_df[col].fillna(cleaned_df[col].median(), inplace=True)
            elif strategy == "fill_mode":
                cleaned_df[col].fillna(cleaned_df[col].mode()[0] if not cleaned_df[col].mode().empty else "", inplace=True)
            elif strategy == "fill_zero":
                cleaned_df[col].fillna(0, inplace=True)
        
        # Apply data type conversions
        for col, dtype in recommendations.get("data_type_conversions", {}).items():
            if col in cleaned_df.columns:
                try:
                    cleaned_df[col] = cleaned_df[col].astype(dtype)
                except:
                    self.log(f"Could not convert {col} to {dtype}", "WARNING")
        
        # Remove duplicates
        cleaned_df = cleaned_df.drop_duplicates()
        
        # Strip whitespace from string columns
        string_columns = cleaned_df.select_dtypes(include=['object']).columns
        for col in string_columns:
            cleaned_df[col] = cleaned_df[col].str.strip() if cleaned_df[col].dtype == 'object' else cleaned_df[col]
        
        return cleaned_df
    
    def _generate_cleaning_report(self, original_df: pd.DataFrame, 
                                  cleaned_df: pd.DataFrame, 
                                  recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a report of cleaning operations"""
        return {
            "original_shape": tuple(original_df.shape),
            "cleaned_shape": tuple(cleaned_df.shape),
            "rows_removed": int(original_df.shape[0] - cleaned_df.shape[0]),
            "columns_removed": int(original_df.shape[1] - cleaned_df.shape[1]),
            "missing_values_before": int(original_df.isnull().sum().sum()),
            "missing_values_after": int(cleaned_df.isnull().sum().sum()),
            "duplicates_removed": int(original_df.duplicated().sum()),
            "recommendations_applied": recommendations
        }
