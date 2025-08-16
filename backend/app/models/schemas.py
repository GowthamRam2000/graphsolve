from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from enum import Enum

class AlgorithmType(str, Enum):
    BACKTRACKING = "backtracking"
    BFS = "bfs"
    DFS = "dfs"
    ASTAR = "astar"
    CONSTRAINT_PROPAGATION = "constraint_propagation"
    WARNSDORFF = "warnsdorff"

class PuzzleType(str, Enum):
    SUDOKU = "sudoku"
    NQUEENS = "nqueens"
    MAZE = "maze"
    KNIGHT = "knight"

class SolveOptions(BaseModel):
    algorithm: Optional[str] = "backtracking"
    return_steps: bool = True
    max_solutions: int = 1
    timeout: int = 30

class SudokuInput(BaseModel):
    grid: List[List[int]] = Field(..., description="9x9 grid with 0 for empty cells")

class NQueensInput(BaseModel):
    n: int = Field(..., ge=4, le=12, description="Board size")
    preset_queens: Optional[List[tuple[int, int]]] = []

class MazeInput(BaseModel):
    grid: List[List[int]] = Field(..., description="Maze grid where 0=path, 1=wall")
    start: tuple[int, int] = Field(..., description="Starting position (row, col)")
    end: tuple[int, int] = Field(..., description="Ending position (row, col)")

class KnightInput(BaseModel):
    n: int = Field(..., ge=5, le=8, description="Board size")
    start: tuple[int, int] = Field(..., description="Starting position (row, col)")
    closed_tour: bool = False

class PuzzleRequest(BaseModel):
    puzzle_type: PuzzleType
    input: Dict[str, Any]
    options: Optional[SolveOptions] = SolveOptions()

class SolutionStep(BaseModel):
    action: str
    position: Optional[tuple[int, int]] = None
    value: Optional[Any] = None
    description: str

class Statistics(BaseModel):
    time_ms: float
    nodes_explored: int
    algorithm_used: str
    backtrack_count: Optional[int] = 0

class PuzzleResponse(BaseModel):
    success: bool
    solution: Optional[Any] = None
    steps: Optional[List[SolutionStep]] = []
    statistics: Optional[Statistics] = None
    error: Optional[str] = None
    message: Optional[str] = None

class PresetPuzzle(BaseModel):
    id: str
    name: str
    difficulty: Literal["easy", "medium", "hard", "expert"]
    data: Dict[str, Any]