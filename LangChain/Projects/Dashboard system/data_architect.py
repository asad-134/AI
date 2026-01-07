"""
Data Architect Agent - Handles data cleaning and feature engineering
Uses Context-Task-Formatting framework for data transformations
"""

import pandas as pd
import numpy as np
from datetime import datetime


class DataArchitect:
    """
    Responsible for data cleaning with intelligent imputation strategies
    """
    
    def __init__(self):
        self.cleaning_report = []
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Main cleaning function following the specified logic:
        - Income: Median imputation grouped by education
        - Categorical/Binary: Mode imputation
        - Feature Engineering: Convert Mnt columns, calculate Customer_Days
        """
        df_clean = df.copy()
        
        # Step 1: Handle Income with Median Imputation grouped by Education
        df_clean = self._impute_income_by_education(df_clean)
        
        # Step 2: Handle Categorical/Binary columns with Mode Imputation
        df_clean = self._impute_categorical_with_mode(df_clean)
        
        # Step 3: Feature Engineering for Mnt (Amount Spent) columns
        df_clean = self._engineer_mnt_features(df_clean)
        
        # Step 4: Calculate Customer_Days if date columns exist
        df_clean = self._calculate_customer_days(df_clean)
        
        # Step 5: Create aggregated spending columns
        df_clean = self._create_spending_aggregates(df_clean)
        
        return df_clean
    
    def _impute_income_by_education(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Context: Income missing values
        Task: Use median imputation grouped by education level
        Formatting: Preserve original data types
        """
        if 'Income' not in df.columns:
            self.cleaning_report.append("⚠️ Income column not found")
            return df
        
        # Identify education columns (education_* pattern)
        education_cols = [col for col in df.columns if col.startswith('education_')]
        
        if not education_cols:
            # Fallback: use overall median if no education columns
            if df['Income'].isnull().sum() > 0:
                median_income = df['Income'].median()
                df['Income'].fillna(median_income, inplace=True)
                self.cleaning_report.append(f"✓ Imputed {df['Income'].isnull().sum()} Income values with overall median: {median_income:.2f}")
        else:
            # Group by education and impute
            missing_before = df['Income'].isnull().sum()
            
            for edu_col in education_cols:
                # For rows where this education is 1 and income is missing
                mask = (df[edu_col] == 1) & (df['Income'].isnull())
                
                if mask.sum() > 0:
                    # Calculate median income for this education group
                    median_income = df[df[edu_col] == 1]['Income'].median()
                    
                    if pd.notna(median_income):
                        df.loc[mask, 'Income'] = median_income
                        self.cleaning_report.append(f"✓ Imputed {mask.sum()} Income values for {edu_col} with median: {median_income:.2f}")
            
            # Handle any remaining missing values with overall median
            if df['Income'].isnull().sum() > 0:
                overall_median = df['Income'].median()
                df['Income'].fillna(overall_median, inplace=True)
                self.cleaning_report.append(f"✓ Imputed remaining Income values with overall median: {overall_median:.2f}")
            
            missing_after = df['Income'].isnull().sum()
            self.cleaning_report.append(f"✓ Income cleaning complete: {missing_before} → {missing_after} missing values")
        
        return df
    
    def _impute_categorical_with_mode(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Context: Categorical and binary flag columns with missing values
        Task: Use mode (most frequent value) imputation
        Formatting: Maintain data type consistency
        """
        # Identify categorical/binary columns (excluding education_ and marital_ which are one-hot encoded)
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Also include binary numeric columns (0/1 flags)
        binary_cols = [col for col in df.columns 
                      if col.startswith(('AcceptedCmp', 'Response', 'Complain', 'Kidhome', 'Teenhome'))]
        
        all_categorical = categorical_cols + binary_cols
        
        for col in all_categorical:
            if df[col].isnull().sum() > 0:
                mode_value = df[col].mode()[0] if len(df[col].mode()) > 0 else df[col].value_counts().index[0]
                missing_count = df[col].isnull().sum()
                df[col].fillna(mode_value, inplace=True)
                self.cleaning_report.append(f"✓ Imputed {missing_count} values in {col} with mode: {mode_value}")
        
        return df
    
    def _engineer_mnt_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Context: Amount Spent columns (Mnt*)
        Task: Ensure all are numeric and properly formatted
        Formatting: Convert to float, handle any non-numeric values
        """
        mnt_cols = [col for col in df.columns if col.startswith('Mnt')]
        
        for col in mnt_cols:
            # Convert to numeric, coercing errors
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Fill any resulting NaNs with 0 (assumption: no purchase = 0 spent)
            if df[col].isnull().sum() > 0:
                df[col].fillna(0, inplace=True)
                self.cleaning_report.append(f"✓ Converted {col} to numeric and filled NaNs with 0")
        
        return df
    
    def _calculate_customer_days(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Context: Date columns that need to be converted to days
        Task: Calculate Customer_Days from date strings if present
        Formatting: Create new numeric column
        """
        # Look for date-related columns
        date_cols = [col for col in df.columns if 'date' in col.lower() or 'dt' in col.lower()]
        
        if date_cols:
            for col in date_cols:
                try:
                    # Convert to datetime
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    
                    # Calculate days from today
                    reference_date = pd.Timestamp.today()
                    df[f'{col}_Days'] = (reference_date - df[col]).dt.days
                    
                    self.cleaning_report.append(f"✓ Created {col}_Days column")
                except Exception as e:
                    self.cleaning_report.append(f"⚠️ Could not process date column {col}: {str(e)}")
        
        # If Customer_Days already exists, ensure it's numeric
        if 'Customer_Days' in df.columns:
            df['Customer_Days'] = pd.to_numeric(df['Customer_Days'], errors='coerce')
            df['Customer_Days'] = df['Customer_Days'].fillna(df['Customer_Days'].median())
        
        return df
    
    def _create_spending_aggregates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Context: Multiple spending columns
        Task: Create useful aggregate columns for analysis
        Formatting: MntTotal, MntRegularProds, MntGoldProds
        """
        mnt_cols = [col for col in df.columns if col.startswith('Mnt') and col != 'MntTotal']
        
        if mnt_cols:
            # Create MntTotal if it doesn't exist
            if 'MntTotal' not in df.columns:
                df['MntTotal'] = df[mnt_cols].sum(axis=1)
                self.cleaning_report.append(f"✓ Created MntTotal from {len(mnt_cols)} spending columns")
            
            # Create MntRegularProds (excluding gold products if separate)
            regular_cols = [col for col in mnt_cols if 'gold' not in col.lower()]
            if regular_cols and 'MntRegularProds' not in df.columns:
                df['MntRegularProds'] = df[regular_cols].sum(axis=1)
                self.cleaning_report.append(f"✓ Created MntRegularProds")
            
            # Create MntGoldProds if gold column exists
            gold_cols = [col for col in mnt_cols if 'gold' in col.lower()]
            if gold_cols and 'MntGoldProds' not in df.columns:
                df['MntGoldProds'] = df[gold_cols].sum(axis=1)
                self.cleaning_report.append(f"✓ Created MntGoldProds")
        
        return df
    
    def get_cleaning_report(self) -> str:
        """Returns a formatted report of all cleaning operations"""
        if not self.cleaning_report:
            return "No cleaning operations performed"
        
        return "\n".join(self.cleaning_report)
    
    def get_data_summary(self, df: pd.DataFrame) -> dict:
        """
        Returns a comprehensive summary of the cleaned dataset
        """
        summary = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "missing_values": df.isnull().sum().sum(),
            "numeric_columns": len(df.select_dtypes(include=[np.number]).columns),
            "categorical_columns": len(df.select_dtypes(include=['object', 'category']).columns),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
            "column_list": df.columns.tolist()
        }
        
        return summary


# Utility function for easy access
def clean_customer_data(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """
    Convenience function to clean data and return cleaned df + report
    """
    architect = DataArchitect()
    cleaned_df = architect.clean_data(df)
    report = architect.get_cleaning_report()
    
    return cleaned_df, report
