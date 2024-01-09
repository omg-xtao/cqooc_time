from datetime import datetime
from typing import List


class Course:
    course_id: str = "0"
    title: str = ""
    start_time: datetime = datetime.now()
    end_time: datetime = datetime.now()

    def __init__(self, data: dict):
        self.course_id = data.get("id", "0")
        self.title = data.get("title", "")
        self.start_time = datetime.fromtimestamp(data.get("startDate", 0) / 1000)
        self.end_time = datetime.fromtimestamp(data.get("endDate", 0) / 1000)

    @property
    def start_time_str(self) -> str:
        return self.start_time.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def end_time_str(self) -> str:
        return self.end_time.strftime("%Y-%m-%d %H:%M:%S")


def get_course_list(courses: List[dict]) -> List[Course]:
    course_list = []
    for msc in courses:
        try:
            course_list.append(Course(msc["course"]))
        except Exception as e:
            print(e)
            continue
    course_list.sort(key=lambda x: x.start_time, reverse=True)
    return course_list


def print_course_list(course_list: List[Course]) -> None:
    for course in course_list:
        print(f"{course.title} | {course.course_id} | {course.start_time_str} - {course.end_time_str}")
