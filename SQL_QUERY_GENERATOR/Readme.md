# 📊 AI-Powered SQL Query Generator (Text-to-SQL Agent)

> *"Bridging the gap between non-technical stakeholders and complex databases using Generative AI."*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/LLM-OpenAI%20%2F%20Groq-412991?style=for-the-badge&logo=openai)](https://openai.com/)

## 📝 Project Overview

This project is an **autonomous Text-to-SQL Agent** designed to democratize data access. It allows users to ask questions in plain English (e.g., *"Who are the top 5 customers by revenue?"*) and instantly retrieves accurate data from a SQL database.

Unlike simple wrappers, this system features a **decoupled architecture** with a robust **FastAPI backend** for query logic and a responsive **Streamlit frontend** for user interaction. It handles schema awareness, error correction, and query optimization.

---

## 🚀 Key Features

### 1. 🗣️ Natural Language to SQL
* Converts complex human questions into optimized SQL queries using **GPT-4** (or Llama-3 via Groq).
* Understand context, filters (WHERE clauses), and aggregations (GROUP BY).

### 2. 🔌 Dynamic Database Connection
* Connects to SQL databases (MySQL/SQLite) dynamically.
* **Schema Awareness:** The agent automatically fetches table structures to ensure queries use valid column names.

### 3. ⚡ High-Performance Architecture
* **Backend:** Built with **FastAPI** to serve REST endpoints for query generation and execution.
* **Frontend:** Interactive **Streamlit** dashboard for querying, visualizing data tables, and reviewing generated SQL code.

### 4. 🛡️ Query Optimization & Safety
* Includes validation steps to prevent common SQL syntax errors.
* Displays the raw SQL before execution for transparency and debugging.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **LLM Engine** | OpenAI GPT-4 / Groq | The brain converting text to SQL logic. |
| **Backend** | FastAPI | High-performance API handling database logic. |
| **Frontend** | Streamlit | User-friendly interface for non-tech users. |
| **Database** | MySQL / SQLite | Relational database storage. |
| **Language** | Python 3.10+ | Core logic and orchestration. |

---

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.10+
* An OpenAI API Key (or Groq API Key)
* MySQL Database (optional, can use SQLite)

### 1. Clone the Repository
```bash
git clone [https://github.com/Raghav1378/Kaleidoscope-Intelligence.git](https://github.com/Raghav1378/Kaleidoscope-Intelligence.git)
cd Kaleidoscope-Intelligence/SQL_Query_Generator
``` 
### 2. Create a Virtual Environment
```bash
python -m venv venv
``` 
### 3. Install Dependencies
```bash
pip install -r requirements.txt
``` 
### 4. Set Up Environment Variables
Create a .env file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_NAME=your_database_name
```

### 5. Run the Application
```bash
streamlit run app.py
```

--- 
## 👨‍💻 Founder & Developer

### **Raghav Ramani**
*Aspiring AI/ML Engineer & Data Analyst*

I am a final-year Computer Science student specializing in **Artificial Intelligence** and **Machine Learning** at **JECRC University**. My passion lies in building "Agentic AI" systems that solve real-world operational inefficiencies.

* **📍 Focus Areas:** Generative AI, Retrieval-Augmented Generation (RAG), MLOps, and Data Analytics.
* **💡 Philosophy:** "Code should not just function; it should solve a problem gracefully."
* **🎯 Short-Term Goal:** Transitioning into a professional Data Analyst role by Sept 2025.

**🔗 Connect with me:**
* **LinkedIn:** [Raghav Ramani](https://www.linkedin.com/in/raghavramani/)
* **GitHub:** [@Raghav1378](https://github.com/Raghav1378)
* **Portfolio:** [Kaleidoscope Intelligence](https://github.com/Raghav1378/Kaleidoscope-Intelligence)

---

## 📄 License

This project is open-source and available under the **MIT License**.