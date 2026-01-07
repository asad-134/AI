# 📋 Quick Reference Card
## Multi-Agent Dashboard - Cheat Sheet

---

## 🚀 Start Command
```powershell
streamlit run app.py
```

---

## 📊 Chart Type Keywords

| Chart Type | Keywords to Use |
|------------|----------------|
| **KPI Card** | kpi, metric, card, rate, conversion |
| **Bar Chart** | bar, compare, comparison, across |
| **Scatter Plot** | scatter, plot, vs, relationship |
| **Heatmap** | heatmap, correlation, heat map |
| **Treemap** | treemap, tree map, hierarchical |
| **Box Plot** | box, distribution, quartile |
| **Histogram** | histogram, frequency, distribution |

---

## 💬 Quick Prompts

### Copy & Paste Ready

**KPIs:**
```
Calculate conversion rate using Response column
Show average income as KPI
```

**Comparisons:**
```
Compare average MntTotal by education level
Show campaign acceptance rates
```

**Relationships:**
```
Plot Income vs MntTotal scatter plot
Show Age vs spending colored by education
```

**Correlations:**
```
Correlation heatmap of Income, Recency, MntWines, NumWebVisitsMonth
```

---

## 🎯 Column Names Reference

### Demographics
- `Age`, `Income`
- `education_Graduation`, `education_Master`, `education_PhD`, `education_Basic`
- `marital_Married`, `marital_Single`, `marital_Divorced`, `marital_Widow`

### Spending
- `MntWines`, `MntFruits`, `MntMeatProducts`
- `MntFishProducts`, `MntSweetProducts`, `MntGoldProds`
- `MntTotal`, `MntRegularProds`

### Campaigns
- `AcceptedCmp1`, `AcceptedCmp2`, `AcceptedCmp3`, `AcceptedCmp4`, `AcceptedCmp5`
- `Response`, `Complain`

### Behavior
- `NumWebVisitsMonth`, `NumWebPurchases`
- `NumCatalogPurchases`, `NumStorePurchases`
- `NumDealsPurchases`, `Recency`

### Family
- `Kidhome`, `Teenhome`

---

## 🔧 Common Commands

```powershell
# Check Ollama
ollama list

# Pull model
ollama pull mistral:7b

# Start Ollama
ollama serve

# Install packages
pip install -r requirements.txt

# Run tests
python test_dashboard.py

# Start dashboard
streamlit run app.py
```

---

## 🐛 Quick Fixes

| Problem | Solution |
|---------|----------|
| Ollama not connecting | `ollama serve` |
| Model not found | `ollama pull mistral:7b` |
| Charts not showing | Check "Use AI" checkbox |
| Slow generation | Uncheck "Use AI" |
| Wrong chart | Be more specific in prompt |

---

## 🎨 Sidebar Features

- **🤖 AI Model Status** - Check Ollama connection
- **📊 Dataset Info** - View data summary
- **🗑️ Clear All Charts** - Reset gallery
- **💾 Download Data** - Export cleaned CSV
- **📋 Pre-built Dashboards** - Load chart sets

---

## ⚡ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Stop Streamlit | `Ctrl + C` (in terminal) |
| Refresh browser | `F5` |
| Open DevTools | `F12` |
| Full screen | `F11` |

---

## 📍 URLs

- **Dashboard:** http://localhost:8501
- **Ollama:** http://localhost:11434
- **Download Ollama:** https://ollama.ai/download

---

## 🎯 Success Checklist

- [ ] Ollama installed and running
- [ ] Mistral 7B model downloaded
- [ ] Python packages installed
- [ ] Dashboard starts without errors
- [ ] Can load default dataset
- [ ] Charts appear in gallery
- [ ] AI status shows "Connected"

---

## 📚 Quick Links

- Full docs: [README.md](README.md)
- Setup: [QUICKSTART.md](QUICKSTART.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🎓 Learning Order

1. Load default dataset
2. Click quick buttons
3. Try pre-built dashboards
4. Write simple prompts
5. Experiment with chart types
6. Combine multiple charts
7. Use data analysis
8. Create custom dashboards

---

## 💡 Pro Tips

✨ Use exact column names
✨ Specify chart type explicitly
✨ Request sorting when comparing
✨ Add color for context
✨ Use quick buttons for speed
✨ Clear charts to free memory
✨ Download data after cleaning

---

**Keep this card handy while using the dashboard!**

_Print or bookmark for quick reference_
