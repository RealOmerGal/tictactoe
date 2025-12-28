import turtle
import config

class Renderer:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title(config.TITLE)
        self.screen.setup(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        self.screen.tracer(0)

        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.width(3)

    def clear_screen(self):
        self.pen.clear()
        self.screen.bgcolor(config.COLOR_BG)

    def draw_menu(self, game_state):
        self.clear_screen()

        # Title
        self.pen.penup()
        self.pen.goto(0, 200)
        self.pen.color("black")
        self.pen.write(config.TITLE, align="center", font=("Arial", 40, "bold"))
        self.pen.goto(0, 180)

        # Draw Mode Buttons
        self._draw_btn_rect(*config.MENU_BTNS['pvp'], "Play PvP")
        self._draw_btn_rect(*config.MENU_BTNS['easy'], "Easy AI")
        self._draw_btn_rect(*config.MENU_BTNS['hard'], "Hard AI")

        # Draw History
        self._draw_btn_rect(*config.MENU_BTNS['history'], "View History")
        self._draw_btn_rect(*config.MENU_BTNS['load'], "Load Game")

        self.screen.update()

    # --- GAME VIEW ---
    def draw_game(self, game_state):
        self.clear_screen()
        self._draw_grid()

        # Draw Side Buttons
        for key, val in config.GAME_BTNS.items():
            self._draw_btn_rect(*val, key.capitalize())

        # Draw Board State (Iterate 2D array)
        for r in range(3):
            for c in range(3):
                symbol = game_state.board[r][c]
                if symbol != "":
                    self.draw_marker(r, c, symbol, update=False)

        # Status Text
        self.pen.penup()
        self.pen.goto(-100, 320)
        self.pen.color("black")
        self.pen.write(f"{game_state.p1_name} vs {game_state.p2_name}", align="center", font=("Arial", 16, "bold"))

        self.screen.update()

    def _draw_btn_rect(self, x, y, w, h, text):
        self.pen.color("black")
        self.pen.fillcolor(config.COLOR_BTN)
        self.pen.penup()
        self.pen.goto(x - w / 2, y - h / 2)
        self.pen.pendown()
        self.pen.begin_fill()
        for _ in range(2):
            self.pen.forward(w)
            self.pen.left(90)
            self.pen.forward(h)
            self.pen.left(90)
        self.pen.end_fill()

        self.pen.penup()
        self.pen.goto(x, y - 10)
        self.pen.color(config.COLOR_TEXT)
        self.pen.write(text, align="center", font=("Arial", 12, "bold"))

    def _draw_grid(self):
        self.pen.color(config.COLOR_LINE)
        # Offset matches the coordinate logic in draw_marker
        offset_x = -100
        # Vertical lines
        self._line(offset_x - 100, 300, offset_x - 100, -300)
        self._line(offset_x + 100, 300, offset_x + 100, -300)
        # Horizontal lines
        self._line(offset_x - 300, 100, offset_x + 300, 100)
        self._line(offset_x - 300, -100, offset_x + 300, -100)

    def draw_marker(self, row, col, player, update=True):
        # Calculate visual coordinates based on row/col
        # Cols: 0=-300, 1=-100, 2=100
        x = -300 + (col * 200)
        # Rows: 0=200, 1=0, 2=-200
        y = 200 - (row * 200)

        if player == "X":
            self.pen.color("blue")
            self._line(x - 60, y + 60, x + 60, y - 60)
            self._line(x - 60, y - 60, x + 60, y + 60)
        else:
            self.pen.color("red")
            self.pen.penup()
            self.pen.goto(x, y - 60)
            self.pen.pendown()
            self.pen.circle(60)

        if update: self.screen.update()

    def show_message(self, text):
        # Could swap into UI message
        print(text)

    def ask_input(self, title, prompt):
        res = self.screen.textinput(title, prompt)
        if res:
            return res.strip()

    def show_history_popup(self, text):
        self.pen.clear()
        self.pen.penup()

        self.pen.goto(0, 260)
        self.pen.write(
            "Match History (Click to return)",
            align="center",
            font=("Arial", 16, "bold")
        )

        y = 220
        line_height = 18
        lines = text.splitlines() if isinstance(text, str) else text

        for line in lines:
            self.pen.goto(0, y)
            self.pen.write(
                line,
                align="center",
                font=("Courier", 10, "normal")
            )
            y -= line_height

        self.screen.update()

    def _line(self, x1, y1, x2, y2):
        self.pen.penup()
        self.pen.goto(x1, y1)
        self.pen.pendown()
        self.pen.goto(x2, y2)

    def get_click_listener(self):
        return self.screen.onclick

    def start_loop(self):
        self.screen.mainloop()