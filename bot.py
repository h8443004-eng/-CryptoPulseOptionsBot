import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcoming message with interactive crypto options menu."""
    user = update.effective_user
    welcome_text = (
        "📈 Welcome to CryptoPulse Bot!\n\n"
        "Track live crypto prices, set instant price alerts, "
        "and view market trends directly inside this bot."
    )
    
    keyboard = [
        [
            InlineKeyboardButton("📈 Market Prices", callback_data="prices"),
            InlineKeyboardButton("⚡ Fast Swap", callback_data="swap"),
        ],
        [
            InlineKeyboardButton("📊 Top Gainers", callback_data="gainers"),
            InlineKeyboardButton("🔔 Price Alerts", callback_data="alerts"),
        ],
        [
            InlineKeyboardButton("🌐 Official Website", url="https://example.com"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard callbacks."""
    query = update.callback_query
    await query.answer()

    if query.data == "prices":
        text = "🔥 **Live Prices:**\n\n• BTC: $64,250 (+2.4%)\n• ETH: $3,480 (+1.8%)\n• TON: $6.80 (+5.1%)\n• SOL: $145 (+3.2%)"
    elif query.data == "swap":
        text = "⚡ **Crypto Swap Service**\n\nFast, non-custodial swaps with low fees. Select your pair to initiate swap."
    elif query.data == "gainers":
        text = "📊 **Top 24h Gainers:**\n\n1. $TON +12.4%\n2. $NOT +9.8%\n3. $PEPE +8.5%"
    elif query.data == "alerts":
        text = "🔔 **Price Alerts**\n\nSet custom price alerts for your favorite crypto tokens. (Feature Active)"
    else:
        text = "Action processed."

    back_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]])
    
    if query.data == "main_menu":
        await start(update, context)
    else:
        await query.edit_message_text(text=text, parse_mode="Markdown", reply_markup=back_keyboard)

def main():
    if not TOKEN:
        raise ValueError("No TELEGRAM_BOT_TOKEN environment variable found!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Bot starting in polling mode...")
    app.run_polling()

if __name__ == "__main__":
    main()
