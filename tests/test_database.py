"""
Database Tests
Tests for database operations
"""

import pytest
import pandas as pd
from pathlib import Path
from database.sqlite_manager import SQLiteManager


@pytest.fixture
def temp_db(tmp_path):
    """Create a temporary database for testing"""
    db_path = tmp_path / "test.db"
    return SQLiteManager(str(db_path))


@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe for testing"""
    return pd.DataFrame({
        'column1': [1, 2, 3, 4, 5],
        'column2': ['a', 'b', 'c', 'd', 'e']
    })


def test_save_dataset(temp_db, sample_dataframe):
    """Test saving a dataset"""
    dataset_id = temp_db.save_dataset(
        df=sample_dataframe,
        name="test_dataset",
        original_filename="test.csv"
    )
    
    assert dataset_id is not None
    assert dataset_id > 0


def test_get_dataset(temp_db, sample_dataframe):
    """Test retrieving a dataset"""
    dataset_id = temp_db.save_dataset(
        df=sample_dataframe,
        name="test_dataset",
        original_filename="test.csv"
    )
    
    retrieved_df = temp_db.get_dataset(dataset_id)
    
    assert retrieved_df is not None
    assert len(retrieved_df) == len(sample_dataframe)
    assert list(retrieved_df.columns) == list(sample_dataframe.columns)


def test_list_datasets(temp_db, sample_dataframe):
    """Test listing datasets"""
    temp_db.save_dataset(
        df=sample_dataframe,
        name="dataset1",
        original_filename="test1.csv"
    )
    
    temp_db.save_dataset(
        df=sample_dataframe,
        name="dataset2",
        original_filename="test2.csv"
    )
    
    datasets = temp_db.list_datasets()
    
    assert len(datasets) == 2
    assert all('name' in ds for ds in datasets)


def test_delete_dataset(temp_db, sample_dataframe):
    """Test deleting a dataset"""
    dataset_id = temp_db.save_dataset(
        df=sample_dataframe,
        name="test_dataset",
        original_filename="test.csv"
    )
    
    success = temp_db.delete_dataset(dataset_id)
    
    assert success is True
    
    retrieved_df = temp_db.get_dataset(dataset_id)
    assert retrieved_df is None


def test_query_history(temp_db, sample_dataframe):
    """Test query history functionality"""
    dataset_id = temp_db.save_dataset(
        df=sample_dataframe,
        name="test_dataset",
        original_filename="test.csv"
    )
    
    temp_db.save_query_history(
        dataset_id=dataset_id,
        query_text="Show me a bar chart",
        execution_time=1.5,
        result_summary="Generated 1 visualization"
    )
    
    history = temp_db.get_query_history()
    
    assert len(history) > 0
    assert history[0]['query_text'] == "Show me a bar chart"


if __name__ == "__main__":
    pytest.main([__file__])
