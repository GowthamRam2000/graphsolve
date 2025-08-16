from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.models.schemas import (
    PuzzleRequest, PuzzleResponse, PresetPuzzle,
    SudokuInput, NQueensInput, MazeInput, KnightInput
)
from app.solvers.sudoku import SudokuSolver
from app.solvers.nqueens import NQueensSolver
from app.solvers.maze import MazeSolver
from app.solvers.knight import KnightSolver

router = APIRouter()


class MazeGenerateRequest(BaseModel):
    size: int = 10
    difficulty: str = "medium"


PUZZLE_PRESETS = {
    "sudoku": [
        {
            "id": "sudoku_easy_1",
            "name": "Easy Sudoku #1",
            "difficulty": "easy",
            "data": {
                "grid": [
                    [5, 3, 0, 0, 7, 0, 0, 0, 0],
                    [6, 0, 0, 1, 9, 5, 0, 0, 0],
                    [0, 9, 8, 0, 0, 0, 0, 6, 0],
                    [8, 0, 0, 0, 6, 0, 0, 0, 3],
                    [4, 0, 0, 8, 0, 3, 0, 0, 1],
                    [7, 0, 0, 0, 2, 0, 0, 0, 6],
                    [0, 6, 0, 0, 0, 0, 2, 8, 0],
                    [0, 0, 0, 4, 1, 9, 0, 0, 5],
                    [0, 0, 0, 0, 8, 0, 0, 7, 9]
                ]
            }
        },
        {
            "id": "sudoku_medium_1",
            "name": "Medium Sudoku #1",
            "difficulty": "medium",
            "data": {
                "grid": [
                    [0, 0, 0, 6, 0, 0, 4, 0, 0],
                    [7, 0, 0, 0, 0, 3, 6, 0, 0],
                    [0, 0, 0, 0, 9, 1, 0, 8, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 5, 0, 1, 8, 0, 0, 0, 3],
                    [0, 0, 0, 3, 0, 6, 0, 4, 5],
                    [0, 4, 0, 2, 0, 0, 0, 6, 0],
                    [9, 0, 3, 0, 0, 0, 0, 0, 0],
                    [0, 2, 0, 0, 0, 0, 1, 0, 0]
                ]
            }
        },
        {
            "id": "sudoku_hard_1",
            "name": "Hard Sudoku #1",
            "difficulty": "hard",
            "data": {
                "grid": [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 3, 0, 8, 5],
                    [0, 0, 1, 0, 2, 0, 0, 0, 0],
                    [0, 0, 0, 5, 0, 7, 0, 0, 0],
                    [0, 0, 4, 0, 0, 0, 1, 0, 0],
                    [0, 9, 0, 0, 0, 0, 0, 0, 0],
                    [5, 0, 0, 0, 0, 0, 0, 7, 3],
                    [0, 0, 2, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 4, 0, 0, 0, 9]
                ]
            }
        }
    ],
    "nqueens": [
        {
            "id": "nqueens_4",
            "name": "4-Queens",
            "difficulty": "easy",
            "data": {"n": 4, "preset_queens": []}
        },
        {
            "id": "nqueens_6",
            "name": "6-Queens",
            "difficulty": "medium",
            "data": {"n": 6, "preset_queens": []}
        },
        {
            "id": "nqueens_8",
            "name": "8-Queens",
            "difficulty": "hard",
            "data": {"n": 8, "preset_queens": []}
        }
    ],
    "maze": [
        {
            "id": "maze_small",
            "name": "Small Maze",
            "difficulty": "easy",
            "data": {
                "grid": [
                    [0, 0, 1, 0, 0],
                    [1, 0, 1, 0, 1],
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0]
                ],
                "start": [0, 0],
                "end": [4, 4]
            }
        },
        {
            "id": "maze_medium",
            "name": "Medium Maze",
            "difficulty": "medium",
            "data": {
                "grid": [
                    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                    [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0]
                ],
                "start": [0, 0],
                "end": [9, 9]
            }
        }
    ],
    "knight": [
        {
            "id": "knight_5",
            "name": "5x5 Knight's Tour",
            "difficulty": "easy",
            "data": {"n": 5, "start": [0, 0], "closed_tour": False}
        },
        {
            "id": "knight_6",
            "name": "6x6 Knight's Tour",
            "difficulty": "medium",
            "data": {"n": 6, "start": [0, 0], "closed_tour": False}
        },
        {
            "id": "knight_8",
            "name": "8x8 Knight's Tour",
            "difficulty": "hard",
            "data": {"n": 8, "start": [0, 0], "closed_tour": False}
        }
    ]
}


@router.post("/sudoku/solve", response_model=PuzzleResponse)
async def solve_sudoku(request: PuzzleRequest):
    try:
        solver = SudokuSolver()
        solution = solver.solve(request.input, request.options.model_dump())

        if solution:
            return PuzzleResponse(
                success=True,
                solution=solution,
                steps=solver.steps if request.options.return_steps else [],
                statistics=solver.get_statistics()
            )
        else:
            return PuzzleResponse(
                success=False,
                error="No solution found",
                statistics=solver.get_statistics()
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/nqueens/solve", response_model=PuzzleResponse)
async def solve_nqueens(request: PuzzleRequest):
    try:
        solver = NQueensSolver()
        solution = solver.solve(request.input, request.options.model_dump())

        if solution:
            return PuzzleResponse(
                success=True,
                solution=solution,
                steps=solver.steps if request.options.return_steps else [],
                statistics=solver.get_statistics()
            )
        else:
            return PuzzleResponse(
                success=False,
                error="No solution found",
                statistics=solver.get_statistics()
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/maze/solve", response_model=PuzzleResponse)
async def solve_maze(request: PuzzleRequest):
    try:
        solver = MazeSolver()
        solution = solver.solve(request.input, request.options.model_dump())

        if solution:
            return PuzzleResponse(
                success=True,
                solution=solution,
                steps=solver.steps if request.options.return_steps else [],
                statistics=solver.get_statistics()
            )
        else:
            return PuzzleResponse(
                success=False,
                error="No path found",
                statistics=solver.get_statistics()
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/knight/solve", response_model=PuzzleResponse)
async def solve_knight(request: PuzzleRequest):
    try:
        solver = KnightSolver()
        solution = solver.solve(request.input, request.options.model_dump())

        if solution:
            return PuzzleResponse(
                success=True,
                solution=solution,
                steps=solver.steps if request.options.return_steps else [],
                statistics=solver.get_statistics()
            )
        else:
            return PuzzleResponse(
                success=False,
                error="No tour found",
                statistics=solver.get_statistics()
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/puzzles/presets/{puzzle_type}")
async def get_presets(puzzle_type: str):
    if puzzle_type not in PUZZLE_PRESETS:
        raise HTTPException(status_code=404, detail="Puzzle type not found")

    return PUZZLE_PRESETS[puzzle_type]


@router.get("/puzzles/algorithms/{puzzle_type}")
async def get_algorithms(puzzle_type: str):
    algorithms = {
        "sudoku": ["backtracking", "constraint_propagation"],
        "nqueens": ["backtracking"],
        "maze": ["bfs", "dfs", "astar"],
        "knight": ["warnsdorff", "backtracking"]
    }

    if puzzle_type not in algorithms:
        raise HTTPException(status_code=404, detail="Puzzle type not found")

    return {"algorithms": algorithms[puzzle_type]}


@router.post("/maze/generate")
async def generate_maze(request: MazeGenerateRequest):
    # Ensure size is an integer and within valid range
    size = int(request.size)
    if size < 5 or size > 50:
        raise HTTPException(status_code=400, detail="Size must be between 5 and 50")

    from app.solvers.maze import MazeSolver

    # Generate maze (the function will handle odd/even conversion internally)
    maze = MazeSolver.generate_maze(size, size, request.difficulty)

    # Ensure we return the correct size grid (trim if necessary)
    if len(maze) > size:
        maze = maze[:size]
    if len(maze[0]) > size:
        maze = [row[:size] for row in maze]

    return {
        "grid": maze,
        "start": [0, 0],
        "end": [size - 1, size - 1]
    }