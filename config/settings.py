"""
Application Settings
Configuration and constants for the dashboard system
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings and configuration"""
    
    # Application Info
    APP_NAME = "AI-Powered Dashboard System"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Multi-agentic AI dashboard with natural language queries"
    
    # API Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # Model Configuration
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash-exp")
    MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
    MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "2048"))
    
    # Database Configuration
    DATABASE_PATH = os.getenv("DATABASE_PATH", "data/database/dashboard.db")
    
    # File Upload Settings
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "200"))
    ALLOWED_FILE_TYPES = os.getenv("ALLOWED_FILE_TYPES", "csv").split(",")
    UPLOAD_DIR = "data/uploads"
    
    # Agent Configuration
    ENABLE_CACHING = os.getenv("ENABLE_CACHING", "True").lower() == "true"
    AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "60"))
    
    # Visualization Settings
    DEFAULT_CHART_HEIGHT = 400
    DEFAULT_CHART_WIDTH = None  # Auto
    CHART_THEME = "plotly"
    
    # Chart Types
    AVAILABLE_CHART_TYPES = [
        "bar_chart",
        "line_chart",
        "scatter_plot",
        "pie_chart",
        "histogram",
        "box_plot",
        "heatmap",
        "area_chart"
    ]
    
    # Data Processing
    MAX_ROWS_DISPLAY = 10000
    MAX_COLUMNS_DISPLAY = 50
    OUTLIER_THRESHOLD = 1.5  # IQR multiplier
    
    # Debug Mode
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate required settings
        
        Returns:
            True if all required settings are valid
        """
        if not cls.GOOGLE_API_KEY:
            print("ERROR: GOOGLE_API_KEY is not set")
            return False
        
        return True
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        directories = [
            cls.UPLOAD_DIR,
            str(Path(cls.DATABASE_PATH).parent),
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_model_config(cls) -> dict:
        """Get model configuration as dictionary"""
        return {
            "model_name": cls.MODEL_NAME,
            "temperature": cls.MODEL_TEMPERATURE,
            "max_output_tokens": cls.MAX_OUTPUT_TOKENS
        }
    
    @classmethod
    def get_database_config(cls) -> dict:
        """Get database configuration as dictionary"""
        return {
            "db_path": cls.DATABASE_PATH
        }
    
    @classmethod
    def get_visualization_config(cls) -> dict:
        """Get visualization configuration as dictionary"""
        return {
            "default_height": cls.DEFAULT_CHART_HEIGHT,
            "default_width": cls.DEFAULT_CHART_WIDTH,
            "theme": cls.CHART_THEME,
            "available_types": cls.AVAILABLE_CHART_TYPES
        }


# Constants
CHART_COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "danger": "#d62728",
    "warning": "#ff9800",
    "info": "#17a2b8"
}

CHART_TEMPLATES = {
    "plotly": "plotly",
    "plotly_white": "plotly_white",
    "plotly_dark": "plotly_dark",
    "ggplot2": "ggplot2",
    "seaborn": "seaborn"
}

# Error Messages
ERROR_MESSAGES = {
    "no_data": "No data available. Please upload a CSV file.",
    "invalid_query": "Could not understand your query. Please try rephrasing.",
    "processing_error": "An error occurred while processing your request.",
    "no_api_key": "Google API key not found. Please set GOOGLE_API_KEY in .env file.",
    "file_too_large": f"File too large. Maximum size is {Settings.MAX_FILE_SIZE_MB}MB.",
    "invalid_file_type": f"Invalid file type. Allowed types: {', '.join(Settings.ALLOWED_FILE_TYPES)}"
}

# Success Messages
SUCCESS_MESSAGES = {
    "upload_success": "File uploaded and processed successfully!",
    "query_success": "Query executed successfully!",
    "data_cleaned": "Data cleaned and ready for analysis!",
    "visualization_generated": "Visualizations generated successfully!"
}

# Query Examples
QUERY_EXAMPLES = {
    "basic": [
        "Show me a summary of the data",
        "Display the first 10 rows",
        "What columns are available?"
    ],
    "visualization": [
        "Create a bar chart of sales by region",
        "Show me a line graph of revenue over time",
        "Display a pie chart of category distribution"
    ],
    "analysis": [
        "Show correlation between price and quantity",
        "Compare average sales across categories",
        "Display distribution of customer ages"
    ],
    "advanced": [
        "Show monthly trends with a moving average",
        "Create a scatter plot with trend line",
        "Display box plots for all numeric columns"
    ]
}
