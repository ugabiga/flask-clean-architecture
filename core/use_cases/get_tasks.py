from dataclasses import dataclass
from typing import List

from core.entities.tasks import Task
from core.repositories.tasks import TaskRepository
from core.use_case_outputs import Failure, Output, Success


@dataclass
class GetUserTasksDto:
    user_id: int
    previous_id: int = 0
    limit: int = 10


class GetTasksByUserUseCase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    def execute(self, dto: GetUserTasksDto) -> Output[List[Task]]:
        tasks = self.task_repository.get_tasks(
            previous_id=dto.previous_id, limit=dto.limit
        )

        if len(tasks) < 1:
            return Failure.build_not_found_error()

        return Success(
            data=tasks, meta={"previous_id": tasks[-1].id, "limit": dto.limit}
        )