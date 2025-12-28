# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Tic Tac Toe"

# Colors
COLOR_BG = "white"
COLOR_LINE = "black"
COLOR_BTN = "lightgray"
COLOR_TEXT = "black"

# Files
BINARY_SAVE_FILE = "game_save.bin"
HISTORY_FILE = "game_history.txt"

# Modes
MODE_PVP = "PvP"
MODE_EASY = "Easy AI"
MODE_HARD = "Hard AI"
STATE_MENU = "menu"
STATE_GAME = "game"

# --- MENU LAYOUT ---
MENU_BTNS = {
    "pvp": (0, 100, 140, 60),
    "easy": (0, 30, 140, 60),
    "hard": (0, -40, 140, 60),
    "history": (-125, -120, 200, 50),
    "load": (125, -120, 200, 50)
}

# --- GAME LAYOUT ---
GAME_BTNS = {
    "save": (300, 200, 80, 40),
    "load": (300, 150, 80, 40),
    "manual": (300, 50, 80, 40),
    "menu": (300, -250, 80, 40)
}