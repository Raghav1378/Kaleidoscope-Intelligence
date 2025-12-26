import streamlit as st
import os
import pandas as pd
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from sqlalchemy import create_engine
from langchain_core.prompts import PromptTemplate

# 1. PAGE SETUP
st.set_page_config(page_title="Prism-SQL", page_icon="💎", layout="wide")

# 2. SIDEBAR - API KEY INPUT
st.sidebar.title("🔑 Configuration")
st.sidebar.markdown("Enter your Groq API Key below to activate the agent.")

# A. User Input (Highest Priority)
user_api_key = st.sidebar.text_input("Groq API Key", type="password", placeholder="gsk_...")

# B. Auto-Load from Secrets/Env (Fallback)
default_api_key = None
try:
    default_api_key = st.secrets["GROQ_API_KEY"]
except (FileNotFoundError, KeyError):
    try:
        from dotenv import load_dotenv
        load_dotenv()
        default_api_key = os.getenv("GROQ_API_KEY")
    except:
        pass

# C. Final Key Selection
groq_api_key = user_api_key if user_api_key else default_api_key

# 3. STOP IF NO KEY
if not groq_api_key:
    st.info("ℹ️ **To get started:** Please paste your Groq API Key in the sidebar.")
    st.markdown("""
    **Don't have a key?** 1. Go to [Groq Console](https://console.groq.com/keys) (It's free!)  
    2. Create a new API Key.  
    3. Paste it here.
    """)
    st.stop()

# 4. DATABASE SETUP
# Create the database file if it doesn't exist (for demo purposes)
db_path = "student.db"

if not os.path.exists(db_path):
    # Optional: You can create a dummy DB here if needed, or just warn the user.
    # For now, we assume you pushed the file.
    st.error(f"❌ Database file '{db_path}' not found! Please ensure 'student.db' is in the repository.")
    st.stop()

db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

# 5. SESSION STATE (History)
if "history" not in st.session_state:
    st.session_state.history = []

# 6. SIDEBAR - DB INFO
st.sidebar.markdown("---")
st.sidebar.title("📂 Database Schema")
try:
    table_info = db.get_table_info()
    st.sidebar.code(table_info, language="sql")
except Exception as e:
    st.sidebar.error(f"Error reading table info: {e}")

st.sidebar.subheader("🕒 Query History")
if st.session_state.history:
    for i, (q, sql) in enumerate(reversed(st.session_state.history[-5:])):
        st.sidebar.text(f"Q: {q}")
        st.sidebar.code(sql, language="sql")
else:
    st.sidebar.text("No history yet.")

# 7. INITIALIZE AGENT
try:
    llm = ChatGroq(
        groq_api_key=groq_api_key, 
        model_name="llama-3.1-8b-instant", 
        temperature=0
    )
    generate_query = create_sql_query_chain(llm, db)
    execute_query = QuerySQLDataBaseTool(db=db)
except Exception as e:
    st.error(f"❌ Error initializing AI: {e}")
    st.stop()

# 8. MAIN UI
st.title("💎 Prism-SQL: Enterprise Database Agent")
st.markdown("""
> *Translate plain English into powerful SQL queries.* > **Try:** "Show me the top 5 students by marks", "Who failed in Section A?", or "Average marks per section".
""")

col1, col2 = st.columns([3, 1])

with col1:
    question = st.text_input("Enter your question:", placeholder="e.g., List all students in Section A with marks > 80")

if st.button("Refract Query 🌈"):
    if question:
        with st.spinner("Refracting logic through the prism..."):
            try:
                # A. Generate Query
                response = generate_query.invoke({"question": question})
                
                # B. Clean Query
                cleaned_sql = response.strip()
                if "```sql" in cleaned_sql:
                    cleaned_sql = cleaned_sql.split("```sql")[1].split("```")[0].strip()
                elif "```" in cleaned_sql:
                    cleaned_sql = cleaned_sql.split("```")[1].strip()
                if "SQLQuery:" in cleaned_sql:
                    cleaned_sql = cleaned_sql.split("SQLQuery:")[1].strip()

                engine = create_engine(f"sqlite:///{db_path}")
                
                # C. Execute or Auto-Correct
                try:
                    # Check if it's a SELECT query (safe to run)
                    if cleaned_sql.lower().startswith("select"):
                        pd.read_sql_query(cleaned_sql, engine) 
                    else:
                        execute_query.invoke(cleaned_sql)
                except Exception as e:
                    # Auto-Correction
                    fix_prompt = f"The following SQL query failed: {cleaned_sql}\nError: {e}\nRegenerate a correct SQL query for the question: {question}"
                    response = generate_query.invoke({"question": fix_prompt})
                    
                    cleaned_sql = response.strip()
                    if "```sql" in cleaned_sql:
                        cleaned_sql = cleaned_sql.split("```sql")[1].split("```")[0].strip()
                    elif "```" in cleaned_sql:
                        cleaned_sql = cleaned_sql.split("```")[1].strip()
                    
                    st.warning("⚠️ Initial query failed. AI auto-corrected the SQL.")

                # D. Save to History
                st.session_state.history.append((question, cleaned_sql))
                
                # E. Show Result
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