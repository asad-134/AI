"""
Dashboard Templates - Pre-configured prompts for common business questions
"""

# Dashboard 1: Campaign Success & Engagement
CAMPAIGN_DASHBOARD = {
    'name': 'Campaign Success & Engagement',
    'description': 'Analyze marketing campaign effectiveness and customer engagement',
    'prompts': [
        {
            'title': 'Conversion Rate KPI',
            'prompt': 'Calculate the conversion rate using the Response column. If it\'s below 15%, color the metric red.',
            'chart_type': 'kpi'
        },
        {
            'title': 'Education vs Spending',
            'prompt': 'Compare the average MntTotal across all education_ categories. Sort descending to show which education level spends the most.',
            'chart_type': 'bar'
        },
        {
            'title': 'Spending Drivers Correlation',
            'prompt': 'Show a correlation heatmap between Income, Recency, MntWines, and NumWebVisitsMonth to find spending drivers.',
            'chart_type': 'heatmap'
        },
        {
            'title': 'Campaign Acceptance by Education',
            'prompt': 'Create a bar chart comparing the sum of all AcceptedCmp columns by education level',
            'chart_type': 'bar'
        }
    ]
}

# Dashboard 2: Family & Spending Habits
FAMILY_DASHBOARD = {
    'name': 'Family & Spending Habits',
    'description': 'Understand how family composition affects purchasing behavior',
    'prompts': [
        {
            'title': 'Product Type by Children',
            'prompt': 'Compare MntRegularProds vs MntGoldProds based on the number of children (Kidhome).',
            'chart_type': 'bar'
        },
        {
            'title': 'Income-Spending Relationship',
            'prompt': 'Plot Income vs MntTotal. Color the points by education_Graduation to see if higher education correlates with higher income/spend.',
            'chart_type': 'scatter'
        },
        {
            'title': 'Revenue by Household Type',
            'prompt': 'Create a treemap of MntTotal grouped by marital_ status categories to see which household type contributes most to revenue.',
            'chart_type': 'treemap'
        },
        {
            'title': 'Family Size Distribution',
            'prompt': 'Show the distribution of total family members (Kidhome + Teenhome) with a histogram',
            'chart_type': 'histogram'
        }
    ]
}

# Dashboard 3: Customer Behavior Analysis
BEHAVIOR_DASHBOARD = {
    'name': 'Customer Behavior Analysis',
    'description': 'Deep dive into customer purchase patterns and engagement',
    'prompts': [
        {
            'title': 'Recency vs Spending',
            'prompt': 'Create a scatter plot of Recency vs MntTotal to identify at-risk high-value customers',
            'chart_type': 'scatter'
        },
        {
            'title': 'Web Visits vs Purchases',
            'prompt': 'Plot NumWebVisitsMonth vs NumWebPurchases to understand conversion efficiency',
            'chart_type': 'scatter'
        },
        {
            'title': 'Purchase Channel Comparison',
            'prompt': 'Compare NumWebPurchases, NumCatalogPurchases, and NumStorePurchases with a bar chart',
            'chart_type': 'bar'
        },
        {
            'title': 'Deals vs Regular Purchases',
            'prompt': 'Show relationship between NumDealsPurchases and MntTotal',
            'chart_type': 'scatter'
        }
    ]
}

# Dashboard 4: Demographics & Segmentation
DEMOGRAPHICS_DASHBOARD = {
    'name': 'Demographics & Segmentation',
    'description': 'Analyze customer segments based on demographic characteristics',
    'prompts': [
        {
            'title': 'Age Distribution',
            'prompt': 'Create a histogram of Age distribution to understand customer age segments',
            'chart_type': 'histogram'
        },
        {
            'title': 'Income Distribution',
            'prompt': 'Show Income distribution with a box plot',
            'chart_type': 'box'
        },
        {
            'title': 'Age vs Income',
            'prompt': 'Plot Age vs Income colored by education level',
            'chart_type': 'scatter'
        },
        {
            'title': 'Marital Status Revenue',
            'prompt': 'Compare total revenue (MntTotal) across different marital status categories',
            'chart_type': 'bar'
        }
    ]
}

# Dashboard 5: Product Category Analysis
PRODUCT_DASHBOARD = {
    'name': 'Product Category Performance',
    'description': 'Analyze performance across different product categories',
    'prompts': [
        {
            'title': 'Product Category Comparison',
            'prompt': 'Create a bar chart comparing average spending across MntWines, MntFruits, MntMeatProducts, MntFishProducts, MntSweetProducts, MntGoldProds',
            'chart_type': 'bar'
        },
        {
            'title': 'Wine Spending Correlation',
            'prompt': 'Show correlation between MntWines and Income with a scatter plot',
            'chart_type': 'scatter'
        },
        {
            'title': 'Product Mix Heatmap',
            'prompt': 'Create a correlation heatmap of all Mnt spending columns',
            'chart_type': 'heatmap'
        },
        {
            'title': 'Gold vs Regular Products',
            'prompt': 'Compare MntGoldProds vs MntRegularProds by Income quartiles',
            'chart_type': 'bar'
        }
    ]
}

# All dashboards
ALL_DASHBOARDS = [
    CAMPAIGN_DASHBOARD,
    FAMILY_DASHBOARD,
    BEHAVIOR_DASHBOARD,
    DEMOGRAPHICS_DASHBOARD,
    PRODUCT_DASHBOARD
]


def get_dashboard_by_name(name: str):
    """Get a specific dashboard configuration by name"""
    for dashboard in ALL_DASHBOARDS:
        if dashboard['name'].lower() == name.lower():
            return dashboard
    return None


def get_all_dashboard_names():
    """Get list of all available dashboard names"""
    return [d['name'] for d in ALL_DASHBOARDS]


def get_prompts_for_dashboard(dashboard_name: str):
    """Get all prompts for a specific dashboard"""
    dashboard = get_dashboard_by_name(dashboard_name)
    if dashboard:
        return dashboard['prompts']
    return []


# Custom analysis prompts for the LLM
ANALYSIS_PROMPTS = {
    'high_value_customers': """
Analyze the dataset to identify characteristics of high-value customers.
Look at Income, MntTotal, and education levels.
Provide 3-5 key insights about who spends the most.
""",
    
    'campaign_effectiveness': """
Analyze campaign acceptance rates across different customer segments.
Consider education, income, and family composition.
Suggest which segments to target in future campaigns.
""",
    
    'churn_risk': """
Identify customers at risk of churning based on:
- High Recency (haven't purchased recently)
- Low web visits
- Previously high spenders
Provide recommendations for retention strategies.
""",
    
    'product_recommendations': """
Analyze product category preferences by customer segment.
Look for patterns in MntWines, MntMeatProducts, etc.
Suggest cross-selling opportunities.
""",
    
    'channel_optimization': """
Compare performance across purchase channels:
- Web purchases
- Catalog purchases  
- Store purchases
Recommend where to invest marketing resources.
"""
}


def get_analysis_prompt(analysis_type: str):
    """Get a specific analysis prompt template"""
    return ANALYSIS_PROMPTS.get(analysis_type, "")


def get_all_analysis_types():
    """Get list of all available analysis types"""
    return list(ANALYSIS_PROMPTS.keys())
