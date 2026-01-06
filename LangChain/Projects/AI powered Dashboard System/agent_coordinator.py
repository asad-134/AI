"""
Agent Coordinator - Manages interaction between agents and Ollama LLM
Handles prompt engineering and agent orchestration
"""

import json
from typing import Dict, Any, Optional
import pandas as pd


class AgentCoordinator:
    """
    Coordinates between Data Architect, Visualization Agent, and Ollama LLM
    """
    
    def __init__(self, model_name: str = "mistral:7b"):
        self.model_name = model_name
        self.ollama_available = False
        
        # Try to import and initialize Ollama
        try:
            import ollama
            self.ollama = ollama
            # Test connection
            self.ollama.list()
            self.ollama_available = True
        except Exception as e:
            print(f"⚠️ Ollama not available: {e}")
            print("Falling back to rule-based visualization generation")
            self.ollama = None
    
    def enhance_prompt_with_context(self, user_prompt: str, df: pd.DataFrame) -> str:
        """
        Enhances user prompt with dataset context for better LLM understanding
        """
        # Get column information
        columns_info = self._get_columns_context(df)
        
        enhanced_prompt = f"""
You are a Senior Marketing & Financial Analyst creating data visualizations.

DATASET CONTEXT:
{columns_info}

USER REQUEST:
{user_prompt}

TASK:
Generate Python code using Plotly to create the requested visualization.
The code should:
1. Use the variable 'df' which contains the dataframe
2. Create a variable called 'fig' with the Plotly figure
3. Use template='plotly_dark' for consistent styling
4. Include proper axis labels and titles
5. Be executable without any imports (they're already imported)

Return ONLY the Python code, no explanations.
"""
        return enhanced_prompt
    
    def _get_columns_context(self, df: pd.DataFrame) -> str:
        """Creates a readable summary of available columns"""
        column_groups = {
            'Demographics': [],
            'Spending': [],
            'Campaigns': [],
            'Family': [],
            'Behavior': [],
            'Other': []
        }
        
        for col in df.columns:
            if col.startswith('education_') or col.startswith('marital_') or col in ['Age', 'Income']:
                column_groups['Demographics'].append(col)
            elif col.startswith('Mnt'):
                column_groups['Spending'].append(col)
            elif 'Cmp' in col or col == 'Response':
                column_groups['Campaigns'].append(col)
            elif 'home' in col.lower():
                column_groups['Family'].append(col)
            elif any(x in col for x in ['Web', 'Recency', 'Customer', 'Purchases']):
                column_groups['Behavior'].append(col)
            else:
                column_groups['Other'].append(col)
        
        context = []
        for group, cols in column_groups.items():
            if cols:
                context.append(f"{group}: {', '.join(cols)}")
        
        return "\n".join(context)
    
    def query_ollama(self, prompt: str, temperature: float = 0.3) -> str:
        """
        Sends prompt to Ollama and returns response
        """
        if not self.ollama_available:
            return None
        
        try:
            response = self.ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': temperature,
                    'top_p': 0.9,
                    'num_predict': 1000
                }
            )
            
            return response['response']
        
        except Exception as e:
            print(f"Error querying Ollama: {e}")
            return None
    
    def extract_code_from_response(self, response: str) -> str:
        """
        Extracts Python code from LLM response
        Handles various code fence formats
        """
        if not response:
            return None
        
        # Look for code blocks
        import re
        
        # Try to find Python code blocks
        patterns = [
            r'```python\n(.*?)```',
            r'```\n(.*?)```',
            r'`([^`]+)`'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response, re.DOTALL)
            if matches:
                return matches[0].strip()
        
        # If no code blocks found, try to extract any code-like content
        lines = response.split('\n')
        code_lines = []
        in_code = False
        
        for line in lines:
            # Detect code by looking for common Python patterns
            if any(keyword in line for keyword in ['fig =', 'px.', 'go.', 'df[', 'import']):
                in_code = True
            
            if in_code:
                code_lines.append(line)
        
        if code_lines:
            return '\n'.join(code_lines)
        
        return response.strip()
    
    def generate_visualization_code(self, user_prompt: str, df: pd.DataFrame, 
                                   use_ollama: bool = True) -> tuple:
        """
        Main method to generate visualization code
        Returns: (code, method_used)
        method_used: 'ollama' or 'rule-based'
        """
        if use_ollama and self.ollama_available:
            # Try Ollama first
            enhanced_prompt = self.enhance_prompt_with_context(user_prompt, df)
            response = self.query_ollama(enhanced_prompt)
            
            if response:
                code = self.extract_code_from_response(response)
                if code and 'fig' in code:
                    # Validate the code has correct syntax before returning
                    if self._validate_code_syntax(code):
                        return code, 'ollama'
                    else:
                        print("Warning: LLM generated invalid code, falling back to rule-based")
        
        # Fallback to rule-based (Visualization Agent)
        from visualization_agent import VisualizationAgent
        viz_agent = VisualizationAgent()
        code, chart_type = viz_agent.create_visualization_from_prompt(user_prompt, df)
        
        return code, 'rule-based'
    
    def _validate_code_syntax(self, code: str) -> bool:
        """
        Quick validation of generated code syntax
        """
        try:
            # Check for common syntax errors
            compile(code, '<string>', 'exec')
            
            # Check for invalid patterns
            invalid_patterns = [
                r"marker\s*=\s*\{[^d]",  # marker={...} instead of marker=dict(...)
                r"x\s*=\s*'[^']+'\s*,",  # x='column' instead of x=df['column'] in go.Figure
                r"go\.Layout\(",  # Layout in data parameter
            ]
            
            import re
            for pattern in invalid_patterns:
                if re.search(pattern, code):
                    return False
            
            return True
        except SyntaxError:
            return False
        
        prompt = f"""
{summary}

Question: {question}

Provide a concise, insightful analysis based on the data summary above.
Focus on actionable insights for business decision-making.
"""
        
        response = self.query_ollama(prompt, temperature=0.5)
        return response if response else "Unable to generate analysis"
    
    def suggest_visualizations(self, df: pd.DataFrame) -> list:
        """
        Suggests relevant visualizations based on dataset characteristics
        """
        suggestions = []
        
        # Check what columns are available
        has_spending = any(col.startswith('Mnt') for col in df.columns)
        has_campaigns = any('Cmp' in col or col == 'Response' for col in df.columns)
        has_demographics = 'Age' in df.columns or 'Income' in df.columns
        has_education = any(col.startswith('education_') for col in df.columns)
        
        if has_campaigns:
            suggestions.append({
                'title': 'Campaign Success Overview',
                'prompt': 'Calculate the conversion rate using the Response column and create a KPI card',
                'category': 'Campaigns'
            })
        
        if has_spending and has_education:
            suggestions.append({
                'title': 'Spending by Education',
                'prompt': 'Compare the average MntTotal across all education categories. Sort descending',
                'category': 'Spending'
            })
        
        if has_spending and has_demographics:
            suggestions.append({
                'title': 'Income vs Spending',
                'prompt': 'Plot Income vs MntTotal with a scatter plot',
                'category': 'Demographics'
            })
        
        if has_spending:
            suggestions.append({
                'title': 'Spending Correlation',
                'prompt': 'Show a correlation heatmap between Income, Recency, MntWines, and NumWebVisitsMonth',
                'category': 'Analysis'
            })
        
        return suggestions
    
    def get_model_status(self) -> Dict[str, Any]:
        """
        Returns status of Ollama connection and model
        """
        status = {
            'ollama_available': self.ollama_available,
            'model_name': self.model_name,
            'fallback_mode': 'rule-based visualization'
        }
        
        if self.ollama_available:
            try:
                models = self.ollama.list()
                status['available_models'] = [m['name'] for m in models.get('models', [])]
            except:
                status['available_models'] = []
        
        return status
