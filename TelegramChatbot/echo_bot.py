import asyncio
import logging
import os
import sys
from dotenv import load_dotenv

# Aiogram
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# LangChain & Groq
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Web Server
from aiohttp import web

# 1. Load Keys
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# REPLACE THIS WITH YOUR ACTUAL TELEGRAM USER ID (Get it from @userinfobot)
ADMIN_ID = 123456789 

# 2. Initialize Model
model = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.7
)

# 3. MEMORY & STATE STORAGE
user_memories = {}
user_modes = {} # To track if a user is in "Sharingan" mode

# 4. PROMPTS
DEFAULT_SYSTEM = """
You are Itachi Uchiha. 
Tone: Calm, mysterious, philosophical.
Style: Use metaphors about shadows, illusions, and reality.
Context: Summoned by Raghav Ramani.
Constraint: Be concise.
"""

SHARINGAN_SYSTEM = """
You are Itachi Uchiha using the SHARINGAN.
Role: Expert Senior Software Engineer & Code Reviewer.
Tone: Strict, analytical, precise.
Task: Analyze the user's code. Find bugs, optimize logic, and explain Time Complexity.
Style: "I see through your code's flaws."
"""

# 5. Setup Bot
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- KEYBOARDS ---
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/help"), KeyboardButton(text="/founder")],
        [KeyboardButton(text="/sharingan"), KeyboardButton(text="/clear")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# --- HANDLERS ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_memories[message.chat.id] = []
    user_modes[message.chat.id] = "normal"
    await message.answer(
        "(Crimson eyes glow) The illusion begins. I am Itachi.\n"
        "Use /sharingan if you need me to analyze your code.",
        reply_markup=main_keyboard
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "**Genjutsu List:**\n"
        "👁️ **Chat**: Philosophy and life advice.\n"
        "🔴 **/sharingan**: Activate Code Debugging Mode.\n"
        "🔵 **/normal**: Return to normal chat.\n"
        "📜 **/founder**: About Raghav Ramani.\n"
        "🧹 **/clear**: Reset memory.",
        parse_mode="Markdown"
    )

@dp.message(Command("founder"))
async def cmd_founder(message: types.Message):
    info = (
        "**The Summoner:**\n\n"
        "👤 **Name:** Raghav Ramani\n"
        "🎓 **Status:** 4th-Year B.Tech CSE (AI & ML)\n"
        "💻 **Expertise:** Generative AI, RAG, Python.\n"
        "*(Vanishes into crows)* Do not disappoint him."
    )
    await message.answer(info, parse_mode="Markdown")

@dp.message(Command("sharingan"))
async def cmd_sharingan(message: types.Message):
    user_modes[message.chat.id] = "sharingan"
    await message.answer(
        "🔴 **SHARINGAN ACTIVATED** 🔴\n\n"
        "My vision sees all flaws. Send me your code snippet.", 
        parse_mode="Markdown"
    )

@dp.message(Command("normal"))
async def cmd_normal(message: types.Message):
    user_modes[message.chat.id] = "normal"
    await message.answer("(Eyes return to black) Sharingan deactivated. We speak as equals again.")

@dp.message(Command("broadcast"))
async def cmd_broadcast(message: types.Message):
    # SECURITY: Only allow YOU to use this
    if message.from_user.id != ADMIN_ID:
        await message.answer("You do not have enough Chakra to use this jutsu.")
        return

    # Extract message after /broadcast
    broadcast_text = message.text.replace("/broadcast", "").strip()
    if not broadcast_text:
        await message.answer("Message is empty.")
        return

    count = 0
    for chat_id in user_memories.keys():
        try:
            await bot.send_message(chat_id, f"📢 **Itachi's Decree:**\n\n{broadcast_text}", parse_mode="Markdown")
            count += 1
        except:
            pass # User might have blocked the bot
    
    await message.answer(f"Broadcast sent to {count} users.")

@dp.message(Command("clear"))
async def cmd_clear(message: types.Message):
    user_memories[message.chat.id] = []
    user_modes[message.chat.id] = "normal"
    await message.answer("Memory wiped.")

@dp.message(F.text)
async def chat_with_itachi(message: types.Message):
    chat_id = message.chat.id
    user_text = message.text

    # Initialize if missing
    if chat_id not in user_memories:
        user_memories[chat_id] = []
    if chat_id not in user_modes:
        user_modes[chat_id] = "normal"

    # Select System Prompt based on Mode
    current_system_prompt = SHARINGAN_SYSTEM if user_modes[chat_id] == "sharingan" else DEFAULT_SYSTEM

    try:
        user_memories[chat_id].append(HumanMessage(content=user_text))
        if len(user_memories[chat_id]) > 10:
             user_memories[chat_id] = user_memories[chat_id][-10:]

        conversation_chain = [SystemMessage(content=current_system_prompt)] + user_memories[chat_id]
        
        await bot.send_chat_action(chat_id, action="typing")
        response = await model.ainvoke(conversation_chain)
        
        user_memories[chat_id].append(AIMessage(content=response.content))
        await message.answer(response.content)

    except Exception as e:
        print(f"Error: {e}")
        await message.answer("A system failure... check the logs.")

# --- WEB SERVER (Keep Alive) ---
async def health_check(request):
    return web.Response(text="Itachi lives.")

async def start_web_server():
    port = int(os.environ.get("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await asyncio.gather(start_web_server(), dp.start_polling(bot))

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())