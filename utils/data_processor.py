"""
Data Processor
Utility functions for data processing and manipulation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import re


class DataProcessor:
    """Handles data processing operations"""
    
    @staticmethod
    def detect_date_columns(df: pd.DataFrame) -> List[str]:
        """
        Detect columns that contain dates
        
        Args:
            df: Input dataframe
            
        Returns:
            List of column names that appear to contain dates
        """
        date_columns = []
        
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try parsing as date
                try:
                    pd.to_datetime(df[col].head(10), errors='coerce')
                    non_null_dates = pd.to_datetime(df[col], errors='coerce').notna().sum()
                    if non_null_dates / len(df) > 0.5:  # More than 50% are valid dates
                        date_columns.append(col)
                except:
                    continue
        
        return date_columns
    
    @staticmethod
    def convert_to_datetime(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Convert specified columns to datetime
        
        Args:
            df: Input dataframe
            columns: Columns to convert
            
        Returns:
            Modified dataframe
        """
        df_copy = df.copy()
        
        for col in columns:
            if col in df_copy.columns:
                try:
                    df_copy[col] = pd.to_datetime(df_copy[col], errors='coerce')
                except:
                    print(f"Could not convert {col} to datetime")
        
        return df_copy
    
    @staticmethod
    def detect_numeric_columns(df: pd.DataFrame) -> List[str]:
        """
        Detect numeric columns including those stored as strings
        
        Args:
            df: Input dataframe
            
        Returns:
            List of numeric column names
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Check object columns that might be numeric
        for col in df.select_dtypes(include=['object']).columns:
            try:
                # Try to convert to numeric
                pd.to_numeric(df[col].str.replace(',', ''), errors='raise')
                numeric_cols.append(col)
            except:
                continue
        
        return numeric_cols
    
    @staticmethod
    def remove_outliers(df: pd.DataFrame, columns: List[str], 
                       method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
        """
        Remove outliers from specified columns
        
        Args:
            df: Input dataframe
            columns: Columns to check for outliers
            method: Method to use ('iqr' or 'zscore')
            threshold: Threshold for outlier detection
            
        Returns:
            Dataframe with outliers removed
        """
        df_copy = df.copy()
        
        for col in columns:
            if col not in df_copy.columns or df_copy[col].dtype not in [np.number]:
                continue
            
            if method == 'iqr':
                Q1 = df_copy[col].quantile(0.25)
                Q3 = df_copy[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                df_copy = df_copy[(df_copy[col] >= lower_bound) & (df_copy[col] <= upper_bound)]
            
            elif method == 'zscore':
                z_scores = np.abs((df_copy[col] - df_copy[col].mean()) / df_copy[col].std())
                df_copy = df_copy[z_scores < threshold]
        
        return df_copy
    
    @staticmethod
    def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize column names (lowercase, replace spaces with underscores)
        
        Args:
            df: Input dataframe
            
        Returns:
            Dataframe with normalized column names
        """
        df_copy = df.copy()
        
        new_columns = []
        for col in df_copy.columns:
            # Convert to lowercase, replace spaces and special chars with underscore
            new_col = re.sub(r'[^a-zA-Z0-9_]', '_', col.lower().strip())
            new_col = re.sub(r'_+', '_', new_col)  # Remove multiple underscores
            new_col = new_col.strip('_')  # Remove leading/trailing underscores
            new_columns.append(new_col)
        
        df_copy.columns = new_columns
        return df_copy
    
    @staticmethod
    def get_summary_statistics(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get comprehensive summary statistics
        
        Args:
            df: Input dataframe
            
        Returns:
            Dictionary of summary statistics
        """
        summary = {
            'shape': df.shape,
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
            'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': df.select_dtypes(include=['object', 'category']).columns.tolist(),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # MB
        }
        
        # Numeric statistics
        numeric_cols = summary['numeric_columns']
        if numeric_cols:
            summary['numeric_stats'] = df[numeric_cols].describe().to_dict()
        
        # Categorical statistics
        categorical_cols = summary['categorical_columns']
        if categorical_cols:
            summary['categorical_stats'] = {}
            for col in categorical_cols[:5]:  # Limit to first 5
                summary['categorical_stats'][col] = {
                    'unique_values': df[col].nunique(),
                    'top_values': df[col].value_counts().head(5).to_dict()
                }
        
        return summary
    
    @staticmethod
    def aggregate_data(df: pd.DataFrame, group_by: List[str], 
                      agg_columns: List[str], agg_func: str = 'mean') -> pd.DataFrame:
        """
        Aggregate data by specified columns
        
        Args:
            df: Input dataframe
            group_by: Columns to group by
            agg_columns: Columns to aggregate
            agg_func: Aggregation function
            
        Returns:
            Aggregated dataframe
        """
        valid_group_cols = [col for col in group_by if col in df.columns]
        valid_agg_cols = [col for col in agg_columns if col in df.columns]
        
        if not valid_group_cols or not valid_agg_cols:
            return df
        
        agg_map = {
            'mean': 'mean',
            'sum': 'sum',
            'count': 'count',
            'min': 'min',
            'max': 'max',
            'median': 'median',
            'std': 'std'
        }
        
        agg_function = agg_map.get(agg_func, 'mean')
        
        return df.groupby(valid_group_cols)[valid_agg_cols].agg(agg_function).reset_index()
    
    @staticmethod
    def filter_data(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply filters to dataframe
        
        Args:
            df: Input dataframe
            filters: Dictionary of column: value pairs
            
        Returns:
            Filtered dataframe
        """
        filtered_df = df.copy()
        
        for column, value in filters.items():
            if column in filtered_df.columns:
                if isinstance(value, (list, tuple)):
                    filtered_df = filtered_df[filtered_df[column].isin(value)]
                else:
                    filtered_df = filtered_df[filtered_df[column] == value]
        
        return filtered_df
    
    @staticmethod
    def pivot_data(df: pd.DataFrame, index: str, columns: str, 
                   values: str, aggfunc: str = 'sum') -> pd.DataFrame:
        """
        Create pivot table
        
        Args:
            df: Input dataframe
            index: Column to use as index
            columns: Column to use as columns
            values: Column to aggregate
            aggfunc: Aggregation function
            
        Returns:
            Pivot table
        """
        try:
            return pd.pivot_table(df, values=values, index=index, 
                                columns=columns, aggfunc=aggfunc, fill_value=0)
        except:
            return df
