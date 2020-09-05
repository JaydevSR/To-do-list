from .taskdata import Table, session
from datetime import datetime


def add_task(new_task: str, date: datetime):
    """
    Add new task to the database.
    :param new_task: The task to be added.
    :param date: The date of the deadline.
    """
    new_row = Table(task=new_task, deadline=date.date())
    session.add(new_row)
    session.commit()
    print("The task has been added!\n")


def delete_task(task_id: int):
    """
    Deletes the task of the given ID.
    """
    session.query(Table).filter(Table.id == task_id).delete()
    session.commit()


def get_tasks(date=None, before=False) -> list:
    """
    Get Tasks from the database.
    :param before: Get tasks before this date.
    :param date: The date of tasks. None returns all tasks.
    :type date: datetime
    """
    if date is None:
        tasks = session.query(Table).all()
    elif before:
        tasks = session.query(Table).filter(Table.deadline < date.date()).all()
    else:
        tasks = session.query(Table).filter(Table.deadline == date.date()).all()
    return tasks
