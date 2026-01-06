"""Quick test to verify visualization fixes"""

import pandas as pd
import numpy as np
from visualization_agent import VisualizationAgent

# Create test data
np.random.seed(42)
df = pd.DataFrame({
    'Income': np.random.normal(50000, 15000, 100),
    'Age': np.random.randint(18, 80, 100),
    'MntTotal': np.random.randint(0, 2000, 100),
    'Recency': np.random.randint(0, 100, 100),
    'education_Graduation': np.random.choice([0, 1], 100)
})

print("Creating Visualization Agent...")
agent = VisualizationAgent()

# Test 1: Bar chart
print("\n✅ Test 1: Bar chart generation")
try:
    code, chart_type = agent.create_visualization_from_prompt(
        "Compare average MntTotal by education", df
    )
    print(f"  Chart type detected: {chart_type}")
    print(f"  Code generated: {len(code)} chars")
    
    fig = agent.execute_visualization_code(code, df)
    print(f"  Figure created: {fig is not None}")
    if fig:
        print("  ✓ Bar chart works!")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 2: Scatter plot
print("\n✅ Test 2: Scatter plot generation")
try:
    code, chart_type = agent.create_visualization_from_prompt(
        "Show Income vs MntTotal scatter plot", df
    )
    print(f"  Chart type detected: {chart_type}")
    fig = agent.execute_visualization_code(code, df)
    print(f"  Figure created: {fig is not None}")
    if fig:
        print("  ✓ Scatter plot works!")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 3: KPI
print("\n✅ Test 3: KPI generation")
try:
    code, chart_type = agent.create_visualization_from_prompt(
        "Show average income as KPI", df
    )
    print(f"  Chart type detected: {chart_type}")
    fig = agent.execute_visualization_code(code, df)
    print(f"  Figure created: {fig is not None}")
    if fig:
        print("  ✓ KPI works!")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 4: Heatmap
print("\n✅ Test 4: Heatmap generation")
try:
    code, chart_type = agent.create_visualization_from_prompt(
        "Correlation heatmap of numeric columns", df
    )
    print(f"  Chart type detected: {chart_type}")
    fig = agent.execute_visualization_code(code, df)
    print(f"  Figure created: {fig is not None}")
    if fig:
        print("  ✓ Heatmap works!")
except Exception as e:
    print(f"  ✗ Error: {e}")

print("\n" + "="*50)
print("All tests completed!")
print("="*50)
