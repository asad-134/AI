# Migration Guide: Ollama Mistral 7B → OpenRouter Gemma3 27B

## Changes Made

### 1. **agent_coordinator.py**
- Removed Ollama dependency
- Added OpenRouter API integration using `requests` library
- Changed model from `mistral:7b` to `google/gemma-2-27b-it`
- Updated method names:
  - `query_ollama()` → `query_llm()`
  - `ollama_available` → `llm_available`
  - `use_ollama` parameter → `use_llm`

### 2. **app.py**
- Updated UI text from "Ollama" to "OpenRouter"
- Updated model status display
- Changed "Use AI" checkbox help text
- Updated footer to show "Powered by OpenRouter Gemma3 27B"

### 3. **requirements.txt**
- Removed: `ollama==0.1.6`, `langchain`, `langchain-community`, `langchain-experimental`
- Added: `requests==2.31.0`

### 4. **New Files**
- `setup_openrouter.py` - Script to configure API key

## Setup Instructions

### Step 1: Get OpenRouter API Key

1. Visit https://openrouter.ai/
2. Sign up or log in
3. Navigate to **Keys** section
4. Create a new API key
5. Copy the key (starts with `sk-or-v1-...`)

### Step 2: Configure API Key

**Option A: Using setup script (Recommended)**
```bash
python setup_openrouter.py
```
Follow the prompts to save your API key.

**Option B: Manual configuration (Windows)**
```powershell
# Set user environment variable
[System.Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY', 'your-api-key-here', 'User')

# Restart your terminal/IDE
```

**Option C: Manual configuration (Linux/Mac)**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export OPENROUTER_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Option D: Using .env file**
```bash
# Create .env file in project directory
echo "OPENROUTER_API_KEY=your-api-key-here" > .env

# Install python-dotenv
pip install python-dotenv

# Load in your code (already handled in agent_coordinator.py)
```

### Step 3: Install Dependencies

```bash
pip install requests==2.31.0
```

Or reinstall all:
```bash
pip install -r requirements.txt
```

### Step 4: Run the Dashboard

```bash
streamlit run app.py
```

## Verify Setup

Check if API key is configured:
```python
import os
print(os.getenv('OPENROUTER_API_KEY'))
```

Should output: `sk-or-v1-...` (your API key)

## Model Information

**OpenRouter Gemma3 27B (google/gemma-2-27b-it)**
- **Parameters:** 27 billion (vs Mistral 7B's 7 billion)
- **Context Window:** 8,192 tokens
- **Provider:** Google via OpenRouter
- **Cost:** ~$0.27 per million tokens (input), ~$1.08 per million tokens (output)
- **Advantages:**
  - Larger model = better code generation
  - Better instruction following
  - More consistent output format
  - Cloud-based = no local GPU needed

## Fallback Behavior

If OpenRouter API key is not configured:
- ⚠️ Warning message shown in UI
- Automatically falls back to **rule-based visualization generation**
- All features still work, just without LLM enhancement

## Testing

Test the integration:
```python
from agent_coordinator import AgentCoordinator
import pandas as pd

# Initialize coordinator
coordinator = AgentCoordinator()

# Check status
status = coordinator.get_model_status()
print(f"LLM Available: {status['llm_available']}")
print(f"Model: {status['model_name']}")
print(f"API Configured: {status['api_configured']}")

# Test query (if API key configured)
if status['llm_available']:
    response = coordinator.query_llm("Say hello!")
    print(f"Response: {response}")
```

## Cost Estimation

For typical dashboard usage:
- **Per visualization:** ~500-1000 tokens = $0.0003-$0.001
- **100 visualizations/day:** ~$0.03-$0.10/day
- **Monthly (active use):** ~$1-$3/month

Much cheaper than running local GPU 24/7!

## Troubleshooting

### "OpenRouter API key not found"
- API key not set in environment
- Restart terminal/IDE after setting
- Check with: `echo %OPENROUTER_API_KEY%` (Windows) or `echo $OPENROUTER_API_KEY` (Linux/Mac)

### "Error querying OpenRouter: 401"
- Invalid API key
- Check key at https://openrouter.ai/keys

### "Error querying OpenRouter: 429"
- Rate limit exceeded
- Wait a few seconds and retry
- Consider upgrading OpenRouter plan

### "Connection timeout"
- Check internet connection
- Verify firewall settings
- Try again in a few seconds

## Rollback (if needed)

To revert to Ollama:
```bash
git checkout agent_coordinator.py app.py requirements.txt
pip install ollama==0.1.6
ollama pull mistral:7b
```

## Support

- **OpenRouter Docs:** https://openrouter.ai/docs
- **Gemma2 Model Card:** https://openrouter.ai/models/google/gemma-2-27b-it
- **Dashboard Issues:** Open issue in repository
