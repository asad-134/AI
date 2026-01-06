# 📚 Usage Examples & Prompt Library
## Multi-Agent Dashboard - Real-World Use Cases

---

## 🎯 Table of Contents

1. [KPI Cards](#kpi-cards)
2. [Bar Charts](#bar-charts)
3. [Scatter Plots](#scatter-plots)
4. [Heatmaps](#heatmaps)
5. [Treemaps](#treemaps)
6. [Box Plots](#box-plots)
7. [Histograms](#histograms)
8. [Complex Analysis](#complex-analysis)
9. [Dashboard Combos](#dashboard-combos)
10. [Troubleshooting Prompts](#troubleshooting-prompts)

---

## 📊 KPI Cards

### Conversion Rate
```
Calculate the conversion rate using the Response column. If below 15%, color the metric red.
```
**Result:** Single large number showing conversion percentage with conditional coloring

### Average Income
```
Show average income as a KPI metric
```
**Result:** Executive-style KPI card with average income value

### Campaign Success Rate
```
Calculate campaign acceptance rate from AcceptedCmp1 through AcceptedCmp5
```
**Result:** Overall campaign performance metric

### Customer Lifetime Value
```
Show average MntTotal as a customer lifetime value KPI
```
**Result:** Total spending KPI with professional formatting

---

## 📊 Bar Charts

### Basic Comparison
```
Compare average MntTotal across education levels
```
**Result:** Bar chart showing spending by education category

### Sorted Analysis
```
Compare average MntTotal across all education categories. Sort descending to show which education level spends the most.
```
**Result:** Bars sorted from highest to lowest spending

### Campaign Comparison
```
Compare acceptance rates across all campaigns (AcceptedCmp1 through AcceptedCmp5)
```
**Result:** Bar chart showing which campaign performed best

### Marital Status Revenue
```
Compare total MntTotal by marital status categories
```
**Result:** Revenue breakdown by relationship status

### Product Categories
```
Compare average spending across MntWines, MntMeatProducts, MntFishProducts, MntFruits, MntSweetProducts
```
**Result:** Multi-category product performance comparison

### Web Activity
```
Compare NumWebVisitsMonth by education level
```
**Result:** Digital engagement by demographic

### Purchase Channels
```
Compare NumWebPurchases, NumCatalogPurchases, and NumStorePurchases
```
**Result:** Channel performance analysis

---

## 🔵 Scatter Plots

### Income vs Spending
```
Plot Income vs MntTotal. Color the points by education_Graduation to see if higher education correlates with higher income/spend.
```
**Result:** Scatter plot showing relationship with education overlay

### Age Analysis
```
Show Age vs MntTotal scatter plot colored by marital status
```
**Result:** Age-spending relationship with demographic context

### Recency Risk
```
Create a scatter plot of Recency vs MntTotal to identify at-risk high-value customers
```
**Result:** Customer retention insights

### Web Engagement
```
Plot NumWebVisitsMonth vs NumWebPurchases to understand conversion efficiency
```
**Result:** Digital conversion analysis

### Wine Preferences
```
Show Income vs MntWines scatter plot
```
**Result:** Wine spending by income level

### Family Impact
```
Plot Kidhome vs MntTotal colored by Teenhome
```
**Result:** Family composition effect on spending

### Gold Products
```
Show Income vs MntGoldProds with education as color
```
**Result:** Premium product preference analysis

---

## 🔥 Heatmaps

### Spending Drivers
```
Show a correlation heatmap between Income, Recency, MntWines, and NumWebVisitsMonth to find spending drivers.
```
**Result:** Correlation matrix identifying key relationships

### Product Mix
```
Create a correlation heatmap of all Mnt spending columns
```
**Result:** Product category correlation analysis

### Full Demographics
```
Correlation heatmap of Income, Age, Kidhome, Teenhome, Recency
```
**Result:** Demographic relationships overview

### Campaign Correlation
```
Show correlation between all AcceptedCmp columns
```
**Result:** Campaign overlap analysis

### Comprehensive Analysis
```
Heatmap of Income, MntTotal, NumWebPurchases, NumCatalogPurchases, NumStorePurchases, Recency
```
**Result:** Multi-channel behavior correlation

---

## 🌳 Treemaps

### Revenue by Household
```
Create a treemap of MntTotal grouped by marital_ status categories to see which household type contributes most to revenue.
```
**Result:** Hierarchical revenue visualization

### Education Revenue
```
Treemap of MntTotal by education level
```
**Result:** Revenue contribution by education segment

### Campaign Revenue
```
Show MntTotal in a treemap grouped by Response column
```
**Result:** Responders vs non-responders revenue split

### Product Category Revenue
```
Create treemap showing MntWines, MntMeatProducts, MntFishProducts revenue distribution
```
**Result:** Product category size comparison

---

## 📦 Box Plots

### Income Distribution
```
Show Income distribution with a box plot
```
**Result:** Income quartiles and outliers

### Spending Distribution by Education
```
Box plot of MntTotal by education level
```
**Result:** Spending spread across education segments

### Age Distribution
```
Create box plot showing Age distribution by marital status
```
**Result:** Age ranges by relationship status

### Web Visits Distribution
```
Show NumWebVisitsMonth distribution across education levels
```
**Result:** Digital engagement distribution

---

## 📈 Histograms

### Age Segments
```
Create a histogram of Age distribution to understand customer age segments
```
**Result:** Age frequency distribution

### Income Brackets
```
Show Income distribution histogram with 20 bins
```
**Result:** Income bracket analysis

### Spending Patterns
```
Histogram of MntTotal to see spending distribution
```
**Result:** Customer spending frequency

### Family Size
```
Show the distribution of total family members (Kidhome + Teenhome) with a histogram
```
**Result:** Family composition patterns

### Web Engagement
```
Histogram of NumWebVisitsMonth
```
**Result:** Digital engagement frequency

---

## 🧠 Complex Analysis

### Multi-Dimensional Analysis
```
Create a scatter plot matrix showing relationships between Income, Age, MntTotal, and Recency
```
**Result:** Multi-variable relationship overview

### Segment Analysis
```
Show MntTotal by education level, with separate colors for Response (accepted vs not)
```
**Result:** Response pattern by education

### Cohort Comparison
```
Compare MntRegularProds vs MntGoldProds based on the number of children (Kidhome)
```
**Result:** Product preference by family size

### Time-Based Analysis
```
Plot Recency vs MntTotal with point size representing Age
```
**Result:** Three-dimensional customer insight

### Channel Efficiency
```
Scatter plot of NumWebVisitsMonth vs NumWebPurchases colored by Income quartiles
```
**Result:** Digital conversion by income level

---

## 🎨 Dashboard Combos

### Executive Dashboard
```
1. Calculate overall conversion rate KPI
2. Show MntTotal by education bar chart (sorted)
3. Income vs MntTotal scatter (colored by education)
4. Correlation heatmap of key metrics
```
**Use Case:** C-suite presentation

### Marketing Dashboard
```
1. Campaign acceptance rate KPI
2. Compare all campaigns bar chart
3. Response by education treemap
4. Campaign correlation heatmap
```
**Use Case:** Campaign performance review

### Product Dashboard
```
1. Total product revenue KPI
2. Product category comparison bar chart
3. Income vs wine spending scatter
4. Product mix correlation heatmap
```
**Use Case:** Product strategy meeting

### Customer Segmentation Dashboard
```
1. Average customer value KPI
2. Spending by demographics bar chart
3. Age vs income scatter (colored by marital status)
4. Demographic correlation heatmap
```
**Use Case:** Segmentation strategy

### Retention Dashboard
```
1. At-risk customers count KPI
2. Recency distribution histogram
3. Recency vs spending scatter
4. Retention drivers correlation
```
**Use Case:** Churn prevention strategy

---

## 🔍 Advanced Prompt Techniques

### Adding Filters
```
Show Income vs MntTotal for customers with education_Graduation = 1
```
**Note:** Visualization Agent will attempt to filter data

### Custom Colors
```
Plot Age vs MntTotal with blue color scheme
```
**Note:** Specify color preferences

### Custom Titles
```
Create bar chart of spending by education with title "Revenue by Education Segment"
```
**Note:** Override default titles

### Multiple Groups
```
Compare MntWines and MntMeatProducts by education level
```
**Note:** Multiple y-variables

### Statistical Overlays
```
Scatter plot of Income vs MntTotal with trend line
```
**Note:** Request statistical elements

---

## 🐛 Troubleshooting Prompts

### When Charts Don't Match Expectations

**Problem:** Wrong chart type
```
# Instead of:
"Show data about spending"

# Try:
"Create a bar chart comparing average spending by education level"
```

**Problem:** Wrong columns used
```
# Instead of:
"Show income stuff"

# Try:
"Plot Income vs MntTotal scatter plot"
```

**Problem:** No aggregation
```
# Instead of:
"Show education and spending"

# Try:
"Compare AVERAGE MntTotal across education levels"
```

**Problem:** No sorting
```
# Instead of:
"Compare spending"

# Try:
"Compare spending by education, sort descending"
```

### When Ollama Is Slow

**Solution 1:** Disable AI mode
- Uncheck "Use AI" checkbox
- Uses instant rule-based generation

**Solution 2:** Use quick buttons
- Pre-optimized prompts
- Faster than custom text

**Solution 3:** Restart Ollama
```powershell
# Stop Ollama
taskkill /F /IM ollama.exe

# Start again
ollama serve
```

### When Visualizations Error

**Check 1:** Verify columns exist
```
Go to "Data Analysis" tab → Check "Show dataset"
Verify column names match your prompt
```

**Check 2:** Use exact column names
```
# Instead of:
"Show income vs total spending"

# Try:
"Show Income vs MntTotal"  # Exact column names
```

**Check 3:** Simplify prompt
```
# Instead of:
"Create a sophisticated multi-dimensional scatter plot matrix..."

# Try:
"Scatter plot of Income vs MntTotal"
```

---

## 📝 Prompt Writing Best Practices

### 1. Be Specific
❌ Bad: "Show me something about customers"
✅ Good: "Create a bar chart comparing average MntTotal by education level"

### 2. Use Exact Column Names
❌ Bad: "Show total spending by education"
✅ Good: "Show MntTotal by education_Graduation"

### 3. Specify Chart Type
❌ Bad: "Compare income and spending"
✅ Good: "Scatter plot of Income vs MntTotal"

### 4. Request Sorting When Needed
❌ Bad: "Compare education spending"
✅ Good: "Compare education spending, sort descending"

### 5. Add Color for Context
❌ Bad: "Income vs spending"
✅ Good: "Income vs MntTotal colored by education_Graduation"

### 6. Use Professional Language
❌ Bad: "gimme income stuff lol"
✅ Good: "Show Income distribution as a box plot"

---

## 🎯 Real-World Business Questions

### Question 1: "Which customer segments are most valuable?"
**Prompts:**
```
1. "Show average MntTotal by education level, sorted descending"
2. "Scatter plot of Income vs MntTotal colored by marital status"
3. "Treemap of revenue by education level"
```

### Question 2: "Are our campaigns effective?"
**Prompts:**
```
1. "Calculate conversion rate using Response column"
2. "Compare acceptance rates across all AcceptedCmp columns"
3. "Show Response by education treemap"
```

### Question 3: "Who are our at-risk customers?"
**Prompts:**
```
1. "Scatter plot of Recency vs MntTotal"
2. "Histogram of Recency distribution"
3. "Plot NumWebVisitsMonth vs MntTotal"
```

### Question 4: "What drives customer spending?"
**Prompts:**
```
1. "Correlation heatmap of Income, Age, Recency, NumWebVisitsMonth, MntTotal"
2. "Scatter plot of Income vs MntTotal"
3. "Box plot of MntTotal by education level"
```

### Question 5: "How do families spend differently?"
**Prompts:**
```
1. "Compare MntTotal by Kidhome"
2. "Scatter plot of Kidhome vs MntTotal colored by Teenhome"
3. "Bar chart of MntRegularProds vs MntGoldProds by Kidhome"
```

---

## 🚀 Power User Tips

### Tip 1: Use Pre-built Dashboards First
- Click sidebar dashboard buttons
- Load 4-5 charts instantly
- Customize from there

### Tip 2: Chain Visualizations
- Create overview chart first
- Then drill into specifics
- Build narrative flow

### Tip 3: Combine Chart Types
- Start with KPI for context
- Add bar chart for comparison
- Use scatter for relationships
- Finish with heatmap for correlations

### Tip 4: Save Favorite Prompts
- Keep a text file of your best prompts
- Copy-paste for quick access
- Build your own dashboard templates

### Tip 5: Use Gallery for Comparisons
- Charts stay side-by-side
- Easy visual comparison
- Print or screenshot for presentations

---

## 📊 Sample Complete Analysis

### Scenario: "New Product Launch Strategy"

**Step 1: Identify Target Segment**
```
1. "Show average MntTotal by education level, sorted descending"
   → Result: PhDs spend most

2. "Scatter plot of Income vs MntTotal colored by education_PhD"
   → Result: Confirms PhDs have high income AND spending
```

**Step 2: Understand Their Preferences**
```
3. "Compare MntWines, MntMeatProducts, MntGoldProds for education_PhD"
   → Result: PhDs prefer wine and gold products

4. "Correlation heatmap of MntWines, MntGoldProds, Income for education_PhD"
   → Result: Strong correlation between income and premium products
```

**Step 3: Find Best Channel**
```
5. "Compare NumWebPurchases, NumCatalogPurchases, NumStorePurchases for education_PhD"
   → Result: PhDs prefer catalog purchases

6. "Plot NumWebVisitsMonth vs NumCatalogPurchases for education_PhD"
   → Result: High web visits lead to catalog orders
```

**Conclusion:** Launch premium product via catalog, target PhD segment, emphasize on website.

---

## 🎓 Learning Path

### Beginner (Week 1)
- Use pre-built dashboards only
- Click quick visualization buttons
- Learn by seeing examples

### Intermediate (Week 2-3)
- Write simple prompts
- Experiment with chart types
- Combine 2-3 visualizations

### Advanced (Week 4+)
- Write complex analysis prompts
- Create custom dashboards
- Chain multiple insights
- Present to stakeholders

---

## 📚 Additional Resources

### Column Reference
Check [README.md](README.md) for complete column list

### Architecture Details
See [ARCHITECTURE.md](ARCHITECTURE.md) for technical deep dive

### Quick Start
Follow [QUICKSTART.md](QUICKSTART.md) for setup

---

**Happy Analyzing! 📊**

_This guide is continuously updated based on user feedback and new use cases._
