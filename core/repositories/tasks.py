from abc import ABC
from typing import List, Optional

from core.entities.tasks import Task


class TaskRepository(ABC):
    def create_task(self, user_id: int, title: str, contents: str) -> Task:
        raise NotImplementedError()

    def update_task(self, dto: Task) -> Optional[Task]:
        raise NotImplementedError()

    def read_task(self, task_id) -> Optional[Task]:
        raise NotImplementedError()

    def get_tasks(self, previous_id: int, limit: int) -> List[Task]:
        raise NotImplementedError()

    def delete_all_tasks(self) -> bool:
        raise NotImplementedError()
