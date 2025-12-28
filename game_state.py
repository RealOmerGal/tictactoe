import random
from storage import StorageManager
import config


class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        # 0-based 3x3 grid
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_turn = "X"
        self.game_over = False
        self.winner = None
        self.p1_name = None
        self.p2_name = None
        self.mode = config.MODE_PVP

    def set_names(self, p1, p2):
        self.p1_name = p1 or "Player 1"
        self.p2_name = p2 or "Player 2"

    def make_move(self, row, col):
        if not self._is_valid(row, col):
            return False

        self.board[row][col] = self.current_turn

        if self.check_win():
            self._handle_end_game(winner_symbol=self.current_turn)
        elif self._is_board_full():
            self._handle_end_game(winner_symbol="Draw")
        else:
            self._switch_turn()
            if not self.game_over and self.current_turn == "O":
                if self.mode == config.MODE_EASY:
                    self._ai_move_random()
                elif self.mode == config.MODE_HARD:
                    self._ai_move_minimax()
        return True

    def _is_valid(self, row, col):
        if self.game_over: return False
        # Validates 0-2
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == "":
            return True
        return False

    # --- AI & WIN LOGIC ---
    def _ai_move_random(self):
        empty = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ""]
        if empty:
            r, c = random.choice(empty)
            self._finalize_ai_move(r, c)

    def _ai_move_minimax(self):
        best_score = -float('inf')
        best_move = None
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    self.board[r][c] = "O"
                    score = self._minimax(self.board, 0, False)
                    self.board[r][c] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        if best_move:
            self._finalize_ai_move(*best_move)

    def _finalize_ai_move(self, r, c):
        self.board[r][c] = "O"
        if self.check_win():
            self._handle_end_game("O")
        elif self._is_board_full():
            self._handle_end_game("Draw")
        else:
            self._switch_turn()

    def _minimax(self, board, depth, is_max):
        if self.check_win_sim(board, "O"): return 10 - depth
        if self.check_win_sim(board, "X"): return -10 + depth
        if self._is_full_sim(board): return 0

        best = -float('inf') if is_max else float('inf')
        func = max if is_max else min
        p = "O" if is_max else "X"

        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = p
                    score = self._minimax(board, depth + 1, not is_max)
                    board[r][c] = ""
                    best = func(score, best)
        return best

    def _switch_turn(self):
        self.current_turn = "O" if self.current_turn == "X" else "X"

    def _handle_end_game(self, winner_symbol):
        self.game_over = True
        self.winner = winner_symbol
        name = "Draw" if winner_symbol == "Draw" else (self.p1_name if winner_symbol == "X" else self.p2_name)
        StorageManager.record_result(self.p1_name, self.p2_name, name)

    def check_win(self):
        return self.check_win_sim(self.board, self.current_turn)

    def check_win_sim(self, b, p):
        # Rows & Cols
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] == p: return True
            if b[0][i] == b[1][i] == b[2][i] == p: return True
        # Diagonals
        if b[0][0] == b[1][1] == b[2][2] == p: return True
        if b[0][2] == b[1][1] == b[2][0] == p: return True
        return False

    def _is_board_full(self):
        return self._is_full_sim(self.board)

    def _is_full_sim(self, b):
        return all(c != "" for r in b for c in r)

    def save_game(self):
        return StorageManager.save_game_state(self)

    def load_game(self):
        s = StorageManager.load_game_state()
        if s: self.__dict__.update(s.__dict__); return True
        return False

    @staticmethod
    def get_history_text():
        lines = StorageManager.get_history()
        return "".join(lines) if lines else "No games recorded."