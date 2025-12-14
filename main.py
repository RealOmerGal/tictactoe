# main.py
from game_state import GameState
from renderer import Renderer
import config

game = GameState()
view = Renderer()

# Current App State
app_state = config.STATE_MENU


def check_button_click(x, y, btn_dict):
    """Generic button click checker"""
    for name, (bx, by, bw, bh) in btn_dict.items():
        if (bx - bw / 2 <= x <= bx + bw / 2) and (by - bh / 2 <= y <= by + bh / 2):
            return name
    return None


def get_grid_index(x, y):
    """Only relevant for Game View"""
    if -400 < x < -200:
        col = 0
    elif -200 < x < 0:
        col = 1
    elif 0 < x < 200:
        col = 2
    else:
        return None

    if 100 < y < 300:
        row = 0
    elif -100 < y < 100:
        row = 1
    elif -300 < y < -100:
        row = 2
    else:
        return None

    return row * 3 + col

def game_start():
    view.draw_menu(game)
    game.p1_name = view.ask_input("Name", "Enter Player 1 Name:")
    game.p2_name = view.ask_input("Name", "Enter Player 2 Name:")
    view.draw_menu(game)  # Refresh to show new name

def handle_click(x, y):
    global app_state

    # --- STATE: MENU ---
    if app_state == config.STATE_MENU:
        btn = check_button_click(x, y, config.MENU_BTNS)

        if btn == "p1_name":
            name = view.ask_input("Name", "Enter Player 1 Name:")
            if name:
                game.p1_name = name
                view.draw_menu(game)  # Refresh to show new name

        elif btn == "p2_name":
            name = view.ask_input("Name", "Enter Player 2 Name:")
            if name:
                game.p2_name = name
                view.draw_menu(game)

        elif btn == "pvp":
            game.reset()  # Reset board
            game.mode = config.MODE_PVP
            # Keep the names user entered
            app_state = config.STATE_GAME
            view.draw_game(game)

        elif btn == "easy":
            game.reset()
            game.mode = config.MODE_EASY
            game.p2_name = "Easy Bot"  # Force P2 name
            app_state = config.STATE_GAME
            view.draw_game(game)

        elif btn == "hard":
            game.reset()
            game.mode = config.MODE_HARD
            game.p2_name = "Hard Bot"  # Force P2 name
            app_state = config.STATE_GAME
            view.draw_game(game)

        elif btn == "history":
            hist = game.get_history_text()
            view.show_history_popup(hist)
            app_state = "HISTORY_VIEW"

    # --- STATE: HISTORY POPUP ---
    elif app_state == "HISTORY_VIEW":
        # Any click returns to menu
        app_state = config.STATE_MENU
        view.draw_menu(game)

    # --- STATE: GAME ---
    elif app_state == config.STATE_GAME:
        # 1. Check Side Buttons
        btn = check_button_click(x, y, config.GAME_BTNS)

        if btn == "save":
            if game.save_game(): view.show_message("Saved!")
            return
        elif btn == "load":
            if game.load_game(): view.draw_game(game)
            return
        elif btn == "menu":
            app_state = config.STATE_MENU
            view.draw_menu(game)
            return

        # 2. Check Grid Click
        if not game.game_over:
            index = get_grid_index(x, y)
            if index is not None:
                if game.make_move(index):
                    view.draw_game(game)
                    if game.game_over:
                        msg = "Tie!" if game.winner == "Draw" else f"{game.winner} Wins!"
                        view.show_message(msg)


if __name__ == "__main__":
    game_start()
    listen = view.get_click_listener()
    listen(handle_click)
    view.start_loop()