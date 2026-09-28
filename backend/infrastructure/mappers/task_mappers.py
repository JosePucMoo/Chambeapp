from infrastructure.schemas.task_schema import CreateTaskDTO
from infrastructure.db.models.task_model import TaskModel
from domain.entities.task import Task


def map_task_entity_to_model(task: Task) -> TaskModel:
    return TaskModel(
        id=task.id,
        title= task.title, 
    description=task.description,
        priority=task.priority,
        due_date= task.due_date,
        column_id= task.column_id,
        assignee_id= task.assignee_id
    )

def map_task_model_to_entity(task: TaskModel) -> TaskModel:
    return Task(
        id= task.id,
        title= task.title, 
        description= task.description,
        priority= task.priority,
        due_date= task.due_date,
        column_id= task.column_id,
        assignee_id= task.assignee_id
    )

def map_task_dto_to_entity(task: CreateTaskDTO) -> Task:
    return Task(
        title=task.description,
        description=task.description,
        priority=task.priority,
        due_date=task.due_date,
        column_id=task.column_id,
        assignee_id=task.assignee_id
    )