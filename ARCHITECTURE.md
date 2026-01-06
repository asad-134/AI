# Architecture Documentation

## System Overview

The AI-Powered Dashboard System is a multi-agent application that enables users to upload CSV files and generate visualizations through natural language queries. The system leverages Google's Gemini AI model through LangChain for intelligent data analysis and visualization recommendations.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend (UI)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Sidebar    │  │  Dashboard   │  │Visualizations│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────┐
│                    Orchestrator Agent                        │
│                  (Workflow Coordination)                     │
└────────────────────────────┬────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌────────▼────────┐  ┌───────▼────────┐
│ Data Cleaning  │  │    Analysis     │  │ Visualization  │
│     Agent      │  │     Agent       │  │     Agent      │
└───────┬────────┘  └────────┬────────┘  └───────┬────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────┐
│                      LangChain Layer                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Google Gemini 2.0 Flash (LLM)                │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────┐
│                      Data Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   SQLite DB  │  │    Pandas    │  │   Plotly     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. Frontend Layer (Streamlit UI)

**Components:**
- `ui/sidebar.py`: File upload, dataset selection, navigation
- `ui/dashboard.py`: Main dashboard, query interface, results display
- `ui/visualizations.py`: Chart rendering and interaction

**Responsibilities:**
- User interaction
- File upload handling
- Query input collection
- Visualization rendering
- Session state management

### 2. Agent Layer

#### Orchestrator Agent (`agents/orchestrator_agent.py`)
**Role:** Main coordinator for all agents

**Workflow:**
1. Receives user query and data
2. Classifies user intent
3. Coordinates other agents in sequence
4. Aggregates results
5. Returns complete analysis

**Key Methods:**
- `execute()`: Main orchestration method
- `process_uploaded_file()`: Handle file uploads
- `_classify_intent()`: Understand user requests

#### Data Cleaning Agent (`agents/data_cleaning_agent.py`)
**Role:** Data preprocessing and quality improvement

**Operations:**
- Detect and handle missing values
- Remove duplicates
- Normalize data types
- Handle outliers
- Generate cleaning reports

**AI-Powered Features:**
- Intelligent column removal suggestions
- Context-aware missing value strategies
- Data quality issue detection

#### Analysis Agent (`agents/analysis_agent.py`)
**Role:** Data analysis and insight generation

**Capabilities:**
- Statistical analysis
- Correlation detection
- Data grouping and aggregation
- Trend identification
- Insight generation

**AI-Powered Features:**
- Query intent understanding
- Automatic feature selection
- Smart aggregation recommendations

#### Visualization Agent (`agents/visualization_agent.py`)
**Role:** Chart recommendation and specification

**Chart Types Supported:**
- Bar charts
- Line charts
- Scatter plots
- Pie charts
- Histograms
- Box plots
- Heatmaps
- Area charts

**AI-Powered Features:**
- Automatic chart type selection
- Layout recommendations
- Multi-chart dashboards
- Configuration optimization

### 3. Base Agent (`agents/base_agent.py`)

**Purpose:** Common functionality for all agents

**Provides:**
- LLM initialization
- Chain creation
- Prompt template handling
- Logging utilities

### 4. Database Layer

#### SQLite Manager (`database/sqlite_manager.py`)
**Responsibilities:**
- Dataset storage and retrieval
- Metadata management
- Query history tracking
- Visualization caching

**Tables:**
- `datasets`: Dataset metadata
- `query_history`: User query logs
- `visualization_cache`: Cached visualizations
- Dynamic data tables (one per dataset)

### 5. Utility Layer

#### Data Processor (`utils/data_processor.py`)
**Functions:**
- Date column detection
- Numeric column detection
- Outlier removal
- Column normalization
- Summary statistics
- Data aggregation
- Filtering and pivoting

#### Chart Generator (`utils/chart_generator.py`)
**Functions:**
- Create various chart types using Plotly
- Generate charts from specifications
- Apply customizations
- Handle data formatting

#### Prompt Templates (`utils/prompt_templates.py`)
**Contains:**
- Structured prompts for each agent
- Intent classification prompts
- Error recovery prompts
- Insight generation prompts

### 6. Configuration Layer

#### Settings (`config/settings.py`)
**Manages:**
- API keys
- Model configuration
- File upload limits
- Chart defaults
- Database paths
- Error messages
- Success messages
- Query examples

## Data Flow

### File Upload Flow

```
1. User uploads CSV → Sidebar Component
2. File saved temporarily → Upload Directory
3. Orchestrator processes file
4. Data Cleaning Agent cleans data
5. Cleaned data saved to SQLite
6. Metadata stored
7. Dataset available for querying
```

### Query Execution Flow

```
1. User enters natural language query
2. Query sent to Orchestrator Agent
3. Orchestrator classifies intent
4. Analysis Agent analyzes data
   - Determines relevant columns
   - Performs aggregations
   - Generates insights
5. Visualization Agent recommends charts
   - Selects chart types
   - Configures visualizations
6. Chart Generator creates Plotly figures
7. UI renders visualizations
8. Query saved to history
```

## Agent Communication

Agents communicate through structured dictionaries:

```python
{
    'success': bool,
    'data': DataFrame or dict,
    'results': {
        'analysis_plan': {...},
        'aggregated_data': DataFrame,
        'insights': [...]
    },
    'visualizations': {
        'chart_specifications': [...]
    }
}
```

## AI Integration

### LangChain Usage

**Chain Creation:**
```python
prompt = PromptTemplate(template=..., input_variables=[...])
chain = LLMChain(llm=gemini_llm, prompt=prompt)
result = chain.run(variables)
```

**Gemini Model:**
- Model: `gemini-2.0-flash-exp`
- Temperature: 0.7 (configurable)
- Max tokens: 2048 (configurable)

### Prompt Engineering

Each agent uses specialized prompts:
- Structured output (JSON format)
- Clear instructions
- Context provision
- Example expectations

## Scalability Considerations

### Current Design
- Single-threaded execution
- In-memory data processing
- Local SQLite database
- Synchronous agent execution

### Future Enhancements
- Async agent execution
- Distributed processing
- Cloud database integration
- Caching mechanisms
- Load balancing

## Security Considerations

1. **API Key Management**: Stored in .env file
2. **File Upload**: Size and type restrictions
3. **SQL Injection**: Parameterized queries
4. **Data Privacy**: Local storage only

## Error Handling

**Strategy:**
- Try-catch blocks at each layer
- Graceful degradation
- User-friendly error messages
- Detailed logging for debugging
- Default fallbacks for AI failures

## Performance Optimization

1. **Data Processing**: Pandas vectorized operations
2. **Database**: Indexed queries
3. **Visualization**: Plotly optimization
4. **Caching**: Query result caching (future)
5. **Lazy Loading**: Load data on demand

## Testing Strategy

**Test Coverage:**
- Unit tests for each agent
- Database operation tests
- Utility function tests
- Integration tests (future)
- E2E tests (future)

## Deployment

**Current Setup:** Local development

**Production Considerations:**
- Streamlit Cloud deployment
- Environment variable management
- Database migration to cloud
- API rate limiting
- User authentication

## Monitoring & Logging

**Current Implementation:**
- Console logging in agents
- Query history in database
- Error tracking in UI

**Future Enhancements:**
- Structured logging
- Performance metrics
- User analytics
- Error monitoring service
