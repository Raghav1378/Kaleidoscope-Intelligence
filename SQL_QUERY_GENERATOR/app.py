import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from sqlalchemy import create_engine
from langchain_core.prompts import PromptTemplate

st.set_page_config(page_title="Text-to-SQL Agent", page_icon="📊", layout="wide")

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found in .env file. Please add it!")
    st.stop()

db_path = "student.db"
if not os.path.exists(db_path):
    st.error(f"❌ Database file '{db_path}' not found! Please run 'python sqlite.py' first.")
    st.stop()

db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.title("📂 Database Schema")
st.sidebar.markdown("Here are the tables available for query:")
table_info = db.get_table_info()
st.sidebar.code(table_info, language="sql")

st.sidebar.markdown("---")
st.sidebar.subheader("🕒 Query History")
if st.session_state.history:
    for i, (q, sql) in enumerate(reversed(st.session_state.history[-5:])):
        st.sidebar.text(f"Q: {q}")
        st.sidebar.code(sql, language="sql")
else:
    st.sidebar.text("No history yet.")

llm = ChatGroq(
    groq_api_key=groq_api_key, 
    model_name="llama-3.1-8b-instant", 
    temperature=0
)

generate_query = create_sql_query_chain(llm, db)
execute_query = QuerySQLDataBaseTool(db=db)

st.title("📊 Enterprise AI SQL Agent")
st.markdown("""
> *Ask complex questions about your database.  
> **Try:** "Show me the top 5 students by marks", "Average attendance of Data Science class", or "Who is failing (marks < 40)?"*
""")

col1, col2 = st.columns([3, 1])

with col1:
    question = st.text_input("Enter your question:", placeholder="e.g., List all students in Section A with marks > 80")

if st.button("Generate & Run Query"):
    if question:
        with st.spinner("🤖 Analyzing Database Schema & Generating Query..."):
            try:
                response = generate_query.invoke({"question": question})
                cleaned_sql = response.strip()
                if "```sql" in cleaned_sql:
                    cleaned_sql = cleaned_sql.split("```sql")[1].split("```")[0].strip()
                elif "```" in cleaned_sql:
                    cleaned_sql = cleaned_sql.split("```")[1].strip()
                if "SQLQuery:" in cleaned_sql:
                    cleaned_sql = cleaned_sql.split("SQLQuery:")[1].strip()

                engine = create_engine(f"sqlite:///{db_path}")
                
                try:
                    if cleaned_sql.lower().startswith("select"):
                        pd.read_sql_query(cleaned_sql, engine) 
                    else:
                        execute_query.invoke(cleaned_sql)
                except Exception as e:
                    fix_prompt = f"The following SQL query failed: {cleaned_sql}\nError: {e}\nRegenerate a correct SQL query for the question: {question}"
                    response = generate_query.invoke({"question": fix_prompt})
                    cleaned_sql = response.strip()
                    if "```sql" in cleaned_sql:
                        cleaned_sql = cleaned_sql.split("```sql")[1].split("```")[0].strip()
                    elif "```" in cleaned_sql:
                        cleaned_sql = cleaned_sql.split("```")[1].strip()
                    if "SQLQuery:" in cleaned_sql:
                        cleaned_sql = cleaned_sql.split("SQLQuery:")[1].strip()
                    st.warning("⚠️ Initial query failed. AI auto-corrected the SQL.")

                st.session_state.history.append((question, cleaned_sql))
                
                st.success("✅ Generated SQL Query:")
                st.code(cleaned_sql, language="sql")

                if cleaned_sql.lower().startswith("select"):
                    df = pd.read_sql_query(cleaned_sql, engine)
                    st.info(f"📊 Query Result ({len(df)} rows found):")
                    
                    if not df.empty:
                        tab1, tab2 = st.tabs(["📄 Data Table", "📈 Visualization"])
                        
                        with tab1:
                            st.dataframe(df, use_container_width=True)
                            csv = df.to_csv(index=False).encode('utf-8')
                            st.download_button("📥 Download CSV", data=csv, file_name="query_results.csv", mime="text/csv")
                        
                        with tab2:
                            numeric_df = df.select_dtypes(include=['number'])
                            if not numeric_df.empty:
                                st.bar_chart(numeric_df)
                            else:
                                st.write("No numeric data available for visualization.")
                    else:
                        st.warning("Query executed successfully, but returned 0 results.")
                else:
                    result = execute_query.invoke(cleaned_sql)
                    st.write(result)
                
            except Exception as e:
                st.error(f"❌ Error Processing Query: {e}")
    else:
        st.warning("Please enter a question first!")

st.markdown("---")
st.markdown("Built with **LangChain** & **Groq** | Created by Raghav Ramani")