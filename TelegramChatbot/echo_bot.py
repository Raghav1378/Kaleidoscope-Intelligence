import asyncio
import logging
import os
import sys
from dotenv import load_dotenv

# Aiogram
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# LangChain & Groq
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Web Server (To trick Render)
from aiohttp import web

# 1. Load Keys
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 2. Initialize Model
model = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.7,
    max_tokens=300
)

# 3. MEMORY STORAGE
user_memories = {}

# 4. Itachi's Personality
SYSTEM_PROMPT = """
You are Itachi Uchiha. 
Tone: Calm, mysterious, philosophical.
Style: Use metaphors about shadows, illusions, and reality.
Memory: You remember previous details.
Constraint: Be concise.
"""

# 5. Setup Bot
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- HANDLERS ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_memories[message.chat.id] = []
    await message.answer("(Crimson eyes glow) The illusion begins anew.")

@dp.message(F.text)
async def chat_with_itachi(message: types.Message):
    user_text = message.text
    chat_id = message.chat.id
    
    try:
        if chat_id not in user_memories:
            user_memories[chat_id] = []
        
        user_memories[chat_id].append(HumanMessage(content=user_text))
        
        if len(user_memories[chat_id]) > 10:
             user_memories[chat_id] = user_memories[chat_id][-10:]

        conversation_chain = [SystemMessage(content=SYSTEM_PROMPT)] + user_memories[chat_id]
        
        response = model.invoke(conversation_chain)
        bot_reply = response.content
        
        user_memories[chat_id].append(AIMessage(content=bot_reply))
        await message.answer(bot_reply)

    except Exception as e:
        print(f"❌ Error: {e}")
        await message.answer("(Coughs blood) My vision blurs... (Error)")

# --- DUMMY WEB SERVER (The Trick) ---
async def health_check(request):
    return web.Response(text="Itachi is alive in the shadows.")

async def start_web_server():
    # Render gives us a PORT env variable. We MUST listen on it.
    port = int(os.environ.get("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🕸️ Web server running on port {port}")

# --- MAIN ---
async def main():
    # Start the dummy web server AND the bot at the same time
    await asyncio.gather(
        start_web_server(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    # Fix for Windows loop policy if needed, otherwise standard run
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")