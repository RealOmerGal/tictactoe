# config.py

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Tic Tac Toe: Ultimate"

# Colors
COLOR_BG = "white"
COLOR_LINE = "black"
COLOR_BTN = "lightgray"
COLOR_BTN_HOVER = "gray"
COLOR_TEXT = "black"

# Files
BINARY_SAVE_FILE = "game_save.bin"
HISTORY_FILE = "game_history.txt"

# Game Modes
MODE_PVP = "PvP"
MODE_EASY = "Easy AI"
MODE_HARD = "Hard AI"

# App States
STATE_MENU = "menu"
STATE_GAME = "game"

# --- MENU LAYOUT ---
# (x, y, w, h)
MENU_BTNS = {
    "p1_name": (0, 100, 300, 50),   # Click to edit name
    "p2_name": (0, 30, 300, 50),    # Click to edit name
    "pvp": (-150, -100, 140, 60),
    "easy": (0, -100, 140, 60),
    "hard": (150, -100, 140, 60),
    "history": (0, -200, 200, 50)
}

# --- GAME LAYOUT ---
GAME_BTNS = {
    "save": (300, 200, 80, 40),
    "load": (300, 150, 80, 40),
    "menu": (300, -250, 80, 40) # Back to menu
}