import logging
import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    ConversationHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.getenv("BOT_TOKEN")

SERVICE, DATE, TIME, NAME, CONTACT = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📅 Make a Booking", callback_data="booking")
        ],
        [
            InlineKeyboardButton("🔎 Check Availability", callback_data="availability")
        ],
        [
            InlineKeyboardButton("📋 My Booking", callback_data="my_booking")
        ],
        [
            InlineKeyboardButton("❌ Cancel Booking", callback_data="cancel")
        ],
        [
            InlineKeyboardButton("❓ FAQs", callback_data="faq")
        ],
        [
            InlineKeyboardButton("💬 Contact Support", callback_data="support")
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 *Welcome to our 24/7 Booking Assistant!*\n\n"
        "I can help you make reservations, check availability, "
        "manage bookings, and answer common questions.\n\n"
        "Please choose an option below:",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    if query.data == "booking":
        await query.message.reply_text(
            "📅 *Let's make your booking!*\n\n"
            "What service would you like to book?\n\n"
            "Example: Meeting room, equipment rental, appointment, etc.",
            parse_mode="Markdown",
        )
        return SERVICE

    elif query.data == "availability":
        await query.message.reply_text(
            "🔎 *Check Availability*\n\n"
            "Please tell me the service and date you want to check.\n\n"
            "Example:\n"
            "Meeting room - August 25",
            parse_mode="Markdown",
        )

    elif query.data == "my_booking":
        await query.message.reply_text(
            "📋 *My Booking*\n\n"
            "Please send your booking reference number.",
            parse_mode="Markdown",
        )

    elif query.data == "cancel":
        await query.message.reply_text(
            "❌ *Cancel Booking*\n\n"
            "Please send your booking reference number.",
            parse_mode="Markdown",
        )

    elif query.data == "faq":
        await query.message.reply_text(
            "❓ *Frequently Asked Questions*\n\n"
            "• How do I make a booking?\n"
            "Use the 📅 Make a Booking button.\n\n"
            "• Can I cancel my booking?\n"
            "Yes. Send your booking reference to request cancellation.\n\n"
            "• Is support available 24/7?\n"
            "Yes, this bot is available 24/7.",
            parse_mode="Markdown",
        )

    elif query.data == "support":
        await query.message.reply_text(
            "💬 *Contact Support*\n\n"
            "Please describe your question or problem, "
            "and our support team will assist you.",
            parse_mode="Markdown",
        )


async def service_received(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    context.user_data["service"] = update.message.text

    await update.message.reply_text(
        "📅 Great!\n\n"
        "What date would you like to book?\n\n"
        "Example: August 25, 2026"
    )

    return DATE


async def date_received(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    context.user_data["date"] = update.message.text

    await update.message.reply_text(
        "⏰ What time would you like?\n\n"
        "Example: 2:00 PM"
    )

    return TIME


async def time_received(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    context.user_data["time"] = update.message.text

    await update.message.reply_text(
        "👤 What is your full name?"
    )

    return NAME


async def name_received(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "📞 Please provide your phone number or email address."
    )

    return CONTACT


async def contact_received(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    context.user_data["contact"] = update.message.text

    service = context.user_data["service"]
    date = context.user_data["date"]
    time = context.user_data["time"]
    name = context.user_data["name"]
    contact = context.user_data["contact"]

    await update.message.reply_text(
        "✅ *Booking Request Received!*\n\n"
        f"📌 Service: {service}\n"
        f"📅 Date: {date}\n"
        f"⏰ Time: {time}\n"
        f"👤 Name: {name}\n"
        f"📞 Contact: {contact}\n\n"
        "Your booking request has been received successfully.\n"
        "Our system will process your reservation and "
        "provide confirmation.",
        parse_mode="Markdown",
    )

    context.user_data.clear()

    return ConversationHandler.END


async def cancel_booking(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "Booking cancelled."
    )

    return ConversationHandler.END


async def unknown_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🤖 I'm here to help with bookings and reservations.\n\n"
        "Please use /start to see the available options."
    )


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable is missing.")

    application = Application.builder().token(TOKEN).build()

    booking_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_handler, pattern="^booking$")
        ],
        states={
            SERVICE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    service_received
                )
            ],
            DATE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    date_received
                )
            ],
            TIME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    time_received
                )
            ],
            NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    name_received
                )
            ],
            CONTACT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    contact_received
                )
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_booking)
        ],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(booking_conversation)
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message)
    )

    print("Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
