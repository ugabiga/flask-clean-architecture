from flasgger import swag_from
from flask import jsonify, request

from app.http.api import api
from app.http.api.v1 import version_prefix
from app.http.requests.v1.tasks import CreateTaskRequest
from app.http.responses import (
    build_response,
)
from app.http.responses.tasks import TaskSchema
from core.use_cases.create_tasks import CreateTaskUseCase

route_name = "tasks"


@swag_from("./task_index.yml")
@api.route(f"{version_prefix}/{route_name}")
def index():
    return jsonify({"result": True})


@api.route(f"{version_prefix}/{route_name}/<int:task_id>")
def detail(task_id):
    return jsonify({"result": True})


@api.route(f"{version_prefix}/{route_name}", methods=["POST"])
def create():
    req = CreateTaskRequest.from_dict(request.get_json())
    output = CreateTaskUseCase().execute(req.to_dto())
    return build_response(output, TaskSchema)


@api.route(f"{version_prefix}/{route_name}", methods=["PUT"])
def update():
    return jsonify({"result": True})


@api.route(f"{version_prefix}/{route_name}", methods=["DELETE"])
def delete():
    return jsonify({"result": True})
