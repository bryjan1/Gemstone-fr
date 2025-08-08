
import pandas as pd
import random
import os

DATA_FILE = "history.csv"

def load_history():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["user_id", "board", "result"])

def save_game(user_id, board, result):
    df = load_history()
    df.loc[len(df)] = [user_id, board, result]
    df.to_csv(DATA_FILE, index=False)

def predict_safe_tiles(board_size=5, bombs=3):
    tiles = list(range(1, board_size * board_size + 1))
    safe_tiles = random.sample(tiles, board_size * board_size - bombs)
    return sorted(safe_tiles)

def get_user_history(user_id):
    df = load_history()
    user_df = df[df["user_id"] == user_id]
    if user_df.empty:
        return "No history found."
    history_lines = user_df.tail(5).apply(lambda row: f"{row['board']} - {row['result']}", axis=1)
    return "\n".join(history_lines)
