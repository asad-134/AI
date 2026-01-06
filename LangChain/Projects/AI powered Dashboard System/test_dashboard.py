"""
Test Suite for Multi-Agent Dashboard
Run with: python test_dashboard.py
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Import our modules
try:
    from data_architect import DataArchitect
    from visualization_agent import VisualizationAgent
    from agent_coordinator import AgentCoordinator
    import dashboard_templates as templates
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the correct directory")
    sys.exit(1)


def print_test_header(test_name):
    """Print formatted test header"""
    print("\n" + "="*60)
    print(f"TEST: {test_name}")
    print("="*60)


def print_result(passed, message=""):
    """Print test result"""
    if passed:
        print(f"✅ PASSED {message}")
    else:
        print(f"❌ FAILED {message}")
    return passed


def create_test_dataframe():
    """Create a sample test dataframe"""
    np.random.seed(42)
    n = 100
    
    df = pd.DataFrame({
        'Income': np.random.normal(50000, 15000, n),
        'Age': np.random.randint(18, 80, n),
        'MntWines': np.random.randint(0, 1000, n),
        'MntMeatProducts': np.random.randint(0, 800, n),
        'MntFishProducts': np.random.randint(0, 500, n),
        'MntFruits': np.random.randint(0, 300, n),
        'MntSweetProducts': np.random.randint(0, 300, n),
        'MntGoldProds': np.random.randint(0, 400, n),
        'NumWebVisitsMonth': np.random.randint(0, 20, n),
        'Recency': np.random.randint(0, 100, n),
        'Response': np.random.choice([0, 1], n),
        'AcceptedCmp1': np.random.choice([0, 1], n),
        'AcceptedCmp2': np.random.choice([0, 1], n),
        'Kidhome': np.random.choice([0, 1, 2], n),
        'Teenhome': np.random.choice([0, 1, 2], n),
        'education_Graduation': np.random.choice([0, 1], n),
        'education_Master': np.random.choice([0, 1], n),
        'education_PhD': np.random.choice([0, 1], n),
        'marital_Married': np.random.choice([0, 1], n),
        'marital_Single': np.random.choice([0, 1], n),
    })
    
    # Add some missing values
    df.loc[df.sample(10).index, 'Income'] = np.nan
    df.loc[df.sample(5).index, 'Age'] = np.nan
    
    return df


def test_data_architect():
    """Test Data Architect functionality"""
    print_test_header("Data Architect")
    
    all_passed = True
    
    # Test 1: Basic initialization
    try:
        architect = DataArchitect()
        all_passed &= print_result(True, "- Initialization")
    except Exception as e:
        all_passed &= print_result(False, f"- Initialization: {e}")
        return False
    
    # Test 2: Data cleaning
    try:
        df = create_test_dataframe()
        original_rows = len(df)
        missing_before = df['Income'].isnull().sum()
        
        df_clean = architect.clean_data(df)
        
        # Check no rows dropped
        all_passed &= print_result(
            len(df_clean) == original_rows,
            f"- No rows dropped ({len(df_clean)} == {original_rows})"
        )
        
        # Check Income imputed
        missing_after = df_clean['Income'].isnull().sum()
        all_passed &= print_result(
            missing_after < missing_before,
            f"- Income imputation ({missing_before} → {missing_after})"
        )
        
        # Check aggregates created
        all_passed &= print_result(
            'MntTotal' in df_clean.columns,
            "- MntTotal created"
        )
        
        all_passed &= print_result(
            'MntRegularProds' in df_clean.columns,
            "- MntRegularProds created"
        )
        
    except Exception as e:
        all_passed &= print_result(False, f"- Data cleaning: {e}")
    
    # Test 3: Cleaning report
    try:
        report = architect.get_cleaning_report()
        all_passed &= print_result(
            len(report) > 0,
            f"- Cleaning report generated ({len(report)} chars)"
        )
    except Exception as e:
        all_passed &= print_result(False, f"- Cleaning report: {e}")
    
    return all_passed


def test_visualization_agent():
    """Test Visualization Agent functionality"""
    print_test_header("Visualization Agent")
    
    all_passed = True
    df = create_test_dataframe()
    
    # Test 1: Initialization
    try:
        agent = VisualizationAgent()
        all_passed &= print_result(True, "- Initialization")
    except Exception as e:
        all_passed &= print_result(False, f"- Initialization: {e}")
        return False
    
    # Test 2: Chart type detection
    try:
        test_cases = [
            ("Show me a KPI", "kpi"),
            ("Compare with bar chart", "bar"),
            ("Scatter plot of X vs Y", "scatter"),
            ("Correlation heatmap", "heatmap"),
            ("Create a treemap", "treemap")
        ]
        
        for prompt, expected in test_cases:
            detected = agent._detect_chart_type(prompt)
            all_passed &= print_result(
                detected == expected,
                f"- Chart type: '{prompt[:20]}...' → {detected}"
            )
    except Exception as e:
        all_passed &= print_result(False, f"- Chart type detection: {e}")
    
    # Test 3: Column extraction
    try:
        prompt = "Show Income vs MntTotal colored by Age"
        columns = agent._extract_columns(prompt, df)
        all_passed &= print_result(
            'Income' in columns and 'MntTotal' not in columns,  # MntTotal not in test df
            f"- Column extraction: found {columns}"
        )
    except Exception as e:
        all_passed &= print_result(False, f"- Column extraction: {e}")
    
    # Test 4: Code generation
    try:
        prompt = "Show Income vs Age scatter plot"
        code, chart_type = agent.create_visualization_from_prompt(prompt, df)
        
        all_passed &= print_result(
            'fig' in code and 'px.' in code,
            f"- Code generation ({len(code)} chars)"
        )
    except Exception as e:
        all_passed &= print_result(False, f"- Code generation: {e}")
    
    # Test 5: Code execution
    try:
        code = """
fig = px.scatter(df, x='Income', y='Age', title='Test Chart', template='plotly_dark')
"""
        fig = agent.execute_visualization_code(code, df)
        all_passed &= print_result(
            fig is not None,
            "- Code execution"
        )
    except Exception as e:
        all_passed &= print_result(False, f"- Code execution: {e}")
    
    return all_passed


def test_agent_coordinator():
    """Test Agent Coordinator functionality"""
    print_test_header("Agent Coordinator")
    
    all_passed = True
    df = create_test_dataframe()
    
    # Test 1: Initialization
    try:
        coordinator = AgentCoordinator()
        all_passed &= print_result(True, "- Initialization")
    except Exception as e:
        all_passed &= print_result(False, f"- Initialization: {e}")
        return False
    
    # Test 2: Model status
    try:
        status = coordinator.get_model_status()
        all_passed &= print_result(
            'ollama_available' in status,
            f"- Model status (Ollama: {status.get('ollama_available', False)})"
        )
    except Exception as e:
        all_passed &= print_result(False, f"- Model status: {e}")
    
    # Test 3: Prompt enhancement
    try:
        enhanced = coordinator.enhance_prompt_with_context(
            "Show me a chart", df
        )
        all_passed &= print_result(
            len(enhanced) > 50 and 'DATASET CONTEXT' in enhanced,
            f"- Prompt enhancement ({len(enhanced)} chars)"
        )
    except Exception as e:
        all_passed &= print_result(False, f"- Prompt enhancement: {e}")
    
    # Test 4: Visualization generation (rule-based fallback)
    try:
        code, method = coordinator.generate_visualization_code(
            "Show Income vs Age scatter plot",
            df,
            use_ollama=False  # Force rule-based
        )
        
        all_passed &= print_result(
            code is not None and method == 'rule-based',
            f"- Rule-based generation (method: {method})"
        )
    except Exception as e:
        all_passed &= print_result(False, f"- Visualization generation: {e}")
    
    # Test 5: Ollama code extraction
    try:
        test_response = """
Here's the code:
```python
fig = px.bar(df, x='Age', y='Income')
```
That should work!
"""
        code = coordinator.extract_code_from_response(test_response)
        all_passed &= print_result(
            code is not None and 'fig' in code,
            "- Code extraction from LLM response"
        )
    except Exception as e:
        all_passed &= print_result(False, f"- Code extraction: {e}")
    
    return all_passed


def test_dashboard_templates():
    """Test Dashboard Templates functionality"""
    print_test_header("Dashboard Templates")
    
    all_passed = True
    
    # Test 1: Dashboard list
    try:
        dashboards = templates.get_all_dashboard_names()
        all_passed &= print_result(
            len(dashboards) >= 5,
            f"- Found {len(dashboards)} dashboards"
        )
        
        for name in dashboards:
            print(f"  • {name}")
    except Exception as e:
        all_passed &= print_result(False, f"- Dashboard list: {e}")
    
    # Test 2: Get specific dashboard
    try:
        dashboard = templates.get_dashboard_by_name("Campaign Success & Engagement")
        all_passed &= print_result(
            dashboard is not None and 'prompts' in dashboard,
            "- Get specific dashboard"
        )
    except Exception as e:
        all_passed &= print_result(False, f"- Get dashboard: {e}")
    
    # Test 3: Get prompts
    try:
        prompts = templates.get_prompts_for_dashboard("Campaign Success & Engagement")
        all_passed &= print_result(
            len(prompts) > 0,
            f"- Dashboard prompts ({len(prompts)} prompts)"
        )
    except Exception as e:
        all_passed &= print_result(False, f"- Get prompts: {e}")
    
    # Test 4: Analysis prompts
    try:
        analysis_types = templates.get_all_analysis_types()
        all_passed &= print_result(
            len(analysis_types) > 0,
            f"- Analysis types ({len(analysis_types)} types)"
        )
    except Exception as e:
        all_passed &= print_result(False, f"- Analysis types: {e}")
    
    return all_passed


def test_file_structure():
    """Test that all required files exist"""
    print_test_header("File Structure")
    
    all_passed = True
    
    required_files = [
        'app.py',
        'data_architect.py',
        'visualization_agent.py',
        'agent_coordinator.py',
        'dashboard_templates.py',
        'requirements.txt',
        'README.md',
        'ARCHITECTURE.md',
        'QUICKSTART.md'
    ]
    
    for filename in required_files:
        exists = Path(filename).exists()
        all_passed &= print_result(
            exists,
            f"- {filename}"
        )
    
    # Check for dataset (optional)
    if Path('ifood_df.csv').exists():
        print_result(True, "- ifood_df.csv (optional)")
    else:
        print("⚠️  OPTIONAL - ifood_df.csv not found (you can upload your own)")
    
    return all_passed


def test_imports():
    """Test that all required packages are installed"""
    print_test_header("Package Imports")
    
    all_passed = True
    
    packages = {
        'streamlit': 'streamlit',
        'pandas': 'pandas',
        'plotly': 'plotly',
        'numpy': 'numpy',
        'ollama': 'ollama'
    }
    
    for package_name, import_name in packages.items():
        try:
            __import__(import_name)
            all_passed &= print_result(True, f"- {package_name}")
        except ImportError:
            all_passed &= print_result(False, f"- {package_name} (not installed)")
    
    return all_passed


def run_integration_test():
    """Test complete workflow end-to-end"""
    print_test_header("Integration Test (End-to-End)")
    
    all_passed = True
    
    try:
        # Step 1: Create test data
        print("Step 1: Creating test data...")
        df = create_test_dataframe()
        all_passed &= print_result(True, "- Test data created")
        
        # Step 2: Clean data
        print("Step 2: Cleaning data...")
        architect = DataArchitect()
        df_clean = architect.clean_data(df)
        all_passed &= print_result(
            len(df_clean) == len(df),
            "- Data cleaned"
        )
        
        # Step 3: Generate visualization
        print("Step 3: Generating visualization...")
        coordinator = AgentCoordinator()
        code, method = coordinator.generate_visualization_code(
            "Show Income vs Age scatter plot",
            df_clean,
            use_ollama=False
        )
        all_passed &= print_result(
            code is not None,
            f"- Code generated using {method}"
        )
        
        # Step 4: Execute visualization
        print("Step 4: Executing visualization...")
        viz_agent = VisualizationAgent()
        fig = viz_agent.execute_visualization_code(code, df_clean)
        all_passed &= print_result(
            fig is not None,
            "- Figure created"
        )
        
        print("\n✅ Complete workflow successful!")
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        all_passed = False
    
    return all_passed


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("MULTI-AGENT DASHBOARD TEST SUITE")
    print("="*60)
    
    results = {}
    
    # Run individual tests
    results['File Structure'] = test_file_structure()
    results['Package Imports'] = test_imports()
    results['Data Architect'] = test_data_architect()
    results['Visualization Agent'] = test_visualization_agent()
    results['Agent Coordinator'] = test_agent_coordinator()
    results['Dashboard Templates'] = test_dashboard_templates()
    results['Integration Test'] = run_integration_test()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    print("="*60)
    print(f"TOTAL: {passed}/{total} test suites passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All tests passed! Your dashboard is ready to use.")
        print("\nRun the dashboard with:")
        print("  streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("  1. Install missing packages: pip install -r requirements.txt")
        print("  2. Ensure Ollama is installed: ollama --version")
        print("  3. Check you're in the correct directory")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
