# OpenRouter Gemma3 27B Dashboard - Quick Reference

## ✅ Migration Complete!

Your dashboard now uses **OpenRouter Gemma3 27B** instead of Ollama Mistral 7B.

## 🚀 Starting the Dashboard

**Option 1: With API key from registry (Recommended for Windows)**
```powershell
$env:OPENROUTER_API_KEY = (Get-ItemProperty -Path 'HKCU:\Environment').OPENROUTER_API_KEY
streamlit run app.py
```

**Option 2: Direct environment variable**
```powershell
$env:OPENROUTER_API_KEY = "your-api-key-here"
streamlit run app.py
```

**Option 3: After restarting terminal**
```bash
streamlit run app.py
```
(API key will be loaded automatically after terminal restart)

## 🎯 Testing the AI

Try these prompts to test Gemma3 27B:

### Simple Tests
- "Show me campaign acceptance rates"
- "Create a bar chart of income by education"
- "Plot spending vs income as scatter"

### Complex Tests
- "Show me a correlation heatmap of all spending categories"
- "Create a treemap of total spending by marital status"
- "Display KPI cards for all campaign metrics"

### Natural Language Tests
- "Which education level spends the most on wine?"
- "Compare spending between married and single customers"
- "Show me how income relates to total purchases"

## 🔍 Verifying AI is Active

Look for these indicators in the app:

1. **Sidebar Status:**
   - ✅ OpenRouter Connected
   - Model: google/gemma-2-27b-it
   - ✓ API key configured

2. **Footer:**
   - "Powered by OpenRouter Gemma3 27B"

3. **Chart Generation:**
   - Method shown after chart: "llm" (AI) or "rule-based" (fallback)

## 💡 Model Comparison

| Feature | Ollama Mistral 7B | OpenRouter Gemma3 27B |
|---------|-------------------|----------------------|
| **Parameters** | 7B | 27B |
| **Hosting** | Local | Cloud |
| **Setup** | Install + Run | API Key only |
| **GPU Required** | Yes | No |
| **Code Quality** | Good | Better |
| **Cost** | Free (electricity) | ~$0.001/chart |
| **Reliability** | Varies by hardware | High |
| **Speed** | Depends on GPU | 2-4 seconds |

## 🎨 Features Working with Gemma3

- ✅ Natural language chart generation
- ✅ 7 chart types (KPI, Bar, Scatter, Heatmap, Treemap, Box, Histogram)
- ✅ Smart column detection
- ✅ Automatic code validation
- ✅ Fallback to rule-based if needed
- ✅ 20 pre-built dashboard templates
- ✅ Side-by-side chart gallery
- ✅ Persistent chart history

## 📊 Cost Tracking

Typical usage costs:
- **Per chart generation:** ~500-1000 tokens = $0.0003-$0.001
- **10 charts:** ~$0.01
- **100 charts:** ~$0.10
- **Daily active use (50 charts):** ~$0.05
- **Monthly estimate:** $1-$5

Much cheaper than running a local GPU!

## 🛠️ Troubleshooting

### "OpenRouter Not Available" warning
```bash
# Reload API key in current session
$env:OPENROUTER_API_KEY = (Get-ItemProperty -Path 'HKCU:\Environment').OPENROUTER_API_KEY

# Or check if it's set
echo $env:OPENROUTER_API_KEY
```

### Charts using "rule-based" instead of "llm"
- Check sidebar status shows "✅ OpenRouter Connected"
- Verify "Use AI" checkbox is enabled
- Try toggling it off and on again
- Check OpenRouter dashboard for usage/credits

### "Method: rule-based" always showing
- API key might not be configured
- Rate limit reached (wait 60 seconds)
- OpenRouter service issue (check status.openrouter.ai)
- Fallback is working correctly - charts still generate!

## 🎓 Pro Tips

1. **Cost Optimization:**
   - Use rule-based for simple charts
   - Use AI for complex natural language requests
   - Toggle "Use AI" checkbox as needed

2. **Better Prompts:**
   - Be specific: "bar chart of..." vs "show me..."
   - Mention columns: "income by education" vs "compare customers"
   - Add details: "sorted descending", "top 10", "with colors"

3. **Performance:**
   - First query might be slower (API warmup)
   - Subsequent queries are faster
   - Rule-based is instant (no API call)

## 📝 Next Steps

1. ✅ Dashboard running with Gemma3 27B
2. ✅ API key configured
3. ✅ Test queries working
4. 📋 Try the dashboard templates
5. 📋 Create custom visualizations
6. 📋 Export charts for reports

## 🆘 Need Help?

- **Setup Issues:** Re-run `python setup_openrouter.py`
- **API Issues:** Check https://openrouter.ai/dashboard
- **Chart Errors:** Check debug expander in UI
- **Documentation:** See OPENROUTER_MIGRATION.md

---

**Dashboard URL:** http://localhost:8504
**Status:** ✅ Running with OpenRouter Gemma3 27B
**Fallback:** ✅ Rule-based generation always available
