"""
Base Agent Class
Provides common functionality for all agents
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os


class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, model_name: str = "gemini-2.0-flash-exp", temperature: float = 0.7):
        """
        Initialize the base agent
        
        Args:
            model_name: Name of the Gemini model to use
            temperature: Temperature for model responses
        """
        self.model_name = model_name
        self.temperature = temperature
        self.llm = self._initialize_llm()
        
    def _initialize_llm(self) -> ChatGoogleGenerativeAI:
        """Initialize the Gemini LLM"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            google_api_key=api_key
        )
    
    def create_chain(self, prompt_template: str):
        """
        Create a LangChain chain with the given prompt template
        
        Args:
            prompt_template: The prompt template string
            
        Returns:
            Configured chain using modern LCEL syntax
        """
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=self._extract_variables(prompt_template)
        )
        return prompt | self.llm
    
    def _extract_variables(self, template: str) -> list:
        """Extract variable names from a prompt template"""
        import re
        return re.findall(r'\{(\w+)\}', template)
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the agent's main task
        Must be implemented by subclasses
        """
        pass
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message (can be extended for proper logging)"""
        print(f"[{level}] {self.__class__.__name__}: {message}")
