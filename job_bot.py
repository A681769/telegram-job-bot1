import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Hello! I am your Job Bot. Use /jobs to see the latest jobs.")

async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching latest jobs...")
    jobs = [
        "🖥️ Software Engineer - Google",
        "📱 Mobile Developer - Apple",
        "☁️ Cloud Engineer - AWS",
        "🤖 AI Engineer - OpenAI",
        "💻 Backend Developer - Microsoft"
    ]
    await update.message.reply_text("\n".join(jobs))

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jobs", jobs))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
