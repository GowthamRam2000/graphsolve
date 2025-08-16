from typing import List, Optional, Set, Tuple
from app.solvers.base import BaseSolver


class NQueensSolver(BaseSolver):
    def __init__(self):
        super().__init__()
        self.algorithm_used = "backtracking_with_pruning"
        self.all_solutions = []

    def solve(self, input_data: dict, options: dict) -> Optional[List[Tuple[int, int]]]:
        self.start_timer()

        if not self.validate_input(input_data):
            return None

        n = input_data['n']
        preset_queens = input_data.get('preset_queens', [])
        max_solutions = options.get('max_solutions', 1)

        board = [[0] * n for _ in range(n)]
        for row, col in preset_queens:
            board[row][col] = 1

        self.all_solutions = []
        self._solve_nqueens(board, 0, n, preset_queens, max_solutions,
                            options.get('return_steps', True))

        if self.all_solutions:
            return self.all_solutions[0] if max_solutions == 1 else self.all_solutions
        return None

    def validate_input(self, input_data: dict) -> bool:
        n = input_data.get('n', 0)
        if n < 4 or n > 12:
            return False

        preset_queens = input_data.get('preset_queens', [])
        for row, col in preset_queens:
            if row < 0 or row >= n or col < 0 or col >= n:
                return False

            for other_row, other_col in preset_queens:
                if (row, col) != (other_row, other_col):
                    if self._conflicts(row, col, other_row, other_col):
                        return False

        return True

    def _conflicts(self, r1: int, c1: int, r2: int, c2: int) -> bool:
        return (r1 == r2 or c1 == c2 or
                abs(r1 - r2) == abs(c1 - c2))

    def _is_safe(self, board: List[List[int]], row: int, col: int, n: int) -> bool:
        for j in range(n):
            if board[row][j] == 1:
                return False

        for i in range(n):
            if board[i][col] == 1:
                return False

        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if board[i][j] == 1:
                return False
            i -= 1
            j -= 1

        i, j = row - 1, col + 1
        while i >= 0 and j < n:
            if board[i][j] == 1:
                return False
            i -= 1
            j += 1

        i, j = row + 1, col - 1
        while i < n and j >= 0:
            if board[i][j] == 1:
                return False
            i += 1
            j -= 1

        i, j = row + 1, col + 1
        while i < n and j < n:
            if board[i][j] == 1:
                return False
            i += 1
            j += 1

        return True

    def _solve_nqueens(self, board: List[List[int]], row: int, n: int,
                       preset_queens: List[Tuple[int, int]], max_solutions: int,
                       track_steps: bool) -> bool:
        self.nodes_explored += 1

        if len(self.all_solutions) >= max_solutions:
            return True

        if row >= n:
            solution = [(i, j) for i in range(n) for j in range(n) if board[i][j] == 1]
            if len(solution) == n:
                self.all_solutions.append(solution)
                if track_steps:
                    self.add_step("solution", None, solution,
                                  f"Found solution #{len(self.all_solutions)}")
                return len(self.all_solutions) >= max_solutions
            return False

        if any(r == row for r, c in preset_queens):
            return self._solve_nqueens(board, row + 1, n, preset_queens,
                                       max_solutions, track_steps)

        for col in range(n):
            if self._is_safe(board, row, col, n):
                if track_steps:
                    self.add_step("place", (row, col), "Q",
                                  f"Placing queen at ({row}, {col})")

                board[row][col] = 1

                if self._solve_nqueens(board, row + 1, n, preset_queens,
                                       max_solutions, track_steps):
                    if len(self.all_solutions) >= max_solutions:
                        return True

                board[row][col] = 0
                self.backtrack_count += 1

                if track_steps:
                    self.add_step("remove", (row, col), None,
                                  f"Removing queen from ({row}, {col})")

        return False

    def _get_all_solutions(self, n: int) -> List[List[Tuple[int, int]]]:
        self.all_solutions = []
        board = [[0] * n for _ in range(n)]
        self._solve_nqueens(board, 0, n, [], float('inf'), False)
        return self.all_solutions