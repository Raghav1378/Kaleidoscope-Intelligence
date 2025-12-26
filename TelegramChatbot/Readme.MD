# 🌑 Itachi Uchiha AI Bot (Telegram)

> *"People live their lives bound by what they accept as correct and true. That is how they define 'Reality'."*

A sophisticated Telegram Bot powered by **Llama 3.1 (via Groq)** and **LangChain**. It features dual-personality modes: a philosophical conversationalist and a technical code reviewer ("Sharingan Mode").

Built by **Raghav Ramani** as a showcase of Generative AI integration, State Management, and Async Python architecture.

---

## 🚀 Key Features

### 1. 🧠 Context-Aware Memory
Utilizes **LangChain** to maintain conversation history. It remembers the last 10 exchanges, allowing for coherent, multi-turn conversations rather than isolated Q&A.

### 2. 👁️ Dual Modes (Prompt Engineering)
The bot dynamically switches system prompts based on user commands:
* **Default Mode (Itachi):** Philosophical, calm, mysterious. Uses metaphors and anime lore.
* **🔴 Sharingan Mode (Debug):** A strict, analytical Senior Software Engineer. Analyzes code snippets for bugs, Big O complexity, and logic errors.

### 3. 📡 Admin Broadcast System
Includes a secure `admin_id` check allowing the owner to send mass notifications to all active users simultaneously.

### 4. ⚡ High-Performance Architecture
* **Groq API:** Utilizes the LPU (Language Processing Unit) inference engine for near-instant responses.
* **Aiogram 3.x:** Fully asynchronous event handling.
* **Keep-Alive Server:** Integrated `aiohttp` web server to prevent sleep on cloud platforms (Render/Heroku).

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **LLM Engine:** Llama-3.1-8b-instant (via Groq Cloud)
* **Framework:** Aiogram (Telegram Bot API)
* **Orchestration:** LangChain (Core & Community)
* **Server:** Aiohttp (Async Web Server)

---

## ⚙️ Installation & Local Setup

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/your-username/itachi-ai-bot.git](https://github.com/your-username/itachi-ai-bot.git)
   cd itachi-ai-bot

   ```
2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   ``` 

3. **Install Dependencies**

```Bash

pip install -r requirements.txt
```

4. **Set Up Environment Variables Create a .env file in the root directory:**

```Bash

TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GROQ_API_KEY=your_groq_api_key_here
(Note: You must hardcode your ADMIN_ID in bot.py or add it to env for security)
```

5. **Run the Bot**

```Bash
python bot.py
```

6. ** Usage Commands **

```Bash
/start - Start the bot
/help - Get help
/founder - Get information about the founder
/sharingan - Activate Sharingan mode
/normal - Activate normal mode
/clear - Clear memory
/broadcast - Broadcast a message to all users
```

7. **Founder**
**Raghav Ramani**

**Role:** 4th-Year B.Tech CSE (AI & ML Specialization)

**Institution:** JECRC University

**Focus:** Generative AI, RAG Systems, MLOps.