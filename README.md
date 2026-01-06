# AI-Powered Dashboard System

A multi-agentic AI dashboard application built with Streamlit, LangChain, and Gemini 2.5-flash-lite that transforms CSV data into interactive visualizations through natural language prompts.

## 🎯 Features

- **CSV Upload & Data Cleaning**: Automatically clean and process uploaded CSV files
- **SQLite Storage**: Persist cleaned data in SQLite database
- **Natural Language Queries**: Generate visualizations using simple text prompts
- **Multi-Agent Architecture**: Specialized agents for different tasks
- **Interactive Dashboard**: Power BI-like visualization capabilities
- **Multiple Chart Types**: Support for various visualization types

## 🏗️ Architecture

### Multi-Agent System

1. **Data Cleaning Agent**: Handles data preprocessing and cleaning
2. **Data Analysis Agent**: Analyzes data structure and statistics
3. **Visualization Agent**: Generates appropriate visualizations
4. **Query Agent**: Interprets user prompts and orchestrates other agents

### Tech Stack

- **Frontend**: Streamlit
- **LLM Framework**: LangChain
- **AI Model**: Google Gemini 2.5-flash-lite
- **Database**: SQLite
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Data Processing**: Pandas, NumPy

## 📁 Project Structure

```
ai-dashboard-system/
├── agents/                      # AI Agent modules
│   ├── __init__.py
│   ├── base_agent.py           # Base agent class
│   ├── data_cleaning_agent.py  # Data cleaning agent
│   ├── analysis_agent.py       # Data analysis agent
│   ├── visualization_agent.py  # Visualization generation agent
│   └── orchestrator_agent.py   # Main orchestration agent
│
├── database/                    # Database management
│   ├── __init__.py
│   ├── sqlite_manager.py       # SQLite operations
│   └── models.py               # Data models
│
├── utils/                       # Utility functions
│   ├── __init__.py
│   ├── data_processor.py       # Data processing utilities
│   ├── chart_generator.py      # Chart generation utilities
│   └── prompt_templates.py     # LangChain prompt templates
│
├── ui/                          # Streamlit UI components
│   ├── __init__.py
│   ├── sidebar.py              # Sidebar components
│   ├── dashboard.py            # Dashboard layout
│   └── visualizations.py       # Visualization rendering
│
├── config/                      # Configuration files
│   ├── __init__.py
│   └── settings.py             # App settings and constants
│
├── data/                        # Data directory
│   ├── uploads/                # Uploaded CSV files
│   └── database/               # SQLite database files
│
├── tests/                       # Unit tests
│   ├── __init__.py
│   ├── test_agents.py
│   ├── test_database.py
│   └── test_utils.py
│
├── app.py                       # Main Streamlit application
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore file
└── README.md                    # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Google Gemini API key

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd ai-dashboard-system
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

5. Run the application
```bash
streamlit run app.py
```

## 📊 Usage

1. **Upload CSV**: Click on the file uploader to select your CSV file
2. **Data Cleaning**: The system automatically cleans and processes the data
3. **Enter Prompt**: Type a natural language query (e.g., "Show me sales trends by month")
4. **View Dashboard**: The system generates relevant visualizations automatically

## 🤖 Agent Workflow

```
User Upload CSV
    ↓
Data Cleaning Agent (Clean & Validate)
    ↓
SQLite Storage
    ↓
User Enters Prompt
    ↓
Orchestrator Agent (Parse Intent)
    ↓
Analysis Agent (Analyze Data)
    ↓
Visualization Agent (Generate Charts)
    ↓
Dashboard Display
```

## 🔧 Configuration

Edit `config/settings.py` to customize:
- Model parameters
- Chart types
- Database settings
- UI preferences

## 📝 Example Prompts

- "Show me a bar chart of sales by category"
- "Create a line graph showing monthly trends"
- "Display a pie chart of revenue distribution"
- "Compare products performance with a scatter plot"

## 🧪 Testing

```bash
pytest tests/
```

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
