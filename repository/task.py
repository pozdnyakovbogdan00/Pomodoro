from sqlalchemy.orm import Session
from sqlalchemy.sql import select, delete, update
from models import Task, Category

class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self):
        qwery = select(Task)
        with self.db_session() as session:
            task = session.execute(qwery).scalars().all()
        return task

    def get_task(self, task_id: int) -> Task | None:
        qwery = select(Task).where(Task.id == task_id)
        with self.db_session() as session:
            task = session.execute(qwery).scalar_one_or_none()
        return task

    def create_task(self, task: Task) -> None:
        task_model = Task(name=task.name, pomodoro_count=task.pomodoro_count, category_id=task.category_id)
        with self.db_session() as session:
            session.add(task_model)
            session.commit()

    def edit_task(self, task_id: int, name: str) -> None:
        task = self.get_task(task_id)
        if task is None:
            return {"message": "Task not found"}
        qwery = update(Task).where(Task.id == task_id).values(name=name)
        with self.db_session() as session:
            session.execute(qwery)
            session.commit()
        return {"message": "Task updated"}

    def delete_task(self, task_id: int) -> None:
        task = self.get_task(task_id)
        if task is None:
            return {"message": "Task not found"}
        qwery = delete(Task).where(Task.id == task_id)
        with self.db_session() as session:
            session.execute(qwery)
            session.commit()
        return {"message": "Task deleted"}

    def get_task_by_category(self, category_name: str) -> list[Task] | None:
        qwery = select(Task).join(Category, Task.category_id == Category.id).where(Category.name == category_name)
        with self.db_session() as session:
            task: list[Task] = session.execute(qwery).scalars().all()
            return task




