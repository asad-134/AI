# Step-by-Step Architectural Plan
## Multi-Agent Dashboard with Ollama Mistral 7B

---

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Architectural Components](#architectural-components)
3. [Agent Specifications](#agent-specifications)
4. [Execution Flow](#execution-flow)
5. [Implementation Steps](#implementation-steps)
6. [Prompt Engineering](#prompt-engineering)
7. [Testing Strategy](#testing-strategy)

---

## 🎯 System Overview

### Purpose
Build an intelligent analytics dashboard that uses multiple AI agents to:
- Clean and prepare customer data
- Generate visualizations from natural language
- Provide business insights
- Support iterative, side-by-side chart comparison

### Technology Stack
- **Frontend:** Streamlit (Python web framework)
- **LLM:** Ollama Mistral 7B (Local inference)
- **Visualization:** Plotly Express/Graph Objects
- **Data Processing:** Pandas, NumPy
- **Agent Framework:** Custom multi-agent system

### Design Philosophy
**Context-Task-Formatting (CTF) Framework**

Every agent operation follows this pattern:
```
Context: What information is available?
Task: What needs to be done?
Formatting: How should the output be structured?
```

---

## 🏗️ Architectural Components

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│                     (Streamlit - app.py)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │   Upload     │  │ Visualization │  │   Dashboard          │ │
│  │   Section    │  │   Creator     │  │   Gallery            │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SESSION STATE MANAGER                         │
│  • df_clean (cleaned dataframe)                                 │
│  • history_charts (list of figure objects)                      │
│  • coordinator (Agent Coordinator instance)                     │
│  • cleaning_report (data cleaning log)                          │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT COORDINATOR                             │
│              (agent_coordinator.py)                              │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Prompt Enhancement Engine                                │  │
│  │ • Add dataset context to user prompts                    │  │
│  │ • Inject CTF framework instructions                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Ollama Interface                                         │  │
│  │ • Connect to local Mistral 7B                            │  │
│  │ • Send enhanced prompts                                  │  │
│  │ • Extract Python code from responses                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Fallback Manager                                         │  │
│  │ • Detect Ollama failures                                 │  │
│  │ • Switch to rule-based generation                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────┬───────────────────────┬──────────────────────┬─────┘
             │                       │                      │
             ▼                       ▼                      ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌────────────────┐
│   DATA ARCHITECT    │  │ VISUALIZATION AGENT │  │ OLLAMA LLM     │
│ (data_architect.py) │  │(visualization_agent)│  │ (Mistral 7B)   │
│                     │  │                     │  │                │
│ • Median Imputation │  │ • Senior Analyst   │  │ • Local Model  │
│ • Mode Imputation   │  │   Persona          │  │ • Code         │
│ • Feature Eng.      │  │ • Chart Types      │  │   Generation   │
│ • Aggregates        │  │ • Plotly Code Gen  │  │ • Analysis     │
└─────────────────────┘  └─────────────────────┘  └────────────────┘
             │                       │
             ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                                │
│  • Raw CSV → Cleaned DataFrame → Visualizations                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Agent Specifications

### 1. Data Architect Agent

**File:** `data_architect.py`

**Responsibility:** Transform raw data into analysis-ready format

**CTF Implementation:**

```python
# Context
Context: Dataset contains customer demographics and spending data
         Income column has missing values
         Education levels are one-hot encoded (education_*)
         
# Task  
Task: Clean data without dropping any rows
      Impute Income using median grouped by education
      Impute categorical columns using mode
      Create spending aggregates

# Formatting
Formatting: Return cleaned DataFrame with same row count
           Add MntTotal, MntRegularProds, MntGoldProds columns
           Generate cleaning report string
```

**Key Methods:**

1. **`clean_data(df) -> df`**
   - Entry point for data cleaning pipeline
   - Calls all sub-cleaning methods in sequence
   - Returns cleaned DataFrame

2. **`_impute_income_by_education(df)`**
   ```python
   For each education_* column where value = 1:
       Find median income for that education group
       Fill missing Income with that median
   ```

3. **`_impute_categorical_with_mode(df)`**
   ```python
   For each categorical/binary column:
       Find most frequent value (mode)
       Fill missing values with mode
   ```

4. **`_engineer_mnt_features(df)`**
   ```python
   For each Mnt* column:
       Convert to numeric (coerce errors)
       Fill NaN with 0
   ```

5. **`_create_spending_aggregates(df)`**
   ```python
   MntTotal = Sum of all Mnt* columns
   MntRegularProds = Sum excluding MntGoldProds
   MntGoldProds = Already exists or 0
   ```

**Output:**
- Cleaned DataFrame
- Text report of all operations performed

---

### 2. Visualization Agent

**File:** `visualization_agent.py`

**Responsibility:** Generate Plotly visualizations from natural language

**Persona:** Senior Marketing & Financial Analyst

**CTF Implementation:**

```python
# Context
Context: Available columns in dataset (Demographics, Spending, Campaigns)
         User's natural language request
         Chart type detection from keywords
         
# Task
Task: Parse user prompt to identify:
      - Chart type (KPI, Bar, Scatter, Heatmap, Treemap)
      - Columns to use
      - Aggregation method (mean, sum, count)
      - Sorting requirements
      - Color conditions
      
# Formatting
Formatting: Generate executable Python code
           Use Plotly Express or Graph Objects
           Apply plotly_dark theme
           Store result in 'fig' variable
           No import statements (already imported)
```

**Key Methods:**

1. **`parse_visualization_request(prompt, df)`**
   - Extracts chart type, columns, aggregation from prompt
   - Returns structured request dictionary

2. **`_detect_chart_type(prompt)`**
   ```python
   Keywords mapping:
   'kpi' or 'metric' -> KPI Card
   'bar' or 'compare' -> Bar Chart
   'scatter' or 'plot' -> Scatter Plot
   'heatmap' or 'correlation' -> Heatmap
   'treemap' or 'hierarchical' -> Treemap
   ```

3. **`_extract_columns(prompt, df)`**
   - Finds column names mentioned in prompt
   - Returns list of matching columns

4. **`generate_*_code()` methods**
   - `generate_kpi_code()` - KPI cards with conditional colors
   - `generate_bar_chart_code()` - Aggregated bar charts
   - `generate_scatter_code()` - Scatter plots with color coding
   - `generate_heatmap_code()` - Correlation matrices
   - `generate_treemap_code()` - Hierarchical visualizations

5. **`execute_visualization_code(code, df)`**
   - Safely executes generated Python code
   - Returns Plotly figure object
   - Handles errors gracefully

**Example Code Generation:**

```python
# Input: "Show Income vs MntTotal colored by education"
# Output:
fig = px.scatter(
    df,
    x='Income',
    y='MntTotal',
    color='education_Graduation',
    title='MntTotal vs Income',
    template='plotly_dark',
    opacity=0.7
)
fig.update_traces(marker=dict(size=8))
fig.update_layout(height=500)
```

---

### 3. Agent Coordinator

**File:** `agent_coordinator.py`

**Responsibility:** Orchestrate LLM and agents, handle fallbacks

**CTF Implementation:**

```python
# Context
Context: User prompt + Dataset column information
         Ollama connection status
         Previous generation method (LLM vs rule-based)
         
# Task
Task: Enhance user prompt with dataset context
      Send to Ollama for code generation
      Extract Python code from LLM response
      Fallback to Visualization Agent if LLM fails
      
# Formatting
Formatting: Return tuple (code_string, method_used)
           Code must be executable with exec()
           Method: 'ollama' or 'rule-based'
```

**Key Methods:**

1. **`__init__(model_name)`**
   - Initialize Ollama connection
   - Test availability
   - Set fallback flag

2. **`enhance_prompt_with_context(prompt, df)`**
   ```python
   Enhanced Prompt = f"""
   You are a Senior Marketing Analyst.
   
   DATASET CONTEXT:
   {columns_by_category}
   
   USER REQUEST:
   {user_prompt}
   
   TASK:
   Generate Plotly code. Use 'df' variable. Create 'fig' variable.
   Use template='plotly_dark'. No imports needed.
   
   Return ONLY executable Python code.
   """
   ```

3. **`query_ollama(prompt)`**
   - Send prompt to Mistral 7B
   - Configure temperature, top_p
   - Return raw response text

4. **`extract_code_from_response(response)`**
   ```python
   # Try multiple extraction patterns:
   1. ```python code ```
   2. ``` code ```
   3. Lines containing 'fig =', 'px.', 'go.'
   4. Return best match
   ```

5. **`generate_visualization_code(prompt, df, use_ollama)`**
   ```python
   if use_ollama and ollama_available:
       code = query_ollama(enhanced_prompt)
       if valid_code:
           return code, 'ollama'
   
   # Fallback
   code = visualization_agent.create_from_prompt(prompt, df)
   return code, 'rule-based'
   ```

6. **`analyze_data_with_llm(df, question)`**
   - Generate data summary
   - Ask Ollama for insights
   - Return analysis text

---

### 4. Dashboard Templates

**File:** `dashboard_templates.py`

**Responsibility:** Pre-built dashboard configurations

**Structure:**

```python
DASHBOARD = {
    'name': 'Dashboard Name',
    'description': 'Purpose description',
    'prompts': [
        {
            'title': 'Chart Title',
            'prompt': 'Natural language prompt',
            'chart_type': 'bar|scatter|heatmap|kpi|treemap'
        }
    ]
}
```

**Available Dashboards:**

1. **Campaign Success & Engagement**
   - Conversion Rate KPI
   - Education vs Spending
   - Spending Drivers Correlation

2. **Family & Spending Habits**
   - Product Type by Children
   - Income-Spending Relationship
   - Revenue by Household Type

3. **Customer Behavior Analysis**
   - Recency vs Spending
   - Web Visits vs Purchases
   - Purchase Channel Comparison

4. **Demographics & Segmentation**
   - Age Distribution
   - Income Distribution
   - Age vs Income Analysis

5. **Product Category Performance**
   - Product Category Comparison
   - Wine Spending Correlation
   - Product Mix Heatmap

---

### 5. UI Orchestrator (Streamlit App)

**File:** `app.py`

**Responsibility:** User interface and session management

**Key Features:**

1. **Session State Management**
   ```python
   st.session_state = {
       'data_loaded': False,
       'df_clean': None,
       'history_charts': [],  # List of figure objects
       'cleaning_report': "",
       'coordinator': AgentCoordinator(),
       'viz_agent': VisualizationAgent()
   }
   ```

2. **Side-by-Side Chart Rendering**
   ```python
   # Render 2 charts per row
   for i in range(0, len(charts), 2):
       cols = st.columns(2)
       
       # First chart
       with cols[0]:
           st.plotly_chart(charts[i]['fig'])
       
       # Second chart (if exists)
       if i + 1 < len(charts):
           with cols[1]:
               st.plotly_chart(charts[i+1]['fig'])
   ```

3. **Persistent Chart History**
   ```python
   # Add new chart to history
   st.session_state.history_charts.append({
       'title': prompt,
       'fig': figure_object,
       'prompt': original_prompt,
       'method': 'ollama' or 'rule-based'
   })
   
   # Charts persist across interactions
   # No loss when new prompt is entered
   ```

4. **Three-Tab Layout**
   - **Tab 1:** Create Visualization (interactive prompt)
   - **Tab 2:** Dashboard Gallery (all charts)
   - **Tab 3:** Data Analysis (LLM insights)

---

## 🔄 Execution Flow

### Complete User Journey

```
┌──────────────────────────────────────────────────────────────────┐
│ STEP 1: Data Upload                                              │
└──────────────────────────────────────────────────────────────────┘
    │
    ├─> User uploads CSV or uses default dataset
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 2: Data Cleaning (Data Architect)                           │
└──────────────────────────────────────────────────────────────────┘
    │
    ├─> Load CSV with pandas
    ├─> Create DataArchitect instance
    ├─> Run clean_data(df)
    │   │
    │   ├─> _impute_income_by_education()
    │   ├─> _impute_categorical_with_mode()
    │   ├─> _engineer_mnt_features()
    │   ├─> _calculate_customer_days()
    │   └─> _create_spending_aggregates()
    │
    ├─> Store df_clean in session_state
    └─> Display cleaning report
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 3: User Enters Visualization Prompt                         │
└──────────────────────────────────────────────────────────────────┘
    │
    ├─> User types: "Show Income vs MntTotal colored by education"
    └─> User clicks "Generate Visualization"
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 4: Agent Coordinator Processes Request                      │
└──────────────────────────────────────────────────────────────────┘
    │
    ├─> Check if Ollama is available
    │
    ├─> If Ollama available:
    │   │
    │   ├─> enhance_prompt_with_context(prompt, df)
    │   ├─> query_ollama(enhanced_prompt)
    │   ├─> extract_code_from_response(response)
    │   │
    │   └─> If valid code extracted:
    │       └─> Return (code, 'ollama')
    │
    ├─> If Ollama unavailable or code invalid:
    │   │
    │   └─> Fallback to Visualization Agent
    │       │
    │       ├─> parse_visualization_request(prompt, df)
    │       ├─> _detect_chart_type() -> 'scatter'
    │       ├─> _extract_columns() -> ['Income', 'MntTotal', 'education_*']
    │       ├─> generate_scatter_code(x, y, color)
    │       │
    │       └─> Return (code, 'rule-based')
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 5: Code Execution (Visualization Agent)                     │
└──────────────────────────────────────────────────────────────────┘
    │
    ├─> execute_visualization_code(code, df_clean)
    │   │
    │   ├─> Create execution environment:
    │   │   {
    │   │       'df': df_clean,
    │   │       'pd': pandas,
    │   │       'px': plotly.express,
    │   │       'go': plotly.graph_objects,
    │   │       'fig': None
    │   │   }
    │   │
    │   ├─> exec(code, exec_globals)
    │   │
    │   └─> Return exec_globals['fig']
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 6: Store in Session State                                   │
└──────────────────────────────────────────────────────────────────┘
    │
    ├─> Append to history_charts:
    │   {
    │       'title': "Income vs MntTotal by Education",
    │       'fig': plotly_figure_object,
    │       'prompt': original_prompt,
    │       'method': 'ollama' or 'rule-based'
    │   }
    │
    └─> st.rerun() to refresh UI
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 7: Render in Gallery (Side-by-Side)                         │
└──────────────────────────────────────────────────────────────────┘
    │
    ├─> Iterate through history_charts in pairs
    │
    ├─> For each pair (i, i+1):
    │   │
    │   ├─> Create st.columns(2)
    │   │
    │   ├─> Render chart[i] in cols[0]
    │   └─> Render chart[i+1] in cols[1]
    │
    └─> Charts persist for entire session
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 8: User Can Continue                                        │
└──────────────────────────────────────────────────────────────────┘
    │
    ├─> Enter new prompt (previous charts stay)
    ├─> Load pre-built dashboard (adds multiple charts)
    ├─> Ask data analysis question
    └─> Clear all charts and start fresh
```

---

## 📝 Implementation Steps

### Phase 1: Setup (10 minutes)

1. **Install Ollama**
   ```powershell
   # Download from ollama.ai
   # Install and run:
   ollama pull mistral:7b
   ollama list  # Verify
   ```

2. **Install Python Dependencies**
   ```powershell
   cd "c:\Users\eduah\Desktop\dashboard 2.0"
   pip install -r requirements.txt
   ```

3. **Verify File Structure**
   ```
   ✓ app.py
   ✓ data_architect.py
   ✓ visualization_agent.py
   ✓ agent_coordinator.py
   ✓ dashboard_templates.py
   ✓ requirements.txt
   ✓ ifood_df.csv
   ```

### Phase 2: Testing Components (20 minutes)

1. **Test Data Architect**
   ```python
   # In Python REPL or notebook:
   from data_architect import DataArchitect
   import pandas as pd
   
   df = pd.read_csv('ifood_df.csv')
   architect = DataArchitect()
   df_clean = architect.clean_data(df)
   print(architect.get_cleaning_report())
   ```

2. **Test Visualization Agent**
   ```python
   from visualization_agent import VisualizationAgent
   
   agent = VisualizationAgent()
   code, chart_type = agent.create_visualization_from_prompt(
       "Show Income vs MntTotal scatter plot", 
       df_clean
   )
   print(code)
   
   fig = agent.execute_visualization_code(code, df_clean)
   fig.show()
   ```

3. **Test Agent Coordinator**
   ```python
   from agent_coordinator import AgentCoordinator
   
   coordinator = AgentCoordinator()
   status = coordinator.get_model_status()
   print(status)
   
   code, method = coordinator.generate_visualization_code(
       "Compare spending by education", 
       df_clean
   )
   print(f"Method used: {method}")
   ```

### Phase 3: Run Application (5 minutes)

1. **Start Streamlit**
   ```powershell
   streamlit run app.py
   ```

2. **Initial Test Flow**
   - Upload ifood_df.csv
   - View cleaning report
   - Try prompt: "Show Income vs MntTotal scatter plot"
   - Verify chart appears
   - Try another prompt
   - Verify both charts are visible side-by-side

3. **Test Pre-built Dashboard**
   - Click "Campaign Success & Engagement" in sidebar
   - Verify all 4 charts load
   - Check side-by-side layout

### Phase 4: Advanced Testing (15 minutes)

1. **Test All Chart Types**
   - KPI: "Calculate conversion rate with Response column"
   - Bar: "Compare MntTotal by education, sort descending"
   - Scatter: "Income vs MntTotal colored by education"
   - Heatmap: "Correlation of Income, Recency, MntWines"
   - Treemap: "MntTotal by marital status"

2. **Test LLM Analysis**
   - Go to "Data Analysis" tab
   - Click "High Value Customers"
   - Verify Ollama generates insights

3. **Test Persistence**
   - Create 5 different charts
   - Navigate between tabs
   - Verify all charts remain visible
   - Delete one chart
   - Verify others persist

---

## 🎯 Prompt Engineering

### For Data Architect

**Persona:** Meticulous Data Engineer

**Sample Internal Prompt:**
```
Context: Income column has 24 missing values
         Education levels: PhD, Master, Graduation, Basic
         
Task: For each missing Income value:
      1. Identify customer's education level
      2. Calculate median Income for that education group
      3. Replace missing value with group median
      
Formatting: Do not drop any rows
           Log each imputation operation
           Return report with before/after statistics
```

### For Visualization Agent

**Persona:** Senior Marketing & Financial Analyst

**Sample Prompt Enhancement:**
```
Original User Prompt:
"Show spending by education"

Enhanced Internal Prompt:
You are a Senior Marketing Analyst creating an executive dashboard.

CONTEXT:
Available columns:
- Demographics: education_Graduation, education_Master, education_PhD, education_Basic
- Spending: MntTotal, MntWines, MntMeatProducts, MntFishProducts

USER REQUEST:
Show spending by education

TASK:
Generate a bar chart comparing average MntTotal across education categories.
Sort bars by spending amount (descending).
Use professional color palette.

FORMATTING:
- Use Plotly Express
- Template: plotly_dark
- X-axis: Education Level
- Y-axis: Average Total Spending ($)
- Title: "Customer Spending by Education Level"
- Sort: Descending by spending

Return ONLY executable Python code. No explanations.
```

### For Ollama LLM

**Temperature Settings:**
- **Code Generation:** 0.3 (low variance, deterministic)
- **Data Analysis:** 0.5-0.7 (creative insights)

**Prompt Structure:**
```
ROLE: {persona}

CONTEXT:
{dataset_info}
{available_columns}

USER REQUEST:
{user_prompt}

TASK:
{specific_task_description}

CONSTRAINTS:
- Use variable 'df' for dataframe
- Create variable 'fig' for Plotly figure
- No imports needed (pre-imported)
- Use template='plotly_dark'
- Executable Python only

FORMATTING:
{output_specifications}

Return ONLY the code. No markdown. No explanations.
```

---

## 🧪 Testing Strategy

### Unit Tests

1. **Data Architect Tests**
   ```python
   def test_income_imputation():
       df = create_test_df_with_missing_income()
       architect = DataArchitect()
       df_clean = architect._impute_income_by_education(df)
       assert df_clean['Income'].isnull().sum() == 0
   
   def test_categorical_imputation():
       # Test mode imputation
       pass
   
   def test_feature_engineering():
       # Test Mnt column conversion
       pass
   ```

2. **Visualization Agent Tests**
   ```python
   def test_chart_type_detection():
       agent = VisualizationAgent()
       assert agent._detect_chart_type("Show KPI") == 'kpi'
       assert agent._detect_chart_type("Compare with bar") == 'bar'
   
   def test_column_extraction():
       # Test column name parsing
       pass
   
   def test_code_execution():
       # Test safe code execution
       pass
   ```

3. **Agent Coordinator Tests**
   ```python
   def test_ollama_connection():
       coordinator = AgentCoordinator()
       status = coordinator.get_model_status()
       assert 'ollama_available' in status
   
   def test_code_extraction():
       # Test code parsing from LLM response
       pass
   
   def test_fallback_mechanism():
       # Test rule-based fallback
       pass
   ```

### Integration Tests

1. **End-to-End Flow**
   ```python
   def test_complete_workflow():
       # Load data
       df = pd.read_csv('test_data.csv')
       
       # Clean
       architect = DataArchitect()
       df_clean = architect.clean_data(df)
       
       # Generate visualization
       coordinator = AgentCoordinator()
       code, method = coordinator.generate_visualization_code(
           "Income vs spending", df_clean
       )
       
       # Execute
       viz_agent = VisualizationAgent()
       fig = viz_agent.execute_visualization_code(code, df_clean)
       
       assert fig is not None
   ```

2. **UI Tests (Manual)**
   - Upload various CSV formats
   - Test all chart types
   - Test all pre-built dashboards
   - Test chart persistence
   - Test error handling

### Performance Tests

1. **Data Cleaning Speed**
   ```python
   import time
   
   df = pd.read_csv('large_dataset.csv')  # 100K rows
   
   start = time.time()
   architect = DataArchitect()
   df_clean = architect.clean_data(df)
   duration = time.time() - start
   
   assert duration < 2.0  # Should complete in < 2 seconds
   ```

2. **Visualization Generation Speed**
   ```python
   # Ollama mode
   start = time.time()
   code, method = coordinator.generate_visualization_code(prompt, df)
   duration = time.time() - start
   assert duration < 10.0  # Ollama should respond in < 10 seconds
   
   # Rule-based mode
   start = time.time()
   code, method = viz_agent.create_visualization_from_prompt(prompt, df)
   duration = time.time() - start
   assert duration < 1.0  # Rule-based should be instant
   ```

---

## 🚀 Deployment Considerations

### Local Development
```powershell
# Run locally
streamlit run app.py
```

### Docker Deployment
```dockerfile
FROM python:3.10

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Copy app files
COPY . /app
WORKDIR /app

# Install Python deps
RUN pip install -r requirements.txt

# Pull Mistral model
RUN ollama pull mistral:7b

# Run
CMD ["streamlit", "run", "app.py"]
```

### Streamlit Cloud
- Ollama requires local server (cannot deploy to cloud)
- Set `use_ollama=False` to use rule-based generation only
- Or host Ollama separately and connect via API

---

## 📚 Learning Resources

1. **Streamlit:** https://docs.streamlit.io/
2. **Plotly:** https://plotly.com/python/
3. **Ollama:** https://ollama.ai/docs
4. **Mistral AI:** https://mistral.ai/
5. **Pandas:** https://pandas.pydata.org/

---

**Architecture Complete! Ready for Implementation.**
