"""
Prompt Templates
Centralized prompt templates for agents
"""

class PromptTemplates:
    """Collection of prompt templates for various agents"""
    
    # Data Cleaning Prompts
    DATA_CLEANING_ANALYSIS = """
    You are a data quality expert. Analyze the following dataset information:
    
    Dataset Profile:
    - Columns: {columns}
    - Data Types: {dtypes}
    - Missing Values: {missing_values}
    - Total Rows: {total_rows}
    - Sample Data: {sample_data}
    
    Provide recommendations for:
    1. Which columns should be removed (if any) and why
    2. How to handle missing values for each column
    3. Data type conversions needed
    4. Potential data quality issues
    5. Suggested transformations
    
    Format your response as JSON with these keys:
    - columns_to_drop
    - missing_value_strategy
    - data_type_conversions
    - quality_issues
    - recommendations
    """
    
    # Analysis Prompts
    DATA_ANALYSIS_INTENT = """
    You are a data analyst. The user wants to analyze their data.
    
    Dataset Information:
    - Columns: {columns}
    - Numeric Columns: {numeric_columns}
    - Categorical Columns: {categorical_columns}
    - Row Count: {row_count}
    
    User Query: "{user_query}"
    
    Determine the analysis approach:
    1. What columns are relevant to this query?
    2. What type of analysis is needed? (trend, comparison, distribution, correlation)
    3. Should data be grouped? By which columns?
    4. What aggregation method? (sum, mean, count, etc.)
    5. Any filters needed?
    
    Respond with JSON containing:
    - relevant_columns
    - analysis_type
    - grouping_columns
    - aggregation_method
    - filters
    - insights
    """
    
    CORRELATION_ANALYSIS = """
    Analyze the correlation matrix and identify key relationships:
    
    Correlation Data: {correlation_data}
    
    Provide insights about:
    1. Strongest positive correlations
    2. Strongest negative correlations
    3. Potential causal relationships
    4. Surprising or unexpected correlations
    
    Return as JSON with 'insights' list.
    """
    
    # Visualization Prompts
    VISUALIZATION_RECOMMENDATION = """
    You are a data visualization expert. Recommend the best visualizations.
    
    Context:
    - Analysis Type: {analysis_type}
    - Data Columns: {columns}
    - Numeric Columns: {numeric_columns}
    - Categorical Columns: {categorical_columns}
    - User Query: "{user_query}"
    
    Available chart types:
    - bar_chart: Compare categories or groups
    - line_chart: Show trends over time or continuous data
    - scatter_plot: Show relationships between two numeric variables
    - pie_chart: Show proportions of a whole
    - histogram: Show distribution of a single numeric variable
    - box_plot: Show statistical distribution and outliers
    - heatmap: Show correlations or patterns in matrix data
    - area_chart: Show cumulative trends
    
    Recommend:
    1. Primary chart (main visualization)
    2. 1-2 secondary charts (supporting visualizations)
    3. Specific configurations (which columns for x, y, color, etc.)
    4. Layout suggestions
    
    Respond with JSON:
    {{
        "primary_chart": {{"type": "...", "x_axis": "...", "y_axis": "...", "title": "..."}},
        "secondary_charts": [{{"type": "...", "x_axis": "...", "y_axis": "...", "title": "..."}}],
        "layout": "grid"
    }}
    """
    
    CHART_TITLE_GENERATION = """
    Generate a descriptive and concise title for a chart:
    
    Chart Type: {chart_type}
    X-Axis: {x_axis}
    Y-Axis: {y_axis}
    Context: {context}
    
    Provide a clear, professional chart title (max 60 characters).
    Return only the title text, no JSON.
    """
    
    # Intent Classification
    USER_INTENT_CLASSIFICATION = """
    Classify the user's intent from their query:
    
    User Query: "{user_query}"
    Available Columns: {columns}
    
    Classify into one of:
    - visualization: User wants to see charts/graphs
    - analysis: User wants statistical analysis or insights
    - comparison: User wants to compare categories or groups
    - trend: User wants to see trends over time
    - distribution: User wants to understand data distribution
    - correlation: User wants to see relationships
    
    Respond with JSON:
    {{
        "intent_type": "...",
        "entities": ["column1", "column2"],
        "action": "specific action to take",
        "confidence": 0.0-1.0
    }}
    """
    
    # Insight Generation
    INSIGHT_GENERATION = """
    Generate meaningful insights from the analysis results:
    
    Data Summary: {data_summary}
    Analysis Results: {analysis_results}
    User Query: "{user_query}"
    
    Generate 3-5 clear, actionable insights that:
    1. Answer the user's question
    2. Highlight interesting patterns
    3. Provide context and interpretation
    4. Are specific and data-driven
    
    Return as JSON with 'insights' array of strings.
    """
    
    # Error Handling
    ERROR_RECOVERY = """
    An error occurred during processing:
    
    Error: {error_message}
    Context: {context}
    User Query: "{user_query}"
    
    Suggest:
    1. What went wrong
    2. How to fix it
    3. Alternative approaches
    4. User-friendly explanation
    
    Return as JSON with 'explanation' and 'suggestions' fields.
    """
    
    @classmethod
    def get_template(cls, template_name: str) -> str:
        """
        Get a template by name
        
        Args:
            template_name: Name of the template
            
        Returns:
            Template string
        """
        return getattr(cls, template_name.upper(), "")
    
    @classmethod
    def format_template(cls, template_name: str, **kwargs) -> str:
        """
        Get and format a template with variables
        
        Args:
            template_name: Name of the template
            **kwargs: Variables to format the template
            
        Returns:
            Formatted template string
        """
        template = cls.get_template(template_name)
        try:
            return template.format(**kwargs)
        except KeyError as e:
            print(f"Missing template variable: {e}")
            return template
