import logging
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes
import openai
from config import Config
from utils import split_long_message, extract_code_from_markdown

logger = logging.getLogger(__name__)

# Initialize OpenAI client for DeepSeek
if Config.DEEPSEEK_API_KEY:
    openai.api_key = Config.DEEPSEEK_API_KEY
    openai.api_base = "https://api.deepseek.com/v1"
    logger.info("DeepSeek AI initialized")
else:
    logger.warning("DEEPSEEK_API_KEY not set")

start_time = datetime.now()

def get_main_keyboard():
    """Return a ReplyKeyboardMarkup with main commands."""
    keyboard = [
        [KeyboardButton("/ask"), KeyboardButton("/code")],
        [KeyboardButton("/status"), KeyboardButton("/help")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message with the keyboard."""
    if update.effective_user.id != Config.ADMIN_ID:
        await update.message.reply_text("⛔ Access denied")
        return
    await update.message.reply_text(
        "🤖 **AI Telegram Bot**\n\nChoose a command:",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ask command – send a question to DeepSeek."""
    if update.effective_user.id != Config.ADMIN_ID:
        return

    question = ' '.join(context.args)
    if not question:
        await update.message.reply_text("❓ Usage: /ask <your question>")
        return

    if not Config.DEEPSEEK_API_KEY:
        await update.message.reply_text("⚠️ AI API key not configured")
        return

    await update.message.chat.send_action(action="typing")

    try:
        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Answer concisely."},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        answer = response.choices[0].message.content
        await update.message.reply_text(f"🧠 **Answer:**\n{answer}", parse_mode="Markdown", reply_markup=get_main_keyboard())
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)[:200]}")

async def code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /code command – generate Python code."""
    if update.effective_user.id != Config.ADMIN_ID:
        return

    task = ' '.join(context.args)
    if not task:
        await update.message.reply_text("💻 Usage: /code <task description>")
        return

    if not Config.DEEPSEEK_API_KEY:
        await update.message.reply_text("⚠️ AI API key not configured")
        return

    await update.message.reply_text(f"⏳ Generating code for: {task}...")
    await update.message.chat.send_action(action="typing")

    try:
        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are an expert Python programmer. Write clean, runnable code without explanations."},
                {"role": "user", "content": f"Write Python code for: {task}"}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        code_text = response.choices[0].message.content
        code_text = extract_code_from_markdown(code_text)

        if len(code_text) > 4000:
            parts = split_long_message(code_text)
            await update.message.reply_text(f"📦 Code is long, sending in {len(parts)} parts:")
            for i, part in enumerate(parts, 1):
                await update.message.reply_text(
                    f"**Part {i}/{len(parts)}:**\n\n```python\n{part}\n```",
                    parse_mode="Markdown",
                    reply_markup=get_main_keyboard()
                )
        else:
            await update.message.reply_text(
                f"💻 **Generated Code:**\n\n```python\n{code_text}\n```",
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)[:200]}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot uptime and status."""
    if update.effective_user.id != Config.ADMIN_ID:
        return
    delta = datetime.now() - start_time
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    await update.message.reply_text(
        f"📊 **Bot Status**\n\nUptime: {hours}h {minutes}m\nAI: {'✅' if Config.DEEPSEEK_API_KEY else '❌'}",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message."""
    await update.message.reply_text(
        "📚 **Commands**\n"
        "/ask <question> – ask AI\n"
        "/code <task> – generate Python code\n"
        "/status – bot status\n"
        "/start – restart bot",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )
