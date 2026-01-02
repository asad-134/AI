import streamlit as st
import pandas as pd
import sqlite3
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import time

# Page configuration
st.set_page_config(
    page_title="CSV Query Assistant",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 CSV Query Assistant with AI")
st.markdown("Upload a CSV file, and ask questions about your data using natural language!")

# Sidebar for API key
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter your Google API Key:", type="password")
    
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        st.success("✅ API Key set!")
    else:
        st.warning("⚠️ Please enter your Google API Key")
        st.markdown("[Get API Key](https://aistudio.google.com/app/apikey)")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This app uses Gemini AI to answer questions about your CSV data.")

# Initialize session state
if 'db_ready' not in st.session_state:
    st.session_state.db_ready = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'table_name' not in st.session_state:
    st.session_state.table_name = None

def clean_column_name(col):
    """Clean column names to be SQL-friendly"""
    col = str(col).strip()
    col = col.replace(' ', '_')
    col = col.replace('-', '_')
    col = ''.join(c for c in col if c.isalnum() or c == '_')
    if col[0].isdigit():
        col = 'col_' + col
    return col.lower()

def process_csv_to_db(uploaded_file, table_name='user_data'):
    """Process uploaded CSV and store in SQLite database"""
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        
        # Clean column names
        df.columns = [clean_column_name(col) for col in df.columns]
        
        # Connect to database
        conn = sqlite3.connect('user_data.db')
        
        # Drop table if exists and create new one
        cursor = conn.cursor()
        cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
        
        # Store DataFrame to SQL
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        conn.commit()
        conn.close()
        
        return True, df, None
    except Exception as e:
        return False, None, str(e)

def create_agent():
    """Create LangChain SQL agent"""
    if not os.environ.get("GOOGLE_API_KEY"):
        return None
    
    db = SQLDatabase.from_uri("sqlite:///user_data.db")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0
    )
    
    agent = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="zero-shot-react-description",
        verbose=True,
        max_iterations=10,
        max_execution_time=60
    )
    
    return agent

def ask_question(agent, question):
    """Ask a question to the agent with retry logic"""
    max_retries = 2
    for attempt in range(max_retries):
        try:
            response = agent.invoke({"input": question})
            return response['output'], None
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                if attempt < max_retries - 1:
                    time.sleep(3)
                else:
                    return None, "Rate limit exceeded. Please wait a moment and try again."
            else:
                return None, f"Error: {str(e)}"

# Main app layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📁 Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file is not None:
        # Display file info
        st.info(f"File uploaded: {uploaded_file.name}")
        
        # Process button
        if st.button("🔄 Process and Load Data", type="primary"):
            with st.spinner("Processing CSV file..."):
                success, df, error = process_csv_to_db(uploaded_file, 'user_data')
                
                if success:
                    st.session_state.db_ready = True
                    st.session_state.table_name = 'user_data'
                    st.success("✅ Data loaded successfully!")
                    
                    # Show preview
                    st.subheader("📋 Data Preview")
                    st.dataframe(df.head(10), width ='stretch')
                    
                    # Show statistics
                    st.subheader("📊 Data Statistics")
                    st.write(f"**Rows:** {len(df)}")
                    st.write(f"**Columns:** {len(df.columns)}")
                    st.write(f"**Column Names:** {', '.join(df.columns)}")
                else:
                    st.error(f"❌ Error processing file: {error}")

with col2:
    st.header("💬 Ask Questions")
    
    if not api_key:
        st.warning("⚠️ Please enter your Google API Key in the sidebar first.")
    elif not st.session_state.db_ready:
        st.info("📤 Please upload and process a CSV file first.")
    else:
        # Question input
        question = st.text_input(
            "Ask a question about your data:",
            placeholder="e.g., What is the average value? How many rows are there?"
        )
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            ask_btn = st.button("🚀 Ask", type="primary")
        with col_btn2:
            if st.button("🗑️ Clear History"):
                st.session_state.chat_history = []
                st.rerun()
        
        if ask_btn and question:
            with st.spinner("🤔 Thinking..."):
                agent = create_agent()
                
                if agent:
                    answer, error = ask_question(agent, question)
                    
                    if answer:
                        # Add to chat history
                        st.session_state.chat_history.append({
                            "question": question,
                            "answer": answer
                        })
                    else:
                        st.error(f"❌ {error}")
                else:
                    st.error("❌ Could not create agent. Check your API key.")
        
        # Display chat history
        if st.session_state.chat_history:
            st.subheader("💭 Conversation History")
            
            for i, chat in enumerate(reversed(st.session_state.chat_history)):
                with st.container():
                    st.markdown(f"**Q{len(st.session_state.chat_history)-i}:** {chat['question']}")
                    st.markdown(f"**A:** {chat['answer']}")
                    st.markdown("---")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with Streamlit, LangChain, and Google Gemini</p>
    </div>
    """,
    unsafe_allow_html=True
)
