from typing import List, Optional, Set, Tuple
from app.solvers.base import BaseSolver
from app.graph.structures import SudokuGraph
import copy


class SudokuSolver(BaseSolver):
    def __init__(self):
        super().__init__()
        self.graph = SudokuGraph()
        self.algorithm_used = "backtracking_with_constraint_propagation"

    def solve(self, input_data: dict, options: dict) -> Optional[List[List[int]]]:
        self.start_timer()
        grid = input_data['grid']

        if not self.validate_input(input_data):
            return None

        board = [row[:] for row in grid]

        if options.get('algorithm') == 'constraint_propagation':
            self.algorithm_used = "constraint_propagation"
            board = self._constraint_propagation(board)
            if board and self._is_complete(board):
                return board

        solution = self._backtrack(board, options.get('return_steps', True))
        return solution

    def validate_input(self, input_data: dict) -> bool:
        grid = input_data.get('grid', [])

        if len(grid) != 9:
            return False

        for row in grid:
            if len(row) != 9:
                return False
            for val in row:
                if not isinstance(val, int) or val < 0 or val > 9:
                    return False

        for i in range(9):
            for j in range(9):
                if grid[i][j] != 0:
                    temp = grid[i][j]
                    grid[i][j] = 0
                    if not self._is_valid(grid, i, j, temp):
                        grid[i][j] = temp
                        return False
                    grid[i][j] = temp

        return True

    def _find_empty_cell_mrv(self, board: List[List[int]]) -> Optional[Tuple[int, int]]:
        min_values = 10
        best_cell = None

        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    possible_values = self._get_possible_values(board, i, j)
                    if len(possible_values) < min_values:
                        min_values = len(possible_values)
                        best_cell = (i, j)
                        if min_values == 0:
                            return best_cell

        return best_cell

    def _get_possible_values(self, board: List[List[int]], row: int, col: int) -> Set[int]:
        if board[row][col] != 0:
            return set()

        used = set()

        for j in range(9):
            if board[row][j] != 0:
                used.add(board[row][j])

        for i in range(9):
            if board[i][col] != 0:
                used.add(board[i][col])

        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] != 0:
                    used.add(board[i][j])

        return set(range(1, 10)) - used

    def _is_valid(self, board: List[List[int]], row: int, col: int, num: int) -> bool:
        for j in range(9):
            if j != col and board[row][j] == num:
                return False

        for i in range(9):
            if i != row and board[i][col] == num:
                return False

        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i != row or j != col) and board[i][j] == num:
                    return False

        return True

    def _backtrack(self, board: List[List[int]], track_steps: bool = True) -> Optional[List[List[int]]]:
        self.nodes_explored += 1

        cell = self._find_empty_cell_mrv(board)
        if not cell:
            return board

        row, col = cell
        possible_values = self._get_possible_values(board, row, col)

        if not possible_values:
            self.backtrack_count += 1
            if track_steps:
                self.add_step("backtrack", (row, col), None,
                              f"No valid values for cell ({row}, {col})")
            return None

        for num in possible_values:
            if track_steps:
                self.add_step("place", (row, col), num,
                              f"Trying {num} at cell ({row}, {col})")

            board[row][col] = num

            result = self._backtrack(board, track_steps)
            if result:
                return result

            board[row][col] = 0
            if track_steps:
                self.add_step("remove", (row, col), num,
                              f"Removing {num} from cell ({row}, {col})")

        self.backtrack_count += 1
        return None

    def _is_complete(self, board: List[List[int]]) -> bool:
        for row in board:
            if 0 in row:
                return False
        return True

    def _constraint_propagation(self, board: List[List[int]]) -> Optional[List[List[int]]]:
        changed = True
        while changed:
            changed = False
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        possible = self._get_possible_values(board, i, j)
                        if len(possible) == 0:
                            return None
                        elif len(possible) == 1:
                            board[i][j] = possible.pop()
                            changed = True
                            self.add_step("propagate", (i, j), board[i][j],
                                          f"Only one possible value for ({i}, {j})")
        return board