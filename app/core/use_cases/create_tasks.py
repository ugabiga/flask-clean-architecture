from typing import Any
from typing import Union

from app.core.dtos.tasks import CreateTaskDto
from app.core.entities.tasks import Task
from app.core.repositories.tasks import TaskRepository
from app.core.use_case_outputs import BaseUseCaseSuccessOutput
from app.core.use_case_outputs import UseCaseFailureOutput
from app.core.use_cases import BaseUseCase


class CreateTaskUseCaseOutput(BaseUseCaseSuccessOutput):
    def __init__(self, task: Task) -> None:
        self.task = task

    def get_data(self) -> Task:
        return self.task

    def get_meta(self) -> Any:
        return None


class CreateTaskUseCase(BaseUseCase):
    def __init__(self, task_repository: TaskRepository, dto: CreateTaskDto) -> None:
        self.dto = dto
        self.repository = task_repository

    def execute(self) -> Union[CreateTaskUseCaseOutput, UseCaseFailureOutput]:
        task = self.repository.create_task(
            self.dto.user_id, self.dto.title, self.dto.contents
        )

        if not task:
            return UseCaseFailureOutput.build_not_found_error("task_not_found")

        return CreateTaskUseCaseOutput(task)
