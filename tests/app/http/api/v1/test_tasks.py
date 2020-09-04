from app.data.sql.repositories.task import TaskSQLRepository
from tests.helper.request import RequestClient


# noinspection PyUnusedLocal
def test_call_index(client: RequestClient, task_repo: TaskSQLRepository) -> None:
    [task_repo.create_task(i, f"{i}", f"{i}") for i in range(0, 3)]
    tasks = task_repo.get_tasks(0, 10)
    print(tasks)

    resp = client.get("/v1/tasks?previous_id=0&limit=10")

    assert resp.get_status_code() == 200
    assert resp.get_data() == {
        "data": [
            {"contents": "0", "id": 1, "title": "0", "user_id": 0},
            {"contents": "1", "id": 2, "title": "1", "user_id": 1},
            {"contents": "2", "id": 3, "title": "2", "user_id": 2},
        ],
        "meta": {"limit": 10, "previous_id": 3},
    }