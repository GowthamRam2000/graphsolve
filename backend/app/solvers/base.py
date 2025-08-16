from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict
from app.models.schemas import SolutionStep, Statistics
import time


class BaseSolver(ABC):
    def __init__(self):
        self.steps: List[SolutionStep] = []
        self.nodes_explored = 0
        self.backtrack_count = 0
        self.start_time = None
        self.algorithm_used = "unknown"

    def start_timer(self):
        self.start_time = time.time()

    def get_elapsed_time(self) -> float:
        if self.start_time:
            return (time.time() - self.start_time) * 1000
        return 0

    def add_step(self, action: str, position: Optional[tuple] = None,
                 value: Optional[Any] = None, description: str = ""):
        step = SolutionStep(
            action=action,
            position=position,
            value=value,
            description=description
        )
        self.steps.append(step)

    def get_statistics(self) -> Statistics:
        return Statistics(
            time_ms=self.get_elapsed_time(),
            nodes_explored=self.nodes_explored,
            algorithm_used=self.algorithm_used,
            backtrack_count=self.backtrack_count
        )

    @abstractmethod
    def solve(self, input_data: Dict[str, Any], options: Dict[str, Any]) -> Optional[Any]:
        pass

    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        pass