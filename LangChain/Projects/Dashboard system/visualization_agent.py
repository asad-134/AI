"""
Visualization Agent - Senior Marketing & Financial Analyst Persona
Transforms raw data into executive-level insights using Plotly
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any
import json
import re


class VisualizationAgent:
    """
    Acts as a Senior Marketing & Financial Analyst
    Interprets requests through Context + Task + Formatting framework
    """
    
    def __init__(self):
        self.persona_prompt = """
You are a Senior Marketing & Financial Analyst with expertise in customer analytics.
Your goal is to transform raw customer data into executive-level insights.

FRAMEWORK: Context + Task + Formatting

AVAILABLE COLUMNS IN DATASET:
- Demographics: Age, Income, Education (education_*), Marital Status (marital_*)
- Spending: MntWines, MntFruits, MntMeatProducts, MntFishProducts, MntSweetProducts, MntGoldProds, MntTotal, MntRegularProds
- Campaigns: AcceptedCmp1, AcceptedCmp2, AcceptedCmp3, AcceptedCmp4, AcceptedCmp5, Response
- Family: Kidhome, Teenhome
- Behavior: NumWebVisitsMonth, Recency, Customer_Days
- Other: Complain, NumDealsPurchases, NumWebPurchases, NumCatalogPurchases, NumStorePurchases

CHART TYPES AVAILABLE:
1. KPI Card - Single metric with conditional coloring
2. Bar Chart - Comparisons across categories
3. Scatter Plot - Relationships between two numeric variables
4. Heatmap - Correlations between multiple variables
5. Treemap - Hierarchical data visualization
6. Line Chart - Trends over time
7. Box Plot - Distribution analysis
8. Histogram - Frequency distribution

FORMATTING RULES:
- Always use Plotly Express or Plotly Graph Objects
- Use professional color palettes: plotly_dark, viridis, Blues, Reds
- All axes must be labeled clearly
- Titles must be descriptive and executive-ready
- Include legends where appropriate

When generating code:
1. Return ONLY executable Python code
2. Assume 'df' variable contains the cleaned dataframe
3. Store the result in a variable called 'fig'
4. Do not include import statements (already imported)
5. Code should be ready to execute with exec()
"""
        
        self.color_palettes = {
            'default': px.colors.qualitative.Plotly,
            'viridis': px.colors.sequential.Viridis,
            'blues': px.colors.sequential.Blues,
            'reds': px.colors.sequential.Reds,
            'professional': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        }
    
    def parse_visualization_request(self, user_prompt: str, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyzes user prompt to extract:
        - Chart type
        - Columns involved
        - Special requirements (colors, thresholds, etc.)
        """
        request = {
            'chart_type': self._detect_chart_type(user_prompt),
            'columns': self._extract_columns(user_prompt, df),
            'aggregation': self._detect_aggregation(user_prompt),
            'color_condition': self._detect_color_condition(user_prompt),
            'sorting': self._detect_sorting(user_prompt)
        }
        
        return request
    
    def _detect_chart_type(self, prompt: str) -> str:
        """Identifies the requested chart type from prompt"""
        prompt_lower = prompt.lower()
        
        chart_keywords = {
            'kpi': ['kpi', 'metric', 'card', 'indicator', 'conversion rate'],
            'bar': ['bar', 'compare', 'comparison', 'across', 'column'],
            'scatter': ['scatter', 'plot', 'relationship', 'correlation plot', 'vs'],
            'heatmap': ['heatmap', 'correlation', 'heat map'],
            'treemap': ['treemap', 'tree map', 'hierarchical'],
            'line': ['line', 'trend', 'over time', 'time series'],
            'box': ['box', 'distribution', 'quartile'],
            'histogram': ['histogram', 'frequency', 'distribution']
        }
        
        for chart_type, keywords in chart_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return chart_type
        
        return 'bar'  # Default
    
    def _extract_columns(self, prompt: str, df: pd.DataFrame) -> list:
        """Extracts column names mentioned in the prompt"""
        columns = []
        
        for col in df.columns:
            if col.lower() in prompt.lower() or col in prompt:
                columns.append(col)
        
        return columns
    
    def _detect_aggregation(self, prompt: str) -> str:
        """Detects aggregation type (average, sum, count, etc.)"""
        prompt_lower = prompt.lower()
        
        if 'average' in prompt_lower or 'mean' in prompt_lower or 'avg' in prompt_lower:
            return 'mean'
        elif 'sum' in prompt_lower or 'total' in prompt_lower:
            return 'sum'
        elif 'count' in prompt_lower:
            return 'count'
        elif 'median' in prompt_lower:
            return 'median'
        
        return 'mean'  # Default
    
    def _detect_color_condition(self, prompt: str) -> dict:
        """Extracts conditional coloring requirements"""
        condition = {}
        
        # Look for patterns like "below 15%, color red"
        threshold_pattern = r'(below|above|less than|greater than|<|>)\s*(\d+\.?\d*)'
        color_pattern = r'color\s+(\w+)'
        
        threshold_match = re.search(threshold_pattern, prompt.lower())
        color_match = re.search(color_pattern, prompt.lower())
        
        if threshold_match:
            operator = threshold_match.group(1)
            value = float(threshold_match.group(2))
            condition['operator'] = 'lt' if operator in ['below', 'less than', '<'] else 'gt'
            condition['value'] = value
        
        if color_match:
            condition['color'] = color_match.group(1)
        
        return condition
    
    def _detect_sorting(self, prompt: str) -> str:
        """Detects sorting requirements"""
        prompt_lower = prompt.lower()
        
        if 'descending' in prompt_lower or 'highest' in prompt_lower or 'most' in prompt_lower:
            return 'descending'
        elif 'ascending' in prompt_lower or 'lowest' in prompt_lower or 'least' in prompt_lower:
            return 'ascending'
        
        return None
    
    def generate_kpi_code(self, metric_col: str, df: pd.DataFrame, condition: dict = None) -> str:
        """Generates code for a KPI card with conditional coloring"""
        value = df[metric_col].mean() if metric_col in df.columns else 0
        
        color = "green"
        if condition:
            if condition['operator'] == 'lt' and value < condition['value']:
                color = condition.get('color', 'red')
            elif condition['operator'] == 'gt' and value > condition['value']:
                color = condition.get('color', 'red')
        
        metric_title = metric_col.replace('_', ' ').title()
        
        code = f"""
# KPI Card for {metric_col}
value = df['{metric_col}'].mean() * 100 if '{metric_col}' in df.columns else 0

fig = go.Figure(go.Indicator(
    mode="number+delta",
    value=value,
    title=dict(text="{metric_title}", font=dict(size=24)),
    number=dict(suffix="%", font=dict(size=48, color="{color}")),
    domain=dict(x=[0, 1], y=[0, 1])
))

fig.update_layout(
    height=300,
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
"""
        return code
    
    def generate_bar_chart_code(self, x_col: str, y_col: str, df: pd.DataFrame, 
                               aggregation: str = 'mean', sorting: str = None) -> str:
        """Generates code for a bar chart with aggregation"""
        sort_code = ""
        if sorting == 'descending':
            sort_code = ".sort_values(ascending=False)"
        elif sorting == 'ascending':
            sort_code = ".sort_values(ascending=True)"
        
        x_label = x_col.replace("_", " ").title()
        y_label = y_col.replace("_", " ").title()
        agg_title = aggregation.title()
        chart_title = f"{agg_title} {y_label} by {x_label}"
        
        code = f"""
# Bar Chart: {y_col} by {x_col}
grouped_data = df.groupby('{x_col}')['{y_col}'].{aggregation}(){sort_code}.reset_index()

fig = px.bar(
    grouped_data,
    x='{x_col}',
    y='{y_col}',
    title='{chart_title}',
    labels={{'{x_col}': '{x_label}', '{y_col}': '{agg_title} {y_label}'}},
    color='{y_col}',
    color_continuous_scale='Viridis',
    template='plotly_dark'
)

fig.update_layout(
    height=500,
    showlegend=False,
    xaxis_tickangle=-45
)
"""
        return code
    
    def generate_scatter_code(self, x_col: str, y_col: str, color_col: str = None, 
                             df: pd.DataFrame = None) -> str:
        """Generates code for a scatter plot"""
        color_param = f", color='{color_col}'" if color_col else ""
        
        code = f"""
# Scatter Plot: {y_col} vs {x_col}
fig = px.scatter(
    df,
    x='{x_col}',
    y='{y_col}'{color_param},
    title='{y_col.replace("_", " ").title()} vs {x_col.replace("_", " ").title()}',
    labels={{'{x_col}': '{x_col.replace("_", " ").title()}', '{y_col}': '{y_col.replace("_", " ").title()}'}},
    template='plotly_dark',
    opacity=0.7
)

fig.update_traces(marker=dict(size=8))
fig.update_layout(height=500)
"""
        return code
    
    def generate_heatmap_code(self, columns: list) -> str:
        """Generates code for a correlation heatmap"""
        cols_str = str(columns)
        
        code = f"""
# Correlation Heatmap
selected_cols = {cols_str}
corr_matrix = df[selected_cols].corr()

fig = px.imshow(
    corr_matrix,
    title='Correlation Heatmap',
    labels=dict(color="Correlation"),
    color_continuous_scale='RdBu_r',
    aspect='auto',
    template='plotly_dark'
)

fig.update_layout(
    height=500,
    xaxis_tickangle=-45
)
"""
        return code
    
    def generate_treemap_code(self, values_col: str, group_col: str) -> str:
        """Generates code for a treemap"""
        values_label = values_col.replace("_", " ").title()
        group_label = group_col.replace("_", " ").title()
        chart_title = f"{values_label} Distribution by {group_label}"
        
        code = f"""
# Treemap: {values_col} grouped by {group_col}
grouped_data = df.groupby('{group_col}')['{values_col}'].sum().reset_index()

fig = px.treemap(
    grouped_data,
    path=['{group_col}'],
    values='{values_col}',
    title='{chart_title}',
    color='{values_col}',
    color_continuous_scale='Viridis',
    template='plotly_dark'
)

fig.update_layout(height=500)
"""
        return code
    
    def create_visualization_from_prompt(self, prompt: str, df: pd.DataFrame) -> tuple:
        """
        Main method: Parses prompt and generates appropriate visualization code
        Returns: (code_string, chart_type)
        """
        parsed = self.parse_visualization_request(prompt, df)
        chart_type = parsed['chart_type']
        columns = parsed['columns']
        
        code = ""
        
        try:
            if chart_type == 'kpi':
                metric_col = columns[0] if columns else 'Response'
                code = self.generate_kpi_code(metric_col, df, parsed['color_condition'])
            
            elif chart_type == 'bar':
                if len(columns) >= 2:
                    # Check if columns exist
                    x_col = columns[0] if columns[0] in df.columns else df.columns[0]
                    y_col = columns[1] if columns[1] in df.columns else df.select_dtypes(include=['number']).columns[0]
                    code = self.generate_bar_chart_code(
                        x_col, y_col, df, 
                        parsed['aggregation'], parsed['sorting']
                    )
                else:
                    # Default bar chart - find suitable columns
                    cat_cols = df.select_dtypes(include=['object', 'category']).columns
                    num_cols = df.select_dtypes(include=['number']).columns
                    
                    if len(cat_cols) > 0 and len(num_cols) > 0:
                        x_col = cat_cols[0]
                        y_col = num_cols[0]
                    else:
                        x_col = df.columns[0]
                        y_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
                    
                    code = self.generate_bar_chart_code(
                        x_col, y_col, df,
                        parsed['aggregation'], parsed['sorting']
                    )
            
            elif chart_type == 'scatter':
                if len(columns) >= 2:
                    x_col = columns[0] if columns[0] in df.columns else df.select_dtypes(include=['number']).columns[0]
                    y_col = columns[1] if columns[1] in df.columns else df.select_dtypes(include=['number']).columns[1]
                    color_col = columns[2] if len(columns) > 2 and columns[2] in df.columns else None
                    code = self.generate_scatter_code(x_col, y_col, color_col, df)
                else:
                    # Find two numeric columns
                    num_cols = df.select_dtypes(include=['number']).columns
                    if len(num_cols) >= 2:
                        code = self.generate_scatter_code(num_cols[0], num_cols[1], None, df)
                    else:
                        code = self.generate_scatter_code(df.columns[0], df.columns[1], None, df)
            
            elif chart_type == 'heatmap':
                if len(columns) >= 2:
                    # Filter to only existing numeric columns
                    valid_cols = [col for col in columns if col in df.columns and df[col].dtype in ['int64', 'float64']]
                    if len(valid_cols) >= 2:
                        code = self.generate_heatmap_code(valid_cols)
                    else:
                        # Use numeric columns from dataframe
                        num_cols = df.select_dtypes(include=['number']).columns.tolist()[:4]
                        code = self.generate_heatmap_code(num_cols if len(num_cols) >= 2 else df.columns.tolist()[:4])
                else:
                    # Get numeric columns for correlation
                    num_cols = df.select_dtypes(include=['number']).columns.tolist()[:4]
                    code = self.generate_heatmap_code(num_cols if len(num_cols) >= 2 else df.columns.tolist()[:4])
            
            elif chart_type == 'treemap':
                if len(columns) >= 2:
                    # values_col should be numeric, group_col can be categorical
                    group_col = columns[0] if columns[0] in df.columns else df.columns[0]
                    values_col = columns[1] if columns[1] in df.columns else df.select_dtypes(include=['number']).columns[0]
                    code = self.generate_treemap_code(values_col, group_col)
                else:
                    # Find suitable columns
                    cat_cols = df.select_dtypes(include=['object', 'category']).columns
                    num_cols = df.select_dtypes(include=['number']).columns
                    
                    if len(cat_cols) > 0 and len(num_cols) > 0:
                        code = self.generate_treemap_code(num_cols[0], cat_cols[0])
                    else:
                        code = self.generate_treemap_code(df.columns[1] if len(df.columns) > 1 else df.columns[0], df.columns[0])
            
            else:
                # Default to bar chart
                code = self.generate_bar_chart_code('education_Graduation', 'MntTotal', df)
        
        except Exception as e:
            # Fallback: simple bar chart
            code = f"""
# Fallback Visualization
fig = px.bar(df.head(10), x=df.columns[0], y=df.columns[1], 
             title='Data Overview', template='plotly_dark')
fig.update_layout(height=500)
"""
        
        return code, chart_type
    
    def execute_visualization_code(self, code: str, df: pd.DataFrame):
        """
        Safely executes the generated code and returns the figure
        """
        try:
            # Validate and fix common code issues before execution
            sanitized_code = self._sanitize_code(code, df)
            
            # If sanitization failed, regenerate with rule-based approach
            if sanitized_code is None:
                print("Warning: Code sanitization failed, regenerating with rule-based approach...")
                # Use a simple bar chart as fallback
                cat_cols = df.select_dtypes(include=['object', 'category']).columns
                num_cols = df.select_dtypes(include=['number']).columns
                if len(cat_cols) > 0 and len(num_cols) > 0:
                    sanitized_code = f"""
import plotly.express as px
fig = px.bar(df.groupby('{cat_cols[0]}')['{num_cols[0]}'].mean().reset_index(),
             x='{cat_cols[0]}', y='{num_cols[0]}',
             title='Data Overview', template='plotly_dark')
fig.update_layout(height=500)
"""
                else:
                    # Ultimate fallback
                    sanitized_code = f"""
import plotly.express as px
fig = px.scatter(df.head(100), x=df.columns[0], y=df.columns[1],
                title='Data Overview', template='plotly_dark')
fig.update_layout(height=500)
"""
            
            # Create execution environment
            exec_globals = {
                'df': df,
                'pd': pd,
                'px': px,
                'go': go,
                'fig': None
            }
            
            # Execute the code
            exec(sanitized_code, exec_globals)
            
            # Return the figure
            fig = exec_globals.get('fig')
            
            if fig is None:
                # Try to create a simple fallback visualization
                print("Warning: No figure was created. Creating fallback...")
                fig = px.scatter(df.head(100), x=df.columns[0], y=df.columns[1], 
                               title='Fallback Visualization', template='plotly_dark')
            
            return fig
        
        except Exception as e:
            print(f"Error executing visualization code: {str(e)}")
            print(f"Code was:\n{code}")
            
            # Return error figure with message
            error_fig = go.Figure()
            error_fig.add_annotation(
                text=f"Error generating visualization:<br>{str(e)}<br><br>Try rephrasing your prompt or use a different chart type.",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=14, color="red"),
                align="center"
            )
            error_fig.update_layout(
                template='plotly_dark',
                height=400,
                xaxis=dict(visible=False),
                yaxis=dict(visible=False)
            )
            return error_fig
    
    def _sanitize_code(self, code: str, df: pd.DataFrame) -> str:
        """
        Sanitize and fix common issues in generated code
        """
        import re
        
        # Only fix go.Figure/go.Scatter/go.Bar syntax, NOT px.* functions
        # px.* functions use column names as strings correctly
        
        # Fix 1: Only replace x='column' with x=df['column'] if it's in go.Scatter/Bar/etc
        # Check if this is go.Figure code (not plotly express)
        if 'go.Figure' in code or 'go.Scatter' in code or 'go.Bar' in code:
            # Pattern: x='column_name' -> x=df['column_name'] in go.* functions
            code = re.sub(r"(go\.\w+\([^)]*\b)x\s*=\s*'([^']+)'", r"\1x=df['\2']", code)
            code = re.sub(r"(go\.\w+\([^)]*\b)y\s*=\s*'([^']+)'", r"\1y=df['\2']", code)
            code = re.sub(r"(go\.\w+\([^)]*\b)text\s*=\s*'([^']+)'", r"\1text=df['\2']", code)
            code = re.sub(r"(go\.\w+\([^)]*\b)values\s*=\s*'([^']+)'", r"\1values=df['\2']", code)
            
            # Fix marker={} to marker=dict()
            code = re.sub(r'\bmarker\s*=\s*\{', 'marker=dict(', code)
        
        # Fix 2: Fix go.Layout in data parameter - this is invalid
        if 'go.Layout' in code and 'data=' in code:
            print("Warning: Detected invalid go.Layout usage, switching to rule-based generation")
            return None
        
        # Fix 3: Fix invalid histogram parameters
        code = code.replace("histnorm='quantile'", "histnorm='percent'")
        
        # Fix 4: Validate column references in grouped_data or df['column']
        # Find columns that don't exist
        column_pattern = r"df\['([^']+)'\]"
        columns_used = re.findall(column_pattern, code)
        for col in columns_used:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found in dataframe")
                # Find closest match
                from difflib import get_close_matches
                matches = get_close_matches(col, df.columns, n=1, cutoff=0.6)
                if matches:
                    print(f"  -> Replacing with '{matches[0]}'")
                    code = code.replace(f"df['{col}']", f"df['{matches[0]}']")
                else:
                    return None  # Can't fix, force rule-based
        
        # Fix 5: Check for groupby column references
        groupby_pattern = r"groupby\('([^']+)'\)"
        groupby_cols = re.findall(groupby_pattern, code)
        for col in groupby_cols:
            if col not in df.columns:
                print(f"Warning: Groupby column '{col}' not found")
                from difflib import get_close_matches
                matches = get_close_matches(col, df.columns, n=1, cutoff=0.6)
                if matches:
                    print(f"  -> Replacing with '{matches[0]}'")
                    code = code.replace(f"groupby('{col}')", f"groupby('{matches[0]}')")
                else:
                    return None
        
        return code
