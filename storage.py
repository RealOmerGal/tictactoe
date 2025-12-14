# storage.py
import pickle
import os
import config

class StorageManager:
    @staticmethod
    def save_game_state(game_state_obj):
        """Saves the entire game object to a binary file."""
        try:
            with open(config.BINARY_SAVE_FILE, "wb") as f:
                pickle.dump(game_state_obj, f)
            print("Game saved successfully.")
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    @staticmethod
    def load_game_state():
        """Loads the game object from binary file."""
        if not os.path.exists(config.BINARY_SAVE_FILE):
            return None
        try:
            with open(config.BINARY_SAVE_FILE, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    @staticmethod
    def record_result(p1, p2, winner):
        """Appends the game result to a text file."""
        # Format: gamer1_name,gamer2_name,winner_name
        line = f"{p1},{p2},{winner}\n"
        with open(config.HISTORY_FILE, "a") as f:
            f.write(line)

    @staticmethod
    def get_history():
        """Reads the history text file."""
        if not os.path.exists(config.HISTORY_FILE):
            return []
        with open(config.HISTORY_FILE, "r") as f:
            return f.readlines()