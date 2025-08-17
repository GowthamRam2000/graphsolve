from typing import List, Optional, Tuple
from app.solvers.base import BaseSolver
import time


class KnightSolver(BaseSolver):
    def __init__(self):
        super().__init__()
        self.algorithm_used = "warnsdorff"
        self.moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        self.timeout = 10  # 10 seconds timeout for backtracking

    def solve(self, input_data: dict, options: dict) -> Optional[List[Tuple[int, int]]]:
        self.start_timer()

        if not self.validate_input(input_data):
            return None

        n = input_data['n']
        start = tuple(input_data['start'])
        closed_tour = input_data.get('closed_tour', False)
        algorithm = options.get('algorithm', 'warnsdorff')

        # Check if board size is too small for a tour
        if n < 5:
            if n == 3 or n == 4:
                # No tour exists for 3x3 or 4x4 boards
                return None

        self.algorithm_used = algorithm

        if algorithm == 'warnsdorff':
            return self._warnsdorff_tour(n, start, closed_tour,
                                         options.get('return_steps', True))
        else:
            # Use optimized backtracking with timeout
            return self._backtrack_tour_optimized(n, start, closed_tour,
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

    def _get_next_moves(self, x: int, y: int, board: List[List[int]], n: int) -> List[Tuple[int, int, int]]:
        """Get next moves sorted by Warnsdorff's heuristic (accessibility)"""
        next_moves = []
        for dx, dy in self.moves:
            nx, ny = x + dx, y + dy
            if self._is_safe(nx, ny, board, n):
                accessibility = self._count_onward_moves(nx, ny, board, n)
                next_moves.append((accessibility, nx, ny))

        # Sort by accessibility (Warnsdorff's heuristic - choose least accessible squares first)
        next_moves.sort()
        return next_moves

    def _warnsdorff_tour(self, n: int, start: Tuple[int, int],
                         closed_tour: bool, track_steps: bool) -> Optional[List[Tuple[int, int]]]:
        board = [[-1] * n for _ in range(n)]
        path = [start]
        x, y = start
        board[x][y] = 0

        for i in range(1, n * n):
            self.nodes_explored += 1

            # Get next moves sorted by Warnsdorff's heuristic
            next_moves = self._get_next_moves(x, y, board, n)

            if not next_moves:
                if track_steps:
                    self.add_step("dead_end", (x, y), None,
                                  f"Dead end at position {(x, y)}")
                self.backtrack_count += 1

                # Try backtracking with different choices if we hit a dead end early
                if i < n * n - 5:  # If we're not near the end, try alternative
                    return self._warnsdorff_with_backtrack(n, start, closed_tour, track_steps)
                return None

            # Choose the square with minimum accessibility
            _, x, y = next_moves[0]
            board[x][y] = i
            path.append((x, y))

            if track_steps:
                self.add_step("move", (x, y), i,
                              f"Knight moves to {(x, y)} (move #{i})")

        # Check if it's a closed tour
        if closed_tour:
            for dx, dy in self.moves:
                if (x + dx, y + dy) == start:
                    if track_steps:
                        self.add_step("closed", start, None,
                                      "Tour closed successfully")
                    return path
            return None

        return path

    def _warnsdorff_with_backtrack(self, n: int, start: Tuple[int, int],
                                   closed_tour: bool, track_steps: bool) -> Optional[List[Tuple[int, int]]]:
        """Warnsdorff's with limited backtracking when stuck"""
        board = [[-1] * n for _ in range(n)]
        path = []
        start_time = time.time()

        def solve_util(x: int, y: int, move_count: int) -> bool:
            # Check timeout
            if time.time() - start_time > self.timeout:
                return False

            self.nodes_explored += 1

            if move_count == n * n:
                path.append((x, y))
                if not closed_tour:
                    return True

                # Check if it's a valid closed tour
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

            if track_steps and move_count % 10 == 0:  # Log every 10th move
                self.add_step("move", (x, y), move_count,
                              f"Knight at {(x, y)} (move #{move_count})")

            # Get next moves sorted by Warnsdorff's heuristic
            next_moves = self._get_next_moves(x, y, board, n)

            # Try each move
            for _, nx, ny in next_moves:
                if solve_util(nx, ny, move_count + 1):
                    return True

            # Backtrack
            board[x][y] = -1
            path.pop()
            self.backtrack_count += 1

            return False

        x, y = start
        if solve_util(x, y, 0):
            return path
        return None

    def _backtrack_tour_optimized(self, n: int, start: Tuple[int, int],
                                  closed_tour: bool, track_steps: bool) -> Optional[List[Tuple[int, int]]]:
        """Optimized backtracking with Warnsdorff's heuristic for move ordering"""
        board = [[-1] * n for _ in range(n)]
        path = []
        start_time = time.time()
        best_path = []
        max_length = 0

        def solve_util(x: int, y: int, move_count: int) -> bool:
            nonlocal max_length, best_path

            # Check timeout
            if time.time() - start_time > self.timeout:
                # Return best partial solution found
                if max_length > n * n * 0.8:  # If we found 80% of the tour
                    path[:] = best_path[:]
                    return True
                return False

            self.nodes_explored += 1

            # Update best path if current is longer
            if move_count > max_length:
                max_length = move_count
                best_path = path[:]
                best_path.append((x, y))

            if move_count == n * n:
                path.append((x, y))
                if not closed_tour:
                    return True

                # Check for closed tour
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

            if track_steps and move_count % 10 == 0:
                self.add_step("move", (x, y), move_count,
                              f"Knight at {(x, y)} (move #{move_count})")

            # Get next moves sorted by Warnsdorff's heuristic
            next_moves = self._get_next_moves(x, y, board, n)

            # For smaller boards or when close to completion, try all moves
            # For larger boards, limit to top candidates to avoid timeout
            max_candidates = len(next_moves) if n <= 6 or move_count > n * n * 0.9 else min(3, len(next_moves))

            for i in range(max_candidates):
                _, nx, ny = next_moves[i]
                if solve_util(nx, ny, move_count + 1):
                    return True

            board[x][y] = -1
            path.pop()
            self.backtrack_count += 1

            if track_steps and self.backtrack_count % 100 == 0:
                self.add_step("backtrack", (x, y), None,
                              f"Backtracking from {(x, y)} ({self.backtrack_count} backtracks)")

            return False

        x, y = start
        if solve_util(x, y, 0):
            return path

        # If no complete solution found but we have a good partial solution
        if max_length > n * n * 0.8:
            if track_steps:
                self.add_step("partial", None, max_length,
                              f"Found partial tour of length {max_length}")
            return best_path

        return None

    def _is_tour_possible(self, n: int) -> bool:
        """Check if a tour is theoretically possible for the given board size"""
        # Knight's tour is not possible for boards smaller than 5x5
        # except for 3x4 and 4x3 which have tours
        if n < 5:
            return False
        return True