from typing import List, Set, Dict, Optional, Tuple, Any
from collections import defaultdict, deque
import heapq


class Graph:
    def __init__(self, directed: bool = False):
        self.adj_list = defaultdict(list)
        self.directed = directed
        self.vertices = set()

    def add_vertex(self, v):
        self.vertices.add(v)

    def add_edge(self, u, v, weight: float = 1.0):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj_list[u].append((v, weight))
        if not self.directed:
            self.adj_list[v].append((u, weight))

    def get_neighbors(self, v):
        return self.adj_list[v]

    def bfs(self, start, target=None):
        visited = set()
        queue = deque([(start, [start])])
        visited.add(start)
        paths = []

        while queue:
            node, path = queue.popleft()

            if target and node == target:
                return path

            for neighbor, _ in self.adj_list[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
                    paths.append(new_path)

        return paths if not target else None

    def dfs(self, start, target=None):
        visited = set()
        stack = [(start, [start])]
        paths = []

        while stack:
            node, path = stack.pop()

            if node in visited:
                continue

            visited.add(node)

            if target and node == target:
                return path

            for neighbor, _ in self.adj_list[node]:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    stack.append((neighbor, new_path))
                    paths.append(new_path)

        return paths if not target else None

    def astar(self, start, goal, heuristic):
        open_set = [(0, start, [start])]
        closed_set = set()
        g_score = {start: 0}

        while open_set:
            _, current, path = heapq.heappop(open_set)

            if current == goal:
                return path

            if current in closed_set:
                continue

            closed_set.add(current)

            for neighbor, weight in self.adj_list[current]:
                if neighbor in closed_set:
                    continue

                tentative_g = g_score[current] + weight

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor, path + [neighbor]))

        return None


class SudokuGraph:
    def __init__(self):
        self.size = 9
        self.graph = Graph()
        self._build_graph()

    def _build_graph(self):
        for i in range(81):
            row, col = i // 9, i % 9

            for j in range(81):
                if i == j:
                    continue

                other_row, other_col = j // 9, j % 9

                if row == other_row or col == other_col:
                    self.graph.add_edge(i, j)
                elif (row // 3 == other_row // 3) and (col // 3 == other_col // 3):
                    self.graph.add_edge(i, j)

    def get_conflicts(self, cell_index: int) -> Set[int]:
        return {neighbor for neighbor, _ in self.graph.get_neighbors(cell_index)}


class ConstraintGraph:
    def __init__(self, variables: List, domains: Dict[Any, List], constraints: List):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.graph = Graph()

        for constraint in constraints:
            for var1 in constraint['variables']:
                for var2 in constraint['variables']:
                    if var1 != var2:
                        self.graph.add_edge(var1, var2)

    def is_consistent(self, assignment: Dict) -> bool:
        for constraint in self.constraints:
            if not self._check_constraint(constraint, assignment):
                return False
        return True

    def _check_constraint(self, constraint, assignment):
        variables = constraint['variables']
        if all(var in assignment for var in variables):
            return constraint['predicate'](assignment)
        return True