from typing import List, Optional, Tuple, Set
from collections import deque
import heapq
from app.solvers.base import BaseSolver


class MazeSolver(BaseSolver):
    def __init__(self):
        super().__init__()
        self.algorithm_used = "bfs"

    def solve(self, input_data: dict, options: dict) -> Optional[List[Tuple[int, int]]]:
        self.start_timer()

        if not self.validate_input(input_data):
            return None

        grid = input_data['grid']
        start = tuple(input_data['start'])
        end = tuple(input_data['end'])
        algorithm = options.get('algorithm', 'bfs')

        self.algorithm_used = algorithm

        if algorithm == 'bfs':
            return self._bfs(grid, start, end, options.get('return_steps', True))
        elif algorithm == 'dfs':
            return self._dfs(grid, start, end, options.get('return_steps', True))
        elif algorithm == 'astar':
            return self._astar(grid, start, end, options.get('return_steps', True))
        else:
            return self._bfs(grid, start, end, options.get('return_steps', True))

    def validate_input(self, input_data: dict) -> bool:
        grid = input_data.get('grid', [])
        if not grid or not all(len(row) == len(grid[0]) for row in grid):
            return False

        start = input_data.get('start')
        end = input_data.get('end')

        if not start or not end:
            return False

        rows, cols = len(grid), len(grid[0])

        if not (0 <= start[0] < rows and 0 <= start[1] < cols):
            return False
        if not (0 <= end[0] < rows and 0 <= end[1] < cols):
            return False

        if grid[start[0]][start[1]] == 1 or grid[end[0]][end[1]] == 1:
            return False

        return True

    def _get_neighbors(self, grid: List[List[int]], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        rows, cols = len(grid), len(grid[0])
        row, col = pos
        neighbors = []

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < rows and 0 <= new_col < cols and
                    grid[new_row][new_col] == 0):
                neighbors.append((new_row, new_col))

        return neighbors

    def _bfs(self, grid: List[List[int]], start: Tuple[int, int],
             end: Tuple[int, int], track_steps: bool) -> Optional[List[Tuple[int, int]]]:
        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            current, path = queue.popleft()
            self.nodes_explored += 1

            if track_steps:
                self.add_step("explore", current, None,
                              f"Exploring position {current}")

            if current == end:
                if track_steps:
                    self.add_step("found", end, None,
                                  f"Found target at {end}")
                return path

            for neighbor in self._get_neighbors(grid, current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

                    if track_steps:
                        self.add_step("enqueue", neighbor, None,
                                      f"Adding {neighbor} to queue")

        return None

    def _dfs(self, grid: List[List[int]], start: Tuple[int, int],
             end: Tuple[int, int], track_steps: bool) -> Optional[List[Tuple[int, int]]]:
        stack = [(start, [start])]
        visited = set()

        while stack:
            current, path = stack.pop()

            if current in visited:
                continue

            visited.add(current)
            self.nodes_explored += 1

            if track_steps:
                self.add_step("explore", current, None,
                              f"Exploring position {current}")

            if current == end:
                if track_steps:
                    self.add_step("found", end, None,
                                  f"Found target at {end}")
                return path

            for neighbor in self._get_neighbors(grid, current):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

                    if track_steps:
                        self.add_step("push", neighbor, None,
                                      f"Adding {neighbor} to stack")

        return None

    def _manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def _astar(self, grid: List[List[int]], start: Tuple[int, int],
               end: Tuple[int, int], track_steps: bool) -> Optional[List[Tuple[int, int]]]:
        open_set = [(0, start, [start])]
        closed_set = set()
        g_score = {start: 0}

        while open_set:
            _, current, path = heapq.heappop(open_set)

            if current in closed_set:
                continue

            closed_set.add(current)
            self.nodes_explored += 1

            if track_steps:
                self.add_step("explore", current, None,
                              f"Exploring position {current} (h={self._manhattan_distance(current, end)})")

            if current == end:
                if track_steps:
                    self.add_step("found", end, None,
                                  f"Found target at {end}")
                return path

            for neighbor in self._get_neighbors(grid, current):
                if neighbor in closed_set:
                    continue

                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self._manhattan_distance(neighbor, end)
                    heapq.heappush(open_set, (f_score, neighbor, path + [neighbor]))

                    if track_steps:
                        self.add_step("evaluate", neighbor, f_score,
                                      f"Evaluating {neighbor} with f-score={f_score}")

        return None

    @staticmethod
    def generate_maze(rows: int, cols: int, difficulty: str = "medium") -> List[List[int]]:
        import random
        from collections import deque

        # Create a maze with all walls
        maze = [[1] * cols for _ in range(rows)]

        # Simple maze generation using Prim's algorithm (guaranteed connected)
        def generate_connected_maze():
            # Start with all walls
            for i in range(rows):
                for j in range(cols):
                    maze[i][j] = 1

            # Mark starting cell as path
            maze[0][0] = 0

            # Walls list (cells that could become paths)
            walls = []

            # Add walls around starting position
            if cols > 1:
                walls.append((0, 1))
            if rows > 1:
                walls.append((1, 0))

            while walls:
                # Pick a random wall
                wall = random.choice(walls)
                y, x = wall
                walls.remove(wall)

                # Count adjacent paths
                adjacent_paths = 0
                for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < rows and 0 <= nx < cols and maze[ny][nx] == 0:
                        adjacent_paths += 1

                # If only one adjacent path, make this a path and add new walls
                if adjacent_paths <= 1:
                    maze[y][x] = 0

                    # Add neighboring walls
                    for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        ny, nx = y + dy, x + dx
                        if (0 <= ny < rows and 0 <= nx < cols and
                                maze[ny][nx] == 1 and (ny, nx) not in walls):
                            walls.append((ny, nx))

        # Generate base maze
        generate_connected_maze()

        # Ensure start and end are paths
        maze[0][0] = 0
        maze[rows - 1][cols - 1] = 0

        # Add additional paths based on difficulty
        if difficulty == "easy":
            # Open up 30% more cells for easy mode
            cells_to_open = (rows * cols) // 3
            for _ in range(cells_to_open):
                y = random.randint(0, rows - 1)
                x = random.randint(0, cols - 1)
                maze[y][x] = 0
        elif difficulty == "medium":
            # Open up 15% more cells for medium mode
            cells_to_open = (rows * cols) // 6
            for _ in range(cells_to_open):
                y = random.randint(0, rows - 1)
                x = random.randint(0, cols - 1)
                maze[y][x] = 0

        # Hard mode keeps the maze as generated (sparse)

        # Ensure path from start to end exists
        def ensure_path_exists():
            # Use BFS to check if path exists
            visited = set()
            queue = deque([(0, 0)])
            visited.add((0, 0))

            while queue:
                y, x = queue.popleft()

                if y == rows - 1 and x == cols - 1:
                    return True  # Path exists

                for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    ny, nx = y + dy, x + dx
                    if (0 <= ny < rows and 0 <= nx < cols and
                            maze[ny][nx] == 0 and (ny, nx) not in visited):
                        visited.add((ny, nx))
                        queue.append((ny, nx))

            return False

        # If no path exists, create one
        if not ensure_path_exists():
            # Create a simple path: go right then down
            # Clear top row
            for x in range(cols):
                maze[0][x] = 0
            # Clear right column
            for y in range(rows):
                maze[y][cols - 1] = 0
            # Add some random paths in between
            for _ in range(rows + cols):
                y = random.randint(0, rows - 1)
                x = random.randint(0, cols - 1)
                maze[y][x] = 0

        return maze