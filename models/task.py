from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ToolCall:
    """Représente un appel d'outil effectué par l'agent."""
    name: str
    inputs: dict[str, Any]
    output: str = ""


@dataclass
class AgentResult:
    """Résultat final produit par l'agent après toutes ses itérations."""
    task: str
    summary: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    iterations: int = 0
    status: TaskStatus = TaskStatus.COMPLETED

    def to_dict(self) -> dict[str, Any]:
        return {
            "task": self.task,
            "status": self.status.value,
            "iterations": self.iterations,
            "tool_calls": [
                {"tool": tc.name, "inputs": tc.inputs, "output_preview": tc.output[:200]}
                for tc in self.tool_calls
            ],
            "summary": self.summary,
        }
