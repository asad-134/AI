# 🚀 Quick Start Guide
## Multi-Agent Dashboard - Get Running in 5 Minutes

---

## ✅ Prerequisites Check

Before starting, ensure you have:
- [ ] Windows 10/11
- [ ] Python 3.8 or higher
- [ ] PowerShell access
- [ ] 8GB+ RAM (recommended for Ollama)
- [ ] Internet connection (for initial setup)

---

## 📦 Step 1: Install Ollama (5 minutes)

### Option A: Automatic Installation

1. **Download Ollama for Windows:**
   - Visit: https://ollama.ai/download
   - Download Windows installer
   - Run the installer

2. **Verify Installation:**
   ```powershell
   ollama --version
   ```
   You should see version info.

3. **Pull Mistral 7B Model:**
   ```powershell
   ollama pull mistral:7b
   ```
   This will download ~4.1GB. Wait for completion.

4. **Test Ollama:**
   ```powershell
   ollama list
   ```
   You should see `mistral:7b` in the list.

### Option B: Already Have Ollama?

Just pull the model if you don't have it:
```powershell
ollama pull mistral:7b
```

---

## 🐍 Step 2: Install Python Dependencies (2 minutes)

1. **Navigate to Project:**
   ```powershell
   cd "c:\Users\eduah\Desktop\dashboard 2.0"
   ```

2. **Install Requirements:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Verify Installation:**
   ```powershell
   python -c "import streamlit; import plotly; import pandas; print('All packages installed!')"
   ```

---

## 🎮 Step 3: Launch Dashboard (30 seconds)

1. **Start the App:**
   ```powershell
   streamlit run app.py
   ```

2. **Browser Opens Automatically:**
   - If not, go to: http://localhost:8501

3. **You Should See:**
   - Blue header: "🤖 Multi-Agent Analytics Dashboard"
   - Sidebar with "AI Model Status"
   - File upload section

---

## 📊 Step 4: First Visualization (2 minutes)

### Quick Test Workflow:

1. **Load Default Dataset:**
   - Click "📊 Use Default Dataset (ifood_df.csv)"
   - Wait for cleaning to complete
   - You'll see "✅ Data loaded and cleaned successfully!"

2. **View Cleaning Report:**
   - Expand "View Cleaning Report"
   - See all data cleaning operations

3. **Create First Chart:**
   - Go to "🎨 Create Visualization" tab
   - Click "📊 Spending Overview" quick button
   - Wait 2-3 seconds
   - Chart appears in the gallery!

4. **Create Second Chart:**
   - Click "👥 Demographics" button
   - New chart appears next to the first one
   - Side-by-side layout!

5. **Try Natural Language:**
   - Type: "Show Income vs MntTotal scatter plot"
   - Click "🎨 Generate Visualization"
   - Chart appears in gallery

---

## 🎯 Step 5: Explore Features (5 minutes)

### Try Pre-built Dashboards:

1. **Campaign Success Dashboard:**
   - Look in sidebar
   - Click "📊 Campaign Success & Engagement"
   - 4 charts load automatically
   - All arranged side-by-side

2. **Family & Spending Dashboard:**
   - Click "📊 Family & Spending Habits"
   - Another set of charts loads
   - Charts from previous dashboard persist!

### Try Data Analysis:

1. **Go to "🔍 Data Analysis" Tab**

2. **Click "🔍 High Value Customers"**
   - Ollama analyzes your data
   - Provides insights in natural language

3. **Ask Custom Question:**
   - Type: "What factors influence spending the most?"
   - Click "🤔 Analyze"
   - Get AI-powered insights

---

## 💡 Example Prompts to Try

### KPI Cards:
```
Calculate the conversion rate using the Response column
Show average income as a KPI
```

### Bar Charts:
```
Compare average MntTotal across education levels
Show campaign acceptance by marital status
```

### Scatter Plots:
```
Plot Income vs MntTotal colored by education_Graduation
Show Age vs spending with education as color
```

### Heatmaps:
```
Correlation heatmap of Income, Recency, MntWines, NumWebVisitsMonth
Show correlations between all spending columns
```

### Treemaps:
```
MntTotal distribution by marital status
Revenue breakdown by education level
```

---

## 🐛 Troubleshooting

### Problem: Ollama Not Connected

**Symptoms:**
```
⚠️ Ollama not available: Connection refused
```

**Solution:**
```powershell
# Start Ollama service
ollama serve
```

In another PowerShell window:
```powershell
# Restart Streamlit
streamlit run app.py
```

### Problem: Model Not Found

**Symptoms:**
```
Error: model 'mistral:7b' not found
```

**Solution:**
```powershell
ollama pull mistral:7b
```

### Problem: Port Already in Use

**Symptoms:**
```
Error: Port 8501 is already in use
```

**Solution:**
```powershell
# Find and kill process using port 8501
netstat -ano | findstr :8501
taskkill /PID <PID_NUMBER> /F

# Or use different port:
streamlit run app.py --server.port 8502
```

### Problem: Import Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'plotly'
```

**Solution:**
```powershell
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Problem: Slow Performance

**Solution:**
```powershell
# Disable Ollama (use rule-based only)
# In the UI, uncheck "Use AI" when generating visualizations
```

---

## 📁 Your Files

All your work is in:
```
c:\Users\eduah\Desktop\dashboard 2.0\
```

**Core Files:**
- `app.py` - Main application
- `data_architect.py` - Data cleaning
- `visualization_agent.py` - Chart generation
- `agent_coordinator.py` - LLM orchestration
- `dashboard_templates.py` - Pre-built dashboards
- `ifood_df.csv` - Sample dataset

**Documentation:**
- `README.md` - Full documentation
- `ARCHITECTURE.md` - Technical architecture
- `QUICKSTART.md` - This file

---

## 🎓 Next Steps

### 1. Upload Your Own Data

Requirements:
- CSV format
- Similar structure to ifood_df.csv
- Columns for demographics, spending, campaigns

### 2. Create Custom Dashboards

Edit `dashboard_templates.py`:
```python
MY_DASHBOARD = {
    'name': 'My Custom Dashboard',
    'description': 'Custom analysis',
    'prompts': [
        {
            'title': 'My Chart',
            'prompt': 'Show me X vs Y',
            'chart_type': 'scatter'
        }
    ]
}

ALL_DASHBOARDS.append(MY_DASHBOARD)
```

### 3. Customize Visualizations

Edit `visualization_agent.py`:
- Change color palettes
- Add new chart types
- Modify themes

### 4. Tune Ollama

Try different models:
```powershell
# Smaller, faster model
ollama pull mistral:7b-instruct

# Larger, more capable model
ollama pull llama2:13b
```

Edit `agent_coordinator.py`:
```python
def __init__(self, model_name: str = "llama2:13b"):
```

---

## 🎉 Success Checklist

After following this guide, you should be able to:

- [x] Start Ollama and verify Mistral 7B is installed
- [x] Launch Streamlit dashboard
- [x] Load and clean data automatically
- [x] Create visualizations with natural language
- [x] See charts persist side-by-side
- [x] Use pre-built dashboards
- [x] Get AI-powered data insights
- [x] Switch between Ollama and rule-based generation

---

## 📞 Getting Help

### Check Status:

1. **Ollama Status:**
   ```powershell
   ollama list
   ```

2. **Python Packages:**
   ```powershell
   pip list | findstr "streamlit plotly pandas"
   ```

3. **Application Status:**
   - Look at sidebar in dashboard
   - Check "🤖 AI Model Status" section

### Common Issues:

| Issue | Quick Fix |
|-------|-----------|
| Ollama not connecting | Run `ollama serve` |
| Charts not appearing | Check browser console (F12) |
| Slow generation | Uncheck "Use AI" checkbox |
| Wrong visualization | Try more specific prompt |
| Data not loading | Check CSV format matches sample |

---

## ⚡ Performance Tips

1. **First Generation Slower:**
   - Ollama "warms up" on first prompt
   - Subsequent generations are faster

2. **Use Quick Buttons:**
   - Faster than typing prompts
   - Pre-optimized queries

3. **Rule-Based Mode:**
   - Instant generation
   - Good for simple charts
   - Uncheck "Use AI" if speed matters

4. **Clear Old Charts:**
   - Click "🗑️ Clear All Charts"
   - Frees memory

---

## 🎬 Video Walkthrough (If Available)

[Future: Add link to video demo]

---

## 🚀 You're Ready!

You now have a fully functional Multi-Agent Analytics Dashboard.

**Happy Analyzing! 📊**

---

**Questions?** Check [README.md](README.md) and [ARCHITECTURE.md](ARCHITECTURE.md) for detailed info.
