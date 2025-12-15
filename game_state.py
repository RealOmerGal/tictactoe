# game_state.py
import random
from storage import StorageManager
import config



class GameState:

    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [""] * 9
        self.current_turn = "X"
        self.game_over = False
        self.winner = None
        self.p1_name = None
        self.p2_name = None
        self.mode = config.MODE_PVP  # Default

    def set_names(self, p1, p2):
        self.p1_name = p1 or "Player 1"
        self.p2_name = p2 or "Player 2"

    def make_move(self, index):
        """Attempts to make a move at index (0-8)"""
        if not self._is_valid(index):
            return False

        self.board[index] = self.current_turn

        # Check for Win/Draw immediately after human move
        if self.check_win():
            self._handle_end_game(winner_symbol=self.current_turn)
        elif "" not in self.board:
            self._handle_end_game(winner_symbol="Draw")
        else:
            self._switch_turn()

            # TRIGGER AI IF NEEDED
            # Only if game isn't over and it's now O's turn
            if not self.game_over and self.current_turn == "O":
                if self.mode == config.MODE_EASY:
                    self._ai_move_random()
                elif self.mode == config.MODE_HARD:
                    self._ai_move_minimax()

        return True

    # --- AI LOGIC ---

    def _ai_move_random(self):
        """Original 'Dumb' AI"""
        empty_indices = [i for i, x in enumerate(self.board) if x == ""]
        if empty_indices:
            choice = random.choice(empty_indices)
            self._finalize_ai_move(choice)

    def _ai_move_minimax(self):
        best_score = -float('inf')
        best_move = None

        # Loop through all available spots
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"  # Try move
                score = self._minimax(self.board, 0, False)  # Calc score
                self.board[i] = ""  # Undo move

                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self._finalize_ai_move(best_move)

    def _finalize_ai_move(self, index):
        """Apply the chosen AI move to the real board"""
        self.board[index] = "O"
        if self.check_win():
            self._handle_end_game(winner_symbol="O")
        elif "" not in self.board:
            self._handle_end_game(winner_symbol="Draw")
        else:
            self._switch_turn()

    def _minimax(self, board, depth, is_maximizing):
        """Recursive score calculation"""
        if self.check_win_simulation(board, "O"): return 10 - depth
        if self.check_win_simulation(board, "X"): return -10 + depth
        if "" not in board: return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "O"
                    score = self._minimax(board, depth + 1, False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "X"
                    score = self._minimax(board, depth + 1, True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    # --- HELPERS ---

    def _is_valid(self, index):
        if self.game_over or index is None:
            return False
        if 0 <= index < 9 and self.board[index] == "":
            return True
        return False

    def _switch_turn(self):
        self.current_turn = "O" if self.current_turn == "X" else "X"

    def _handle_end_game(self, winner_symbol):
        self.game_over = True

        if winner_symbol == "Draw":
            self.winner = "Draw"
            real_winner_name = "Draw"
        else:
            self.winner = winner_symbol
            real_winner_name = self.p1_name if winner_symbol == "X" else self.p2_name

        StorageManager.record_result(self.p1_name, self.p2_name, real_winner_name)

    def check_win(self):
            for a, b, c in config.WINS:
                if self.board[a] == self.board[b] == self.board[c] and self.board[a] != "":
                    return True
            return False

    def check_win_simulation(self, current_board, player_symbol):
        for a, b, c in config.WINS:
            if current_board[a] == current_board[b] == current_board[c] == player_symbol:
                return True
        return False

    # --- STORAGE ---

    def save_game(self):
        return StorageManager.save_game_state(self)

    def load_game(self):
        loaded_state = StorageManager.load_game_state()
        if loaded_state:
            self.__dict__.update(loaded_state.__dict__)
            return True
        return False

    def get_history_text(self):
        lines = StorageManager.get_history()
        return "".join(lines) if lines else "No games recorded."