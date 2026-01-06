"""
Test script specifically for bar chart functionality
"""
import pandas as pd
import sys

print("Testing Bar Chart Generation...")
print("=" * 50)

# Create sample data similar to ifood dataset
data = {
    'education': ['Graduation', 'PhD', 'Master', 'Basic', 'Graduation', 'PhD'],
    'Income': [50000, 80000, 60000, 30000, 55000, 90000],
    'MntTotal': [500, 800, 600, 200, 550, 900],
    'AcceptedCmp1': [0, 1, 0, 0, 1, 1],
    'AcceptedCmp2': [0, 0, 1, 0, 0, 1],
    'AcceptedCmp3': [0, 1, 0, 0, 1, 0],
    'AcceptedCmp4': [1, 0, 1, 0, 1, 1],
    'AcceptedCmp5': [0, 1, 0, 1, 0, 1],
    'Response': [0, 1, 0, 0, 1, 1]
}
df = pd.DataFrame(data)

print(f"Test DataFrame shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print()

# Test 1: Campaign Acceptance Rates
print("Test 1: Campaign Acceptance Rates")
print("-" * 50)
from visualization_agent import VisualizationAgent

viz_agent = VisualizationAgent()
code, chart_type = viz_agent.create_visualization_from_prompt(
    "Show me campaign acceptance rates",
    df
)

print(f"Chart type: {chart_type}")
print(f"Generated code length: {len(code)} chars")
print("\nGenerated code:")
print(code)
print()

# Try to execute it
try:
    fig = viz_agent.execute_visualization_code(code, df)
    print("✅ Execution successful!")
    print(f"Figure type: {type(fig)}")
except Exception as e:
    print(f"❌ Execution failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)

# Test 2: Spending by Education
print("\nTest 2: Spending by Education")
print("-" * 50)

code2, chart_type2 = viz_agent.create_visualization_from_prompt(
    "Average spending by education level",
    df
)

print(f"Chart type: {chart_type2}")
print(f"Generated code length: {len(code2)} chars")

try:
    fig2 = viz_agent.execute_visualization_code(code2, df)
    print("✅ Execution successful!")
except Exception as e:
    print(f"❌ Execution failed: {e}")

print("\n" + "=" * 50)
print("Tests completed!")
