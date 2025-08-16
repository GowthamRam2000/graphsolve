import time
from functools import wraps
from typing import Any, Callable
import asyncio


def timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {(end - start) * 1000:.2f}ms")
        return result

    return wrapper


def async_timer(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {(end - start) * 1000:.2f}ms")
        return result

    return wrapper


def timeout(seconds: int):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(
                    asyncio.create_task(func(*args, **kwargs)),
                    timeout=seconds
                )
            except asyncio.TimeoutError:
                raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            import signal

            def timeout_handler(signum, frame):
                raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")

            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def validate_grid_dimensions(grid: list, expected_rows: int, expected_cols: int) -> bool:
    if len(grid) != expected_rows:
        return False
    for row in grid:
        if len(row) != expected_cols:
            return False
    return True


def print_sudoku_grid(grid: list):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            if j == 8:
                print(grid[i][j])
            else:
                print(str(grid[i][j]) + " ", end="")


def print_maze(grid: list, path: list = None):
    if path:
        path_set = set(path)
    else:
        path_set = set()

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if (i, j) in path_set:
                print("*", end=" ")
            elif cell == 0:
                print(".", end=" ")
            else:
                print("#", end=" ")
        print()


def print_chessboard(n: int, positions: list):
    board = [["." for _ in range(n)] for _ in range(n)]

    for i, (row, col) in enumerate(positions):
        board[row][col] = str(i) if len(positions) > 1 else "Q"

    for row in board:
        print(" ".join(row))
    print()


def generate_empty_sudoku():
    return [[0 for _ in range(9)] for _ in range(9)]


def generate_empty_maze(rows: int, cols: int):
    return [[0 for _ in range(cols)] for _ in range(rows)]


def is_valid_position(pos: tuple, rows: int, cols: int) -> bool:
    row, col = pos
    return 0 <= row < rows and 0 <= col < cols