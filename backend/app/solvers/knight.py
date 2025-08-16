from typing import List, Optional, Tuple
from app.solvers.base import BaseSolver


class KnightSolver(BaseSolver):
    def __init__(self):
        super().__init__()
        self.algorithm_used = "warnsdorff"
        self.moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]

    def solve(self, input_data: dict, options: dict) -> Optional[List[Tuple[int, int]]]:
        self.start_timer()

        if not self.validate_input(input_data):
            return None

        n = input_data['n']
        start = tuple(input_data['start'])
        closed_tour = input_data.get('closed_tour', False)
        algorithm = options.get('algorithm', 'warnsdorff')

        self.algorithm_used = algorithm

        if algorithm == 'warnsdorff':
            return self._warnsdorff_tour(n, start, closed_tour,
                                         options.get('return_steps', True))
        else:
            return self._backtrack_tour(n, start, closed_tour,
                                        options.get('return_steps', True))

    def validate_input(self, input_data: dict) -> bool:
        n = input_data.get('n', 0)
        if n < 5 or n > 8:
            return False

        start = input_data.get('start')
        if not start or len(start) != 2:
            return False

        if not (0 <= start[0] < n and 0 <= start[1] < n):
            return False

        return True

    def _is_safe(self, x: int, y: int, board: List[List[int]], n: int) -> bool:
        return 0 <= x < n and 0 <= y < n and board[x][y] == -1

    def _count_onward_moves(self, x: int, y: int, board: List[List[int]], n: int) -> int:
        count = 0
        for dx, dy in self.moves:
            if self._is_safe(x + dx, y + dy, board, n):
                count += 1
        return count

    def _warnsdorff_tour(self, n: int, start: Tuple[int, int],
                         closed_tour: bool, track_steps: bool) -> Optional[List[Tuple[int, int]]]:
        board = [[-1] * n for _ in range(n)]
        path = [start]
        x, y = start
        board[x][y] = 0

        for i in range(1, n * n):
            self.nodes_explored += 1

            next_moves = []
            for dx, dy in self.moves:
                nx, ny = x + dx, y + dy
                if self._is_safe(nx, ny, board, n):
                    accessibility = self._count_onward_moves(nx, ny, board, n)
                    next_moves.append((accessibility, nx, ny))

            if not next_moves:
                if track_steps:
                    self.add_step("dead_end", (x, y), None,
                                  f"Dead end at position {(x, y)}")
                self.backtrack_count += 1
                return None

            next_moves.sort()
            _, x, y = next_moves[0]
            board[x][y] = i
            path.append((x, y))

            if track_steps:
                self.add_step("move", (x, y), i,
                              f"Knight moves to {(x, y)} (move #{i})")

        if closed_tour:
            for dx, dy in self.moves:
                if (x + dx, y + dy) == start:
                    if track_steps:
                        self.add_step("closed", start, None,
                                      "Tour closed successfully")
                    return path
            return None

        return path

    def _backtrack_tour(self, n: int, start: Tuple[int, int],
                        closed_tour: bool, track_steps: bool) -> Optional[List[Tuple[int, int]]]:
        board = [[-1] * n for _ in range(n)]
        path = []

        def solve_util(x: int, y: int, move_count: int) -> bool:
            self.nodes_explored += 1

            if move_count == n * n:
                path.append((x, y))
                if not closed_tour:
                    return True

                for dx, dy in self.moves:
                    if (x + dx, y + dy) == start:
                        if track_steps:
                            self.add_step("closed", start, None,
                                          "Tour closed successfully")
                        return True
                path.pop()
                return False

            board[x][y] = move_count
            path.append((x, y))

            if track_steps:
                self.add_step("move", (x, y), move_count,
                              f"Knight at {(x, y)} (move #{move_count})")

            next_moves = []
            for dx, dy in self.moves:
                nx, ny = x + dx, y + dy
                if self._is_safe(nx, ny, board, n):
                    next_moves.append((nx, ny))

            next_moves.sort(key=lambda pos: self._count_onward_moves(pos[0], pos[1], board, n))

            for nx, ny in next_moves:
                if solve_util(nx, ny, move_count + 1):
                    return True

            board[x][y] = -1
            path.pop()
            self.backtrack_count += 1

            if track_steps:
                self.add_step("backtrack", (x, y), None,
                              f"Backtracking from {(x, y)}")

            return False

        x, y = start
        if solve_util(x, y, 0):
            return path
        return None