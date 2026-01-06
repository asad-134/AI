"""
Orchestrator Agent
Coordinates all other agents and manages the workflow
"""

from typing import Dict, Any
import pandas as pd
from .base_agent import BaseAgent
from .data_cleaning_agent import DataCleaningAgent
from .analysis_agent import AnalysisAgent
from .visualization_agent import VisualizationAgent


class OrchestratorAgent(BaseAgent):
    """Main agent that coordinates all other agents"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cleaning_agent = DataCleaningAgent(**kwargs)
        self.analysis_agent = AnalysisAgent(**kwargs)
        self.visualization_agent = VisualizationAgent(**kwargs)
        
        self.intent_prompt = """
        You are a user intent classifier. Analyze the user's query and determine their intent:
        
        User Query: {user_query}
        
        Available Columns: {columns}
        
        Classify the intent and provide a JSON response with:
        1. intent_type: primary intent (visualization, analysis, comparison, trend, distribution)
        2. entities: key entities mentioned (column names, values, etc.)
        3. action: specific action to perform
        4. confidence: confidence score (0-1)
        
        Response must be valid JSON only.
        """
    
    def execute(self, df: pd.DataFrame, user_query: str, 
                skip_cleaning: bool = False) -> Dict[str, Any]:
        """
        Orchestrate the entire workflow
        
        Args:
            df: Input dataframe
            user_query: User's natural language query
            skip_cleaning: Whether to skip data cleaning (if already cleaned)
            
        Returns:
            Complete results including visualizations
        """
        self.log("Starting orchestration workflow")
        
        workflow_results = {
            "status": "in_progress",
            "steps": []
        }
        
        try:
            # Step 1: Data Cleaning (if needed)
            if not skip_cleaning:
                self.log("Step 1: Data Cleaning")
                cleaning_results = self.cleaning_agent.execute(df)
                cleaned_df = cleaning_results["cleaned_data"]
                workflow_results["steps"].append({
                    "step": "cleaning",
                    "status": "completed",
                    "report": cleaning_results["report"]
                })
            else:
                cleaned_df = df
                workflow_results["steps"].append({
                    "step": "cleaning",
                    "status": "skipped"
                })
            
            # Step 2: Understand user intent
            self.log("Step 2: Understanding user intent")
            intent = self._classify_intent(user_query, cleaned_df.columns.tolist())
            workflow_results["intent"] = intent
            
            # Step 3: Data Analysis
            self.log("Step 3: Analyzing data")
            analysis_results = self.analysis_agent.execute(cleaned_df, user_query)
            workflow_results["steps"].append({
                "step": "analysis",
                "status": "completed",
                "insights": analysis_results["insights"]
            })
            
            # Step 4: Generate Visualizations
            self.log("Step 4: Generating visualizations")
            viz_results = self.visualization_agent.execute(analysis_results, user_query)
            workflow_results["steps"].append({
                "step": "visualization",
                "status": "completed",
                "charts_count": len(viz_results["chart_specifications"])
            })
            
            # Compile final results
            workflow_results.update({
                "status": "completed",
                "cleaned_data": cleaned_df,
                "analysis": analysis_results,
                "visualizations": viz_results,
                "success": True
            })
            
            self.log("Orchestration workflow completed successfully")
            
        except Exception as e:
            self.log(f"Error in orchestration: {str(e)}", "ERROR")
            workflow_results.update({
                "status": "failed",
                "error": str(e),
                "success": False
            })
        
        return workflow_results
    
    def _classify_intent(self, user_query: str, columns: list) -> Dict[str, Any]:
        """Classify user intent"""
        try:
            chain = self.create_chain(self.intent_prompt)
            response = chain.invoke({
                "user_query": user_query,
                "columns": columns
            })
            
            import json
            response_text = response.content if hasattr(response, 'content') else str(response)
            intent = json.loads(response_text)
            return intent
        except Exception as e:
            self.log(f"Error classifying intent: {e}", "WARNING")
            return {
                "intent_type": "visualization",
                "entities": [],
                "action": "create_chart",
                "confidence": 0.5
            }
    
    def process_uploaded_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process an uploaded CSV file
        
        Args:
            file_path: Path to the uploaded file
            
        Returns:
            Processing results
        """
        self.log(f"Processing uploaded file: {file_path}")
        
        try:
            # Read CSV
            df = pd.read_csv(file_path)
            
            # Clean the data
            cleaning_results = self.cleaning_agent.execute(df)
            
            return {
                "success": True,
                "original_shape": df.shape,
                "cleaned_shape": cleaning_results["cleaned_data"].shape,
                "cleaned_data": cleaning_results["cleaned_data"],
                "report": cleaning_results["report"]
            }
            
        except Exception as e:
            self.log(f"Error processing file: {str(e)}", "ERROR")
            return {
                "success": False,
                "error": str(e)
            }
