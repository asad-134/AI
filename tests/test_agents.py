"""
Agent Tests
Tests for AI agents
"""

import pytest
import pandas as pd
from agents.data_cleaning_agent import DataCleaningAgent
from agents.analysis_agent import AnalysisAgent
from agents.orchestrator_agent import OrchestratorAgent


@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe for testing"""
    return pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', None, 'Eve'],
        'age': [25, 30, 35, 40, 45],
        'salary': [50000, 60000, None, 80000, 90000],
        'department': ['Sales', 'IT', 'Sales', 'IT', 'HR']
    })


def test_data_cleaning_agent(sample_dataframe):
    """Test data cleaning agent"""
    agent = DataCleaningAgent()
    result = agent.execute(sample_dataframe)
    
    assert result is not None
    assert 'cleaned_data' in result
    assert 'report' in result
    assert isinstance(result['cleaned_data'], pd.DataFrame)


def test_analysis_agent(sample_dataframe):
    """Test analysis agent"""
    agent = AnalysisAgent()
    result = agent.execute(sample_dataframe, "Show me average salary by department")
    
    assert result is not None
    assert 'analysis_plan' in result
    assert 'results' in result
    assert 'insights' in result


def test_orchestrator_agent(sample_dataframe):
    """Test orchestrator agent"""
    agent = OrchestratorAgent()
    result = agent.execute(sample_dataframe, "Show salary distribution", skip_cleaning=True)
    
    assert result is not None
    assert 'status' in result
    assert 'steps' in result


if __name__ == "__main__":
    pytest.main([__file__])
