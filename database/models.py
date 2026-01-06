"""
Data Models
Define data structures for the application
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List


@dataclass
class DatasetModel:
    """Model for dataset metadata"""
    id: Optional[int] = None
    name: str = ""
    original_filename: str = ""
    upload_date: Optional[datetime] = None
    row_count: int = 0
    column_count: int = 0
    columns_info: Optional[Dict] = None
    cleaning_report: Optional[Dict] = None
    table_name: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'original_filename': self.original_filename,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'row_count': self.row_count,
            'column_count': self.column_count,
            'columns_info': self.columns_info,
            'cleaning_report': self.cleaning_report,
            'table_name': self.table_name
        }


@dataclass
class QueryHistoryModel:
    """Model for query history"""
    id: Optional[int] = None
    dataset_id: int = 0
    query_text: str = ""
    query_date: Optional[datetime] = None
    execution_time: float = 0.0
    result_summary: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'dataset_id': self.dataset_id,
            'query_text': self.query_text,
            'query_date': self.query_date.isoformat() if self.query_date else None,
            'execution_time': self.execution_time,
            'result_summary': self.result_summary
        }


@dataclass
class VisualizationSpec:
    """Model for visualization specifications"""
    chart_id: str
    chart_type: str
    data: Optional[Dict] = None
    config: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'chart_id': self.chart_id,
            'chart_type': self.chart_type,
            'data': self.data,
            'config': self.config
        }


@dataclass
class ChartConfig:
    """Model for chart configuration"""
    title: str = ""
    x_axis: str = ""
    y_axis: str = ""
    color: Optional[str] = None
    size: Optional[str] = None
    orientation: str = "v"
    show_legend: bool = True
    height: int = 400
    width: Optional[int] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'title': self.title,
            'x_axis': self.x_axis,
            'y_axis': self.y_axis,
            'color': self.color,
            'size': self.size,
            'orientation': self.orientation,
            'show_legend': self.show_legend,
            'height': self.height,
            'width': self.width
        }
