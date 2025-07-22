import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("7788657031:AAEzUpF_PFn6cu2UjhUuhVpqCRm4Qht0u4M")
RAPID_API_KEY = os.environ.get("8fd72b41camshb6c4219391fa1d3p13aa0ejsn56721517a303")


# ✅ Fetch live jobs from JSearch API
def get_jobs():
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {
        "query": "python developer remote",
        "page": "1",
        "num_pages": "1"
    }

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        print("API raw response:", response.text)  # ✅ Debug output
        data = response.json()

        jobs = []
        for job in data.get("data", [])[:5]:  # Get only top 5
            title = job.get("job_title", "No title")
            company = job.get("employer_name", "Unknown")
            link = job.get("job_apply_link", "#")
            jobs.append({"title": title, "company": company, "link": link})

        return jobs
    except Exception as e:
        print("API error:", e)
        return []

# ✅ /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I’m your Job Alert Bot.\n\n"
        "Type /jobs to see the latest *Python Remote Jobs*.\n"
        "Or test with /ping."
    )

# ✅ /ping command
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong!")

# ✅ /jobs command (uses RapidAPI JSearch)
async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Fetching live job openings...")

    job_list = get_jobs()

    if not job_list:
        await update.message.reply_text("❌ No jobs found or API failed. Try again later.")
        return

    message = "🔥 *Latest Python Remote Jobs:*\n\n"
    for job in job_list:
        message += f"✅ *{job['title']}* at _{job['company']}_\n👉 [Apply here]({job['link']})\n\n"

    await update.message.reply_text(message, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("jobs", jobs))

    print("✅ Bot is running... Press CTRL+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
