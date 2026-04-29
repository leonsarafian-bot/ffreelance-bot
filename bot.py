import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from groq import Groq

TELEGRAM_TOKEN = "8568073474:AAFt3H1_cAqy8xPODZ4j07a1IGOLzRItuc0"
CHAT_ID = "8289404218"
GROQ_KEY = "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"

groq_client = Groq(api_key=GROQ_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running! Use /job to test.")

async def job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sample = "Client needs a Telegram bot for restaurant in Dubai. Auto-reply in Arabic. Budget $100."
    keyboard = [[InlineKeyboardButton("YES", callback_data="yes"), InlineKeyboardButton("NO", callback_data="no")]]
    await update.message.reply_text(f"New Job:\n\n{sample}", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "yes":
        await query.edit_message_text("AI is working...")
        result = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Write a short Telegram bot plan for a Dubai restaurant with Arabic auto-reply."}]
        )
        await context.bot.send_message(chat_id=CHAT_ID, text=f"AI Result:\n\n{result.choices[0].message.content}")
    else:
        await query.edit_message_text("Job skipped.")

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("job", job))
app.add_handler(CallbackQueryHandler(button))
print("Bot started!")
app.run_polling()
