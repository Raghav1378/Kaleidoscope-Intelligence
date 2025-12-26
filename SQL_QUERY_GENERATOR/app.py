import streamlit as st
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# LangChain Core & Specialized Imports
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain.chains import create_sql_query_chain
from langchain_community.tools import QuerySQLDatabaseTool 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Prism-SQL | Enterprise AI", 
    page_icon="💎", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a sleek "Agentic" look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stTextInput>div>div>input { border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR - SECURE CONFIGURATION
with st.sidebar:
    st.title("💎 Prism-SQL")
    st.caption("Advanced NLP-to-SQL Engine")
    st.divider()
    
    st.subheader("🔑 Configuration")
    user_api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    
    # Load Key logic
    default_api_key = None
    try:
        default_api_key = st.secrets["GROQ_API_KEY"]
    except:
        load_dotenv()
        default_api_key = os.getenv("GROQ_API_KEY")
    
    groq_api_key = user_api_key if user_api_key else default_api_key

    if not groq_api_key:
        st.warning("⚠️ Please provide an API Key to proceed.")
        st.stop()
    
    st.success("API Key Active")
    st.divider()

# 3. DATABASE SETUP
db_path = "student.db"
if not os.path.exists(db_path):
    st.error("❌ student.db not found in the root directory.")
    st.stop()

db_uri = f"sqlite:///{db_path}"
db = SQLDatabase.from_uri(db_uri)
engine = create_engine(db_uri)

# 4. PROMPT ENGINEERING (Few-Shot Strategy)
examples = [
    {"input": "Top 5 students?", "query": "SELECT Name, Marks FROM STUDENT ORDER BY Marks DESC LIMIT 5;"},
    {"input": "Avg marks in Section A", "query": "SELECT AVG(Marks) AS Average_Marks FROM STUDENT WHERE Section = 'A';"},
    {"input": "Count students by section", "query": "SELECT Section, COUNT(ID) AS Student_Count FROM STUDENT GROUP BY Section;"}
]

example_prompt = ChatPromptTemplate.from_messages([("human", "{input}"), ("ai", "{query}")])
few_shot_prompt = FewShotChatMessagePromptTemplate(example_prompt=example_prompt, examples=examples)

# FIXED: Added {table_info} and {top_k} to satisfy the create_sql_query_chain requirements
final_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run.
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    
    Only use the following tables:
    {table_info}
    
    Return ONLY raw SQL. No markdown. Use 'AS' for naming calculated columns."""),
    few_shot_prompt,
    ("human", "{input}"),
])

# 5. INITIALIZE AGENT
@st.cache_resource
def get_agent(_api_key):
    llm = ChatGroq(groq_api_key=_api_key, model_name="llama-3.1-8b-instant", temperature=0)
    gen_chain = create_sql_query_chain(llm, db, prompt=final_prompt)
    exec_tool = QuerySQLDatabaseTool(db=db)
    return gen_chain, exec_tool

generate_query, execute_query = get_agent(groq_api_key)

# 6. SIDEBAR - SCHEMA & HISTORY
with st.sidebar:
    st.subheader("📂 Database Schema")
    with st.expander("View Tables"):
        st.code(db.get_table_info(), language="sql")
    
    if "history" not in st.session_state:
        st.session_state.history = []
    
    st.subheader("🕒 History")
    if st.session_state.history:
        if st.button("Clear Logs"):
            st.session_state.history = []
            st.rerun()
        for q, s in reversed(st.session_state.history[-3:]):
            st.caption(f"Q: {q}")

# 7. MAIN UI LAYOUT
st.title("📊 Enterprise AI SQL Agent")
st.info("Directly query your database using natural language.")

query_input = st.text_input("Ask your database:", placeholder="e.g., Who is the topper in Section B?")

if st.button("Generate Insights 🚀"):
    if query_input:
        with st.spinner("Refracting through the Prism..."):
            try:
                # A. Intelligence Layer
                sql_response = generate_query.invoke({"question": query_input})
                
                # B. Robust Cleaning
                clean_sql = sql_response.strip()
                if "SELECT" in clean_sql.upper():
                    clean_sql = clean_sql[clean_sql.upper().find("SELECT"):]
                clean_sql = clean_sql.split(';')[0]
                
                st.session_state.history.append((query_input, clean_sql))

                # C. Display & Tabs
                st.subheader("🔍 Analysis Result")
                st.code(clean_sql, language="sql")
                
                df = pd.read_sql_query(clean_sql, engine)

                if not df.empty:
                    tab1, tab2 = st.tabs(["📄 Data Preview", "📈 Smart Visualization"])
                    
                    with tab1:
                        st.dataframe(df, use_container_width=True)
                        st.download_button("📥 Export CSV", df.to_csv(index=False), "export.csv")
                    
                    with tab2:
                        # Logic to prevent visualization errors
                        nums = df.select_dtypes(include=['number']).columns.tolist()
                        cats = df.select_dtypes(include=['object']).columns.tolist()
                        
                        if nums:
                            if cats:
                                st.bar_chart(df.set_index(cats[0])[nums[0]])
                            else:
                                st.bar_chart(df[nums[0]])
                        else:
                            st.warning("No numeric data found to plot a chart.")
                else:
                    st.warning("No records found for this query.")
                    
            except Exception as e:
                st.error(f"Execution Error: {e}")
    else:
        st.warning("Please enter a question.")

# 8. FOOTER
st.markdown("---")
st.markdown("<h4 style='text-align: center;'>Built with ❤️ by Raghav Ramani</h4>", unsafe_allow_html=True)
st.center = st.markdown("<p style='text-align: center; color: grey;'>Agentic AI Portfolio Project v1.0</p>", unsafe_allow_html=True)