"""
SQLite Manager
Handles all database operations
"""

import sqlite3
import pandas as pd
from typing import Optional, List, Dict, Any
from pathlib import Path
import json
from datetime import datetime


class SQLiteManager:
    """Manages SQLite database operations for the dashboard system"""
    
    def __init__(self, db_path: str = "data/database/dashboard.db"):
        """
        Initialize SQLite Manager
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._create_tables()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Datasets metadata table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS datasets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    original_filename TEXT NOT NULL,
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    row_count INTEGER,
                    column_count INTEGER,
                    columns_info TEXT,
                    cleaning_report TEXT,
                    table_name TEXT UNIQUE NOT NULL
                )
            """)
            
            # Query history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS query_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dataset_id INTEGER,
                    query_text TEXT NOT NULL,
                    query_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    execution_time REAL,
                    result_summary TEXT,
                    FOREIGN KEY (dataset_id) REFERENCES datasets(id)
                )
            """)
            
            # Visualization cache table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS visualization_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dataset_id INTEGER,
                    query_hash TEXT NOT NULL,
                    visualization_spec TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (dataset_id) REFERENCES datasets(id)
                )
            """)
            
            conn.commit()
    
    def save_dataset(self, df: pd.DataFrame, name: str, original_filename: str,
                    cleaning_report: Optional[Dict] = None) -> int:
        """
        Save a dataset to the database
        
        Args:
            df: Dataframe to save
            name: Dataset name
            original_filename: Original filename
            cleaning_report: Report from data cleaning
            
        Returns:
            Dataset ID
        """
        table_name = f"data_{name.lower().replace(' ', '_').replace('-', '_')}"
        
        # Save the actual data
        with self._get_connection() as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            
            # Save metadata
            cursor = conn.cursor()
            
            columns_info = json.dumps({
                'columns': df.columns.tolist(),
                'dtypes': df.dtypes.astype(str).to_dict()
            })
            
            cleaning_report_json = json.dumps(cleaning_report) if cleaning_report else None
            
            cursor.execute("""
                INSERT INTO datasets (name, original_filename, row_count, column_count, 
                                    columns_info, cleaning_report, table_name)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, original_filename, len(df), len(df.columns), 
                  columns_info, cleaning_report_json, table_name))
            
            dataset_id = cursor.lastrowid
            conn.commit()
            
        return dataset_id
    
    def get_dataset(self, dataset_id: int) -> Optional[pd.DataFrame]:
        """
        Retrieve a dataset by ID
        
        Args:
            dataset_id: Dataset ID
            
        Returns:
            Dataframe or None
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT table_name FROM datasets WHERE id = ?", (dataset_id,))
            result = cursor.fetchone()
            
            if result:
                table_name = result['table_name']
                df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
                return df
        
        return None
    
    def get_dataset_by_name(self, name: str) -> Optional[pd.DataFrame]:
        """
        Retrieve a dataset by name
        
        Args:
            name: Dataset name
            
        Returns:
            Dataframe or None
        """
        table_name = f"data_{name.lower().replace(' ', '_').replace('-', '_')}"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM datasets WHERE table_name = ?", (table_name,))
            result = cursor.fetchone()
            
            if result:
                df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
                return df
        
        return None
    
    def list_datasets(self) -> List[Dict[str, Any]]:
        """
        List all available datasets
        
        Returns:
            List of dataset metadata
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, original_filename, upload_date, 
                       row_count, column_count, table_name
                FROM datasets
                ORDER BY upload_date DESC
            """)
            
            datasets = []
            for row in cursor.fetchall():
                datasets.append({
                    'id': row['id'],
                    'name': row['name'],
                    'original_filename': row['original_filename'],
                    'upload_date': row['upload_date'],
                    'row_count': row['row_count'],
                    'column_count': row['column_count'],
                    'table_name': row['table_name']
                })
            
            return datasets
    
    def get_dataset_info(self, dataset_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a dataset
        
        Args:
            dataset_id: Dataset ID
            
        Returns:
            Dataset information
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM datasets WHERE id = ?
            """, (dataset_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row['id'],
                    'name': row['name'],
                    'original_filename': row['original_filename'],
                    'upload_date': row['upload_date'],
                    'row_count': row['row_count'],
                    'column_count': row['column_count'],
                    'columns_info': json.loads(row['columns_info']) if row['columns_info'] else None,
                    'cleaning_report': json.loads(row['cleaning_report']) if row['cleaning_report'] else None,
                    'table_name': row['table_name']
                }
        
        return None
    
    def save_query_history(self, dataset_id: int, query_text: str, 
                          execution_time: float, result_summary: str):
        """
        Save query to history
        
        Args:
            dataset_id: Dataset ID
            query_text: User's query
            execution_time: Time taken to execute
            result_summary: Summary of results
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO query_history (dataset_id, query_text, execution_time, result_summary)
                VALUES (?, ?, ?, ?)
            """, (dataset_id, query_text, execution_time, result_summary))
            conn.commit()
    
    def get_query_history(self, dataset_id: Optional[int] = None, limit: int = 10) -> List[Dict]:
        """
        Get query history
        
        Args:
            dataset_id: Filter by dataset ID (optional)
            limit: Maximum number of records
            
        Returns:
            List of query history records
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if dataset_id:
                cursor.execute("""
                    SELECT * FROM query_history 
                    WHERE dataset_id = ?
                    ORDER BY query_date DESC
                    LIMIT ?
                """, (dataset_id, limit))
            else:
                cursor.execute("""
                    SELECT * FROM query_history 
                    ORDER BY query_date DESC
                    LIMIT ?
                """, (limit,))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'id': row['id'],
                    'dataset_id': row['dataset_id'],
                    'query_text': row['query_text'],
                    'query_date': row['query_date'],
                    'execution_time': row['execution_time'],
                    'result_summary': row['result_summary']
                })
            
            return history
    
    def delete_dataset(self, dataset_id: int) -> bool:
        """
        Delete a dataset and its data
        
        Args:
            dataset_id: Dataset ID
            
        Returns:
            Success status
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Get table name
                cursor.execute("SELECT table_name FROM datasets WHERE id = ?", (dataset_id,))
                result = cursor.fetchone()
                
                if result:
                    table_name = result['table_name']
                    
                    # Drop the data table
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                    
                    # Delete metadata
                    cursor.execute("DELETE FROM datasets WHERE id = ?", (dataset_id,))
                    
                    # Delete related query history
                    cursor.execute("DELETE FROM query_history WHERE dataset_id = ?", (dataset_id,))
                    
                    # Delete cached visualizations
                    cursor.execute("DELETE FROM visualization_cache WHERE dataset_id = ?", (dataset_id,))
                    
                    conn.commit()
                    return True
            
            return False
        except Exception as e:
            print(f"Error deleting dataset: {e}")
            return False
