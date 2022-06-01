import traceback
from datetime import datetime
from typing import List


class Task:
    id: str = "0"
    title: str = ""
    chapter: str = ""
    submitEnd: int = 0
    end_time: str = ""

    def __init__(self, data: dict):
        self.id = data.get("id", "0")
        self.chapter = data.get("chapter", {}).get("title", "")
        self.title = data.get("title", "")
        self.submitEnd = data.get("submitEnd", 0) / 1000
        self.end_time = datetime.strftime(datetime.fromtimestamp(self.submitEnd), '%Y-%m-%d %H:%M:%S')


def get_task_list(tasks: List[dict], ) -> List[Task]:
    task_list = []
    for task in tasks:
        try:
            task_list.append(Task(task))
        except Exception as e:  # noqa
            print(traceback.format_exc())
            continue
    return task_list
