import traceback
from datetime import datetime
from typing import List


class Exam:
    id: str = "0"
    chapter: str = ""
    title: str = ""
    parentId: str = "0"
    submitEnd: int = 0
    end_time: str = ""

    def __init__(self, data: dict):
        self.id = data.get("id", "0")
        self.title = data.get("title", "")
        self.parentId = data.get("parentId", "0")
        self.submitEnd = data.get("submitEnd", 0) / 1000
        self.end_time = datetime.strftime(datetime.fromtimestamp(self.submitEnd), '%Y-%m-%d %H:%M:%S')


def get_title(chapter_id: str, chapters: List[dict]) -> str:
    for chapter in chapters:
        if chapter.get("id", "0") == chapter_id and chapter.get("title", None) is not None:
            if chapter.get("parentId", None) is None:
                return chapter.get("title", "")
            else:
                return get_title(chapter.get("parentId"), chapters)
    return ""


def get_exam_list(exams: List[dict], chapters: List[dict]) -> List[Exam]:
    exam_list = []
    for exam in exams:
        try:
            exam_ = Exam(exam)
            exam_.chapter = get_title(exam_.parentId, chapters)
            exam_list.append(exam_)
        except Exception as e:  # noqa
            print(traceback.format_exc())
            continue
    return exam_list
