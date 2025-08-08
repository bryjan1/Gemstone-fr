
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from predictor import predict_safe_tiles, save_game, get_user_history

TOKEN = os.getenv("TOKEN") or "YOUR_TELEGRAM_BOT_TOKEN"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to Stake Mine Predictor Bot!\nUse /predict or /help for commands.")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Available commands:\n"
        "/predict <board_size> <bombs> – Predict safe tiles (default 5x5, 3 bombs)\n"
        "/history – Show your last 5 games\n"
        "/help – Show this help message"
    )

def predict(update: Update, context: CallbackContext):
    try:
        board_size = int(context.args[0]) if len(context.args) >= 1 else 5
        bombs = int(context.args[1]) if len(context.args) >= 2 else 3

        if board_size <= 0 or bombs < 0 or bombs >= board_size ** 2:
            raise ValueError

        safe_tiles = predict_safe_tiles(board_size, bombs)
        board_str = f"{board_size}x{board_size} with {bombs} bombs"
        result = f"Predicted safe tiles: {safe_tiles}"

        user_id = update.effective_user.id
        save_game(user_id, board_str, result)

        update.message.reply_text(f"{result}")
    except (ValueError, IndexError):
        update.message.reply_text("Invalid input. Usage: /predict <board_size> <bombs>")

def history(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    history = get_user_history(user_id)
    update.message.reply_text(f"Your Game History:\n{history}")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("predict", predict))
    dp.add_handler(CommandHandler("history", history))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
