import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Replace with your actual Channel/Group URL or Website link
CHANNEL_URL = "https://t.me/your_channel_username" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command for any user."""
    user_first_name = update.effective_user.first_name

    welcome_text = (
        f"⚽ **Welcome {user_first_name}!**\n\n"
        "Welcome to **SBR24h_1bot**! Your round-the-clock booking assistant.\n\n"
        "**What I can do:**\n"
        "📅 **Check Availability:** Browse open date and time slots instantly.\n"
        "⚡ **Fast Booking:** Reserve appointments, venues, or equipment in seconds.\n"
        "🔔 **Instant Confirmation:** Get immediate booking details and reminder alerts.\n"
        "❌ **Easy Management:** View or cancel your upcoming reservations anytime.\n\n"
        "Tap /start to pick a time and confirm your booking!"
    )

    # Creating inline buttons (matching the format in your image)
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel Here", url=CHANNEL_URL)],
        [InlineKeyboardButton("✅ I Have Joined!", callback_data="check_joined")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles button clicks (like 'I Have Joined!')."""
    query = update.callback_query
    await query.answer()

    if query.data == "check_joined":
        await query.message.reply_text("Thank you for verifying! Use /start anytime to start booking.")

async def handle_questions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers general questions regarding what the bot does."""
    text = update.message.text.lower()
    
    if any(q in text for q in ["who are you", "what can you do", "help", "how to book", "service"]):
        response = (
            "I am **SBR24h_1bot**, an automated 24/7 booking assistant!\n\n"
            "I help you check available time slots, make fast reservations for venues or equipment, "
            "send instant confirmations, and manage or cancel existing bookings seamlessly."
        )
    else:
        response = (
            "I'm here to assist with your bookings! "
            "Please send /start to select an option or ask me how to book."
        )
        
    await update.message.reply_text(response, parse_mode="Markdown")

def main() -> None:
    """Starts the background worker bot."""
    # Retrieve Bot Token securely from Railway Environment Variables
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("No BOT_TOKEN found in environment variables!")

    app = Application.builder().token(token).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_questions))

    # Run polling mode (suited for Railway Background Worker)
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
