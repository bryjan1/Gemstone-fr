import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging

# --- Telegram Bot Logic ---
TOKEN = os.getenv("TOKEN")

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to Stake Mine Predictor Bot! Use /predict or /help.")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("/predict <number_of_tiles> <bombs>\n/history\n/help")

def predict(update: Update, context: CallbackContext):
    try:
        board_size = int(context.args[0]) if len(context.args) > 0 else 5
        bombs = int(context.args[1]) if len(context.args) > 1 else 3
        tiles = list(range(1, board_size * board_size + 1))
        safe_tiles = sorted(tiles[:(board_size * board_size - bombs)])
        update.message.reply_text(f"Predicted safe tiles: {safe_tiles}")
    except:
        update.message.reply_text("Usage: /predict <tiles> <bombs>")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("predict", predict))

# --- Flask Keepalive ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running."

def run():
    app.run(host="0.0.0.0", port=10000)

def start_bot():
    updater.start_polling()
    updater.idle()

# Start Flask + Bot in parallel
if __name__ == "__main__":
    Thread(target=run).start()
    Thread(target=start_bot).start()