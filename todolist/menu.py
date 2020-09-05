from sql_sess import Table, session
from datetime import datetime, timedelta


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


def menu():
    menu_items = {1: "Today's tasks",
                  2: "Week's tasks",
                  3: "All tasks",
                  4: "Missed tasks",
                  5: "Add task",
                  6: "Delete task",
                  0: "Exit"}
    for key, value in menu_items.items():
        print(f"{key}) {value}")

    select = input()
    print("")

    if select == '1':
        date = datetime.today()
        tasks = get_tasks(date)
        print(f"Today {date.day} {date.strftime('%b')}:")
        if len(tasks) == 0:
            print("Nothing to do!\n")
        else:
            for sr, task in enumerate(tasks):
                print(f'{sr + 1}. {task}\n')

    elif select == '2':
        week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        date = datetime.today() - timedelta(days=1)
        for i in range(7):
            date = date + timedelta(days=1)
            tasks = get_tasks(date)
            print(f"{week[date.weekday()]} {date.day} {date.strftime('%b')}:")
            if len(tasks) == 0:
                print("Nothing to do!\n")
            else:
                for sr, task in enumerate(tasks):
                    print(f"{sr + 1}. {task}\n")

    elif select == '3':
        print("All tasks:")
        all_tasks = get_tasks()
        all_tasks.sort(key=lambda elem: elem.deadline)
        for num, task in enumerate(all_tasks):
            print(f"{num+1}. {task}. {task.deadline.day} {task.deadline.strftime('%b')}")
        print("")

    elif select == '4':
        all_tasks = get_tasks(datetime.today(), before=True)
        all_tasks.sort(key=lambda elem: elem.deadline)
        print("Missed tasks:")
        for num, task in enumerate(all_tasks):
            print(f"{num+1}. {task}. {task.deadline.day} {task.deadline.strftime('%b')}")
        print("")

    elif select == '5':
        new_task = input("Enter task\n")
        deadline = input("Enter deadline\n")
        year, month, day = map(int, deadline.split("-"))
        date = datetime(year, month, day)
        add_task(new_task, date)

    elif select == '6':
        print("Choose the number of task you want to delete:")
        all_tasks = get_tasks()
        all_tasks.sort(key=lambda elem: elem.deadline)
        for num, task in enumerate(all_tasks):
            print(f"{num+1}. {task}. {task.deadline.day} {task.deadline.strftime('%b')}")
        task_num = int(input())
        task_id = all_tasks[task_num-1].id
        delete_task(task_id)
        print("The task has been deleted!\n")

    elif select == '0':
        print("Bye!")
        return False
    else:
        print("Unknown selection")
    return True
