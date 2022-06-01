from typing import List


class Course:
    course_id: str = "0"
    title: str = ""
    owner_id: str = "0"

    def __init__(self, data: dict):
        self.course_id = data.get("courseId", "0")
        self.title = data.get("title", "")
        self.owner_id = data.get("ownerId", "0")


def get_course_list(courses: List[dict]) -> List[Course]:
    course_list = []
    for course in courses:
        try:
            course_list.append(Course(course))
        except Exception as e:
            print(e)
            continue
    return course_list


def print_course_list(course_list: List[Course]) -> None:
    for course in course_list:
        print(f"{course.title} | {course.course_id}")
