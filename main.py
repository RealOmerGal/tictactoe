from game_state import GameState
from renderer import Renderer
import config

game = GameState()
view = Renderer()
app_state = config.STATE_MENU


def check_button_click(x, y, btn_dict):
    for name, (bx, by, bw, bh) in btn_dict.items():
        if (bx - bw / 2 <= x <= bx + bw / 2) and (by - bh / 2 <= y <= by + bh / 2):
            return name
    return None


def get_grid_coords(x, y):
    """Maps mouse click pixels to 0-2 Index directly"""
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

    return row, col


def game_start():
    view.draw_menu(game)


def handle_click(x, y):
    global app_state

    # --- MENU STATE ---
    if app_state == config.STATE_MENU:
        btn = check_button_click(x, y, config.MENU_BTNS)
        if btn == "p1_name":
            name = view.ask_input("Name", "Enter Player 1 Name:")
            if name: game.p1_name = name; view.draw_menu(game)
        elif btn == "p2_name":
            name = view.ask_input("Name", "Enter Player 2 Name:")
            if name: game.p2_name = name; view.draw_menu(game)
        elif btn == "pvp":
            game.reset()
            game.mode = config.MODE_PVP
            game.set_names(view.ask_input("Name", "Player 1:"), view.ask_input("Name", "Player 2:"))
            app_state = config.STATE_GAME
            view.draw_game(game)
        elif btn == "easy":
            game.reset()
            game.mode = config.MODE_EASY
            game.set_names(view.ask_input("Name", "Player 1:"), "Easy Bot")
            app_state = config.STATE_GAME
            view.draw_game(game)
        elif btn == "hard":
            game.reset()
            game.mode = config.MODE_HARD
            game.set_names(view.ask_input("Name", "Player 1:"), "Hard Bot")
            app_state = config.STATE_GAME
            view.draw_game(game)
        elif btn == "history":
            view.show_history_popup(game.get_history_text())
            app_state = "HISTORY_VIEW"
        elif btn == "load":
            if game.load_game():
                app_state = config.STATE_GAME
                view.draw_game(game)

    elif app_state == "HISTORY_VIEW":
        app_state = config.STATE_MENU
        view.draw_menu(game)

    # --- GAME STATE ---
    elif app_state == config.STATE_GAME:
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

        elif btn == "manual":
            if not game.game_over:
                # Ask for ROW (1-3)
                r_in = view.ask_input("Move", "Enter Row (1-3):")
                # Ask for COL (1-3)
                c_in = view.ask_input("Move", "Enter Column (1-3):")

                # Validation & Conversion
                if r_in and c_in and r_in.isdigit() and c_in.isdigit():
                    r_val = int(r_in)
                    c_val = int(c_in)

                    if 1 <= r_val <= 3 and 1 <= c_val <= 3:
                        # Convert to 0-based index board
                        final_r = r_val - 1
                        final_c = c_val - 1

                        if game.make_move(final_r, final_c):
                            view.draw_game(game)
                            if game.game_over:
                                msg = "Tie!" if game.winner == "Draw" else f"{game.winner} Wins!"
                                view.show_message(msg)
                        else:
                            view.show_message("Invalid Move! Cell occupied or out  bounds.")
                    else:
                        view.show_message("Invalid Input! Use 1-3")
            return

        if not game.game_over:
            coords = get_grid_coords(x, y)
            if coords:
                if game.make_move(*coords):
                    view.draw_game(game)
                    if game.game_over:
                        msg = "Tie!" if game.winner == "Draw" else f"{game.winner} Wins!"
                        view.show_message(msg)


if __name__ == "__main__":
    game_start()
    listen = view.get_click_listener()
    listen(handle_click)
    view.start_loop()