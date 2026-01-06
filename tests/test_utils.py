"""
Utility Tests
Tests for utility functions
"""

import pytest
import pandas as pd
import numpy as np
from utils.data_processor import DataProcessor
from utils.chart_generator import ChartGenerator


@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe for testing"""
    return pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'Salary': [50000, 60000, 70000],
        'Department': ['Sales', 'IT', 'Sales']
    })


def test_normalize_column_names(sample_dataframe):
    """Test column name normalization"""
    normalized_df = DataProcessor.normalize_column_names(sample_dataframe)
    
    assert 'name' in normalized_df.columns
    assert 'age' in normalized_df.columns
    assert 'salary' in normalized_df.columns


def test_get_summary_statistics(sample_dataframe):
    """Test summary statistics generation"""
    summary = DataProcessor.get_summary_statistics(sample_dataframe)
    
    assert 'shape' in summary
    assert 'total_rows' in summary
    assert 'columns' in summary
    assert summary['total_rows'] == 3


def test_aggregate_data(sample_dataframe):
    """Test data aggregation"""
    agg_df = DataProcessor.aggregate_data(
        df=sample_dataframe,
        group_by=['Department'],
        agg_columns=['Salary'],
        agg_func='mean'
    )
    
    assert len(agg_df) <= len(sample_dataframe)
    assert 'Department' in agg_df.columns


def test_filter_data(sample_dataframe):
    """Test data filtering"""
    filtered_df = DataProcessor.filter_data(
        df=sample_dataframe,
        filters={'Department': 'Sales'}
    )
    
    assert len(filtered_df) == 2
    assert all(filtered_df['Department'] == 'Sales')


def test_create_bar_chart(sample_dataframe):
    """Test bar chart creation"""
    fig = ChartGenerator.create_bar_chart(
        data=sample_dataframe,
        x='Name',
        y='Salary'
    )
    
    assert fig is not None
    assert hasattr(fig, 'data')


def test_create_line_chart(sample_dataframe):
    """Test line chart creation"""
    fig = ChartGenerator.create_line_chart(
        data=sample_dataframe,
        x='Name',
        y='Age'
    )
    
    assert fig is not None
    assert hasattr(fig, 'data')


def test_create_chart_from_spec(sample_dataframe):
    """Test chart creation from specification"""
    spec = {
        'chart_type': 'bar_chart',
        'data': sample_dataframe,
        'config': {
            'x': 'Name',
            'y': 'Salary',
            'title': 'Test Chart'
        }
    }
    
    fig = ChartGenerator.create_chart_from_spec(spec)
    
    assert fig is not None


if __name__ == "__main__":
    pytest.main([__file__])
