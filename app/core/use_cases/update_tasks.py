from dataclasses import dataclass
from typing import Any
from typing import Optional
from typing import Union

from app.core.entities.tasks import Task
from app.core.exceptions import NotAuthorizedException
from app.core.exceptions import NotFoundException
from app.core.repositories.tasks import TaskRepository
from app.core.use_case_outputs import BaseUseCaseSuccessOutput
from app.core.use_case_outputs import UseCaseFailureOutput
from app.core.use_cases import BaseUseCase
from app.http.requests.v1.tasks import UpdateTaskRequest


@dataclass
class UpdateTaskDto:
    task_id: int
    title: Optional[str] = None
    contents: Optional[str] = None


class UpdateTaskUseCaseOutput(BaseUseCaseSuccessOutput):
    def __init__(self, task: Task) -> None:
        self.task = task

    def get_data(self) -> Task:
        return self.task

    def get_meta(self) -> Any:
        return None


class UpdateTaskUseCase(BaseUseCase):
    def __init__(
        self, task_repository: TaskRepository, user_id: int, request: UpdateTaskRequest
    ) -> None:
        self.user_id = user_id
        self.request = request
        self.task_repository = task_repository

    def execute(self) -> Union[UpdateTaskUseCaseOutput, UseCaseFailureOutput]:
        dto = self.request.to_dto()

        try:
            self._check_task_authorization(dto)
        except NotFoundException:
            return UseCaseFailureOutput.build_not_found_error("task_not_found")
        except NotAuthorizedException:
            return UseCaseFailureOutput.build_not_authorized_error(
                "not_authorized_action"
            )

        try:
            new_task = self._update_task(dto)
        except NotFoundException:
            return UseCaseFailureOutput.build_not_found_error("task_not_found")

        return UpdateTaskUseCaseOutput(new_task)

    def _check_task_authorization(self, dto: UpdateTaskDto) -> bool:
        task = self.task_repository.read_task(dto.task_id)

        if task is None:
            raise NotFoundException()

        if task.user_id != self.user_id:
            raise NotAuthorizedException()

        return True

    def _update_task(self, dto: UpdateTaskDto) -> Task:
        new_task = self.task_repository.update_task(dto)

        if new_task is None:
            raise NotFoundException()

        return new_task
