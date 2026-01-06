# Multi-Agent Analytics Dashboard

## 🎯 Overview

A sophisticated Streamlit-based analytics dashboard powered by **Ollama Mistral 7B** that uses multiple AI agents to clean data, generate visualizations, and provide insights using the **Context-Task-Formatting** framework.

## 🏗️ Architecture

### Multi-Agent System

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit UI Layer                        │
│                    (app.py - UI Orchestrator)                │
└────────────────┬──────────────────────────────────┬──────────┘
                 │                                  │
        ┌────────▼────────┐                ┌───────▼──────────┐
        │ Agent Coordinator│                │ Dashboard        │
        │                 │                │ Templates        │
        │ - Ollama LLM    │                │                  │
        │ - Prompt Engine │                │ - Pre-built      │
        │ - Code Generator│                │   Dashboards     │
        └────────┬────────┘                │ - Analysis       │
                 │                          │   Templates      │
     ┌───────────┼───────────┐             └──────────────────┘
     │           │           │
┌────▼───┐  ┌───▼─────┐  ┌─▼──────────┐
│ Data   │  │ Visual  │  │  Ollama    │
│Architect│  │ Agent   │  │ Mistral 7B │
│        │  │         │  │            │
│-Clean  │  │-Plotly  │  │- Natural   │
│-Impute │  │-Charts  │  │  Language  │
│-Feature│  │-Persona │  │- Code Gen  │
└────────┘  └─────────┘  └────────────┘
```

## 🧩 Components

### 1. Data Architect (`data_architect.py`)

**Purpose:** Intelligent data cleaning and feature engineering

**Key Features:**
- **Median Imputation** for Income grouped by education level
- **Mode Imputation** for categorical/binary flags
- **Feature Engineering** for spending columns (Mnt*)
- **Customer Days calculation** from date columns
- **Aggregate creation** (MntTotal, MntRegularProds, MntGoldProds)

**Context-Task-Formatting Implementation:**
```python
Context: Income missing values, Education levels available
Task: Impute using median grouped by education
Formatting: Preserve original data types
```

### 2. Visualization Agent (`visualization_agent.py`)

**Purpose:** Senior Marketing Analyst persona for creating executive-level visualizations

**Capabilities:**
- KPI Cards with conditional coloring
- Bar Charts with aggregation and sorting
- Scatter Plots with color coding
- Correlation Heatmaps
- Treemaps for hierarchical data
- Box Plots and Histograms

**Prompt Framework:**
```python
Context: Available columns (Demographics, Spending, Campaigns)
Task: Identify chart type from user request
Formatting: Plotly Express/Graph Objects, plotly_dark theme
```

### 3. Agent Coordinator (`agent_coordinator.py`)

**Purpose:** Orchestrate communication between agents and Ollama LLM

**Functions:**
- Connect to Ollama Mistral 7B
- Enhance prompts with dataset context
- Generate visualization code using LLM
- Extract executable Python code from responses
- Fallback to rule-based generation
- Provide data analysis insights

### 4. Dashboard Templates (`dashboard_templates.py`)

**Purpose:** Pre-configured analysis dashboards

**Available Dashboards:**

1. **Campaign Success & Engagement**
   - Conversion Rate KPI
   - Education vs Spending
   - Spending Drivers Correlation
   - Campaign Acceptance Analysis

2. **Family & Spending Habits**
   - Product Type by Children
   - Income-Spending Relationship
   - Revenue by Household Type
   - Family Size Distribution

3. **Customer Behavior Analysis**
   - Recency vs Spending
   - Web Visits vs Purchases
   - Purchase Channel Comparison
   - Deals vs Regular Purchases

4. **Demographics & Segmentation**
   - Age Distribution
   - Income Distribution
   - Age vs Income Analysis
   - Marital Status Revenue

5. **Product Category Performance**
   - Product Category Comparison
   - Wine Spending Correlation
   - Product Mix Heatmap
   - Gold vs Regular Products

### 5. UI Orchestrator (`app.py`)

**Purpose:** Main Streamlit application with persistent chart history

**Features:**
- Session state management for chart persistence
- Side-by-side chart rendering (2 per row)
- Interactive visualization creator
- Gallery view for all charts
- AI-powered data analysis
- Pre-built dashboard loader

## 🚀 Setup & Installation

### Prerequisites

1. **Python 3.8+**
2. **Ollama installed** with Mistral 7B model

### Install Ollama (if not already installed)

**Windows:**
```powershell
# Download and install from: https://ollama.ai/download
# After installation, pull Mistral 7B:
ollama pull mistral:7b
```

**Verify Ollama:**
```powershell
ollama list
```

### Install Python Dependencies

```powershell
# Navigate to project directory
cd "c:\Users\eduah\Desktop\dashboard 2.0"

# Install requirements
pip install -r requirements.txt
```

## 🎮 Usage

### Start the Application

```powershell
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

### Workflow

1. **Upload Data**
   - Upload CSV file or use default `ifood_df.csv`
   - Data Architect automatically cleans the data
   - View cleaning report

2. **Create Visualizations**
   - Use natural language prompts
   - Example: "Show me Income vs MntTotal colored by education level"
   - Toggle "Use AI" to enable/disable Ollama
   - Charts are added to persistent gallery

3. **Use Pre-built Dashboards**
   - Click dashboard buttons in sidebar
   - All charts load automatically
   - Arranged in side-by-side layout

4. **Analyze Data**
   - Ask custom questions
   - Use pre-defined analysis templates
   - Get AI-powered insights

## 📝 Example Prompts

### KPI Cards
```
"Calculate the conversion rate using the Response column. If below 15%, color red"
"Show average income as a KPI metric"
```

### Bar Charts
```
"Compare average MntTotal across education levels, sort descending"
"Show campaign acceptance by marital status"
```

### Scatter Plots
```
"Plot Income vs MntTotal colored by education_Graduation"
"Show relationship between Age and spending with recency as color"
```

### Heatmaps
```
"Correlation heatmap of Income, Recency, MntWines, NumWebVisitsMonth"
"Show correlations between all spending columns"
```

### Treemaps
```
"MntTotal distribution by marital status"
"Revenue breakdown by education level"
```

## 🧠 Context-Task-Formatting Framework

Every agent operation follows this framework:

### Data Architect Example
```
Context: Income column has missing values; Education columns available
Task: Impute missing Income using median grouped by education level
Formatting: For PhD with missing income, use median of all PhDs
```

### Visualization Agent Example
```
Context: User requests "spending by education"
Task: Create bar chart showing average MntTotal per education category
Formatting: Use Plotly Express, plotly_dark theme, sort descending, label axes
```

## 🔧 Configuration

### Change Ollama Model

Edit `agent_coordinator.py`:
```python
def __init__(self, model_name: str = "mistral:7b"):  # Change here
```

Available models:
- `mistral:7b` (default)
- `llama2:13b`
- `codellama:34b`

### Customize Color Palettes

Edit `visualization_agent.py`:
```python
self.color_palettes = {
    'default': px.colors.qualitative.Plotly,
    'viridis': px.colors.sequential.Viridis,
    # Add your custom palette
}
```

### Add Custom Dashboard Templates

Edit `dashboard_templates.py`:
```python
CUSTOM_DASHBOARD = {
    'name': 'Your Dashboard Name',
    'description': 'Dashboard description',
    'prompts': [
        {
            'title': 'Chart Title',
            'prompt': 'Your visualization prompt',
            'chart_type': 'bar'
        }
    ]
}

# Add to ALL_DASHBOARDS list
ALL_DASHBOARDS.append(CUSTOM_DASHBOARD)
```

## 📊 Data Requirements

### Expected Columns

**Demographics:**
- Age, Income
- education_* (one-hot encoded)
- marital_* (one-hot encoded)

**Spending:**
- MntWines, MntFruits, MntMeatProducts
- MntFishProducts, MntSweetProducts, MntGoldProds

**Campaigns:**
- AcceptedCmp1, AcceptedCmp2, AcceptedCmp3, AcceptedCmp4, AcceptedCmp5
- Response

**Family:**
- Kidhome, Teenhome

**Behavior:**
- NumWebVisitsMonth, Recency, Customer_Days
- NumWebPurchases, NumCatalogPurchases, NumStorePurchases
- NumDealsPurchases

### Data Cleaning Pipeline

1. **Income Imputation:** Median by education group
2. **Categorical Imputation:** Mode for each column
3. **Feature Engineering:** Convert Mnt columns to numeric
4. **Date Processing:** Calculate Customer_Days
5. **Aggregates:** Create MntTotal, MntRegularProds, MntGoldProds

## 🎨 UI Features

### Session State Management
- Persistent chart history across interactions
- No chart loss on new prompts
- Individual chart deletion

### Side-by-Side Layout
```python
for i in range(0, len(charts), 2):
    cols = st.columns(2)
    # First chart in cols[0]
    # Second chart in cols[1]
```

### Responsive Design
- Automatically adjusts for odd number of charts
- Last chart takes full width if alone
- Mobile-friendly layout

## 🐛 Troubleshooting

### Ollama Connection Issues
```
⚠️ Ollama not available: Connection refused
```
**Solution:** Ensure Ollama is running:
```powershell
ollama serve
```

### Model Not Found
```
Error: model 'mistral:7b' not found
```
**Solution:** Pull the model:
```powershell
ollama pull mistral:7b
```

### Import Errors
```
ModuleNotFoundError: No module named 'plotly'
```
**Solution:** Install requirements:
```powershell
pip install -r requirements.txt
```

### Visualization Errors
- If Ollama fails, system automatically falls back to rule-based generation
- Check sidebar for "Model Status"
- Verify dataset has required columns

## 📈 Performance

- **Data Cleaning:** < 1 second for 10K rows
- **Chart Generation (Ollama):** 2-5 seconds
- **Chart Generation (Rule-based):** < 0.5 seconds
- **Chart Rendering:** Instant (Plotly is fast)

## 🔒 Security

- No external API calls (Ollama runs locally)
- Data never leaves your machine
- No cloud dependencies
- Privacy-first architecture

## 📄 File Structure

```
dashboard 2.0/
├── app.py                      # Main Streamlit application
├── data_architect.py           # Data cleaning agent
├── visualization_agent.py      # Visualization generation agent
├── agent_coordinator.py        # LLM orchestration
├── dashboard_templates.py      # Pre-built dashboards
├── requirements.txt            # Python dependencies
├── ifood_df.csv               # Default dataset
└── README.md                  # This file
```

## 🚀 Future Enhancements

- [ ] Add more chart types (Sankey, Sunburst, 3D plots)
- [ ] Export dashboard as HTML
- [ ] Scheduled reports
- [ ] Real-time data refresh
- [ ] Custom theme builder
- [ ] Multi-dataset support
- [ ] Collaborative features
- [ ] Mobile app version

## 📚 References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [Ollama Documentation](https://ollama.ai/docs)
- [Mistral AI](https://mistral.ai/)

## 🤝 Contributing

This is a demonstration project. Feel free to:
1. Fork the repository
2. Create feature branches
3. Submit pull requests
4. Report issues

## 📧 Support

For questions or issues, consult the documentation or check:
- Ollama installation status
- Python package versions
- Dataset format

---

**Built with ❤️ using Streamlit, Plotly, and Ollama Mistral 7B**
