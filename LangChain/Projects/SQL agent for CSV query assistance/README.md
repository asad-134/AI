# 📊 CSV Query Assistant with AI

A powerful Streamlit application that allows you to upload CSV files and query your data using natural language questions.  Powered by Google's Gemini AI and LangChain, this app converts your questions into SQL queries and returns intelligent answers about your data.

![CSV Query Assistant Screenshot](![image1](image1))

## ✨ Features

- **📁 CSV File Upload**: Easy drag-and-drop or browse interface for uploading CSV files (up to 200MB)
- **🤖 Natural Language Queries**: Ask questions about your data in plain English
- **🔄 Real-time Data Processing**: Automatic conversion of CSV data to SQLite database
- **💬 Conversation History**: Track all your questions and answers in one place
- **📊 Data Preview**: View your uploaded data and statistics
- **🔐 Secure API Key Management**: Safe handling of your Google API key

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google API Key (Get one from [Google AI Studio](https://aistudio.google.com/app/apikey))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/asad-134/AI.git
cd "AI/LangChain/Projects/SQL agent for CSV query assistance"
```

2. Install required dependencies:
```bash
pip install streamlit pandas sqlite3 langchain-community langchain-google-genai
```

### Running the Application

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically `http://localhost:8501`)

## 📖 How to Use

### Step 1: Configure API Key
1. Enter your Google API Key in the sidebar configuration section
2. Wait for the "API Key set!" confirmation message

### Step 2: Upload Your Data
1. Click on "Browse files" or drag and drop your CSV file
2. Click the "Process and Load Data" button
3. Review the data preview and statistics

### Step 3: Ask Questions
1. Type your question in natural language in the "Ask Questions" section
2. Click the "Ask" button
3. View the AI-generated answer based on your data

### Example Questions
- "What is the average value of column X?"
- "How many rows are in the dataset?"
- "Show me the top 5 entries by sales"
- "What is the total sum of revenue?"
- "Average EMI per month for people who monthly balance upto 500"

## 🛠️ Technical Details

### Technologies Used
- **Streamlit**:  Web application framework
- **Pandas**: Data manipulation and analysis
- **SQLite3**: Database for storing CSV data
- **LangChain**: Framework for building LLM applications
- **Google Gemini AI**: Large language model for query understanding and generation

### Key Components

#### Data Processing
- Automatic column name cleaning for SQL compatibility
- Conversion of CSV data to SQLite database
- Data validation and error handling

#### AI Agent
- Uses Gemini 2.5 Flash Lite model
- Zero-shot React description agent type
- Maximum 10 iterations with 60-second execution timeout
- Rate limit handling with retry logic

## 📋 Features Breakdown

### Configuration Panel
- Secure API key input with password masking
- Real-time validation
- Quick access to API key generation link

### Upload Section
- File size display
- Data preview with first 10 rows
- Statistics including row count, column count, and column names

### Query Section
- Text input for natural language questions
- Real-time processing indicator
- Clear history functionality
- Conversation tracking with Q&A pairs

## 🔒 Security

- API keys are stored in environment variables
- Password-type input fields for sensitive data
- No data is stored permanently on the server

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the application.

## 📝 License

This project is part of the [AI Repository](https://github.com/asad-134/AI) - A repository for AI-related projects and content. 

## 👤 Author

**asad-134**
- GitHub: [@asad-134](https://github.com/asad-134)

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://langchain.com/)
- AI model by [Google Gemini](https://deepmind.google/technologies/gemini/)

---

<div align="center">
Made with ❤️ using Streamlit, LangChain, and Google Gemini
</div>
