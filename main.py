from coloredlogs import ColoredFormatter
from logging import getLogger, StreamHandler, CRITICAL, INFO, basicConfig
from sys import exit

from defs.core import Core
from defs.export import export_exam_list
from model.course import get_course_list, print_course_list
from model.exam import get_exam_list
from model.task import get_task_list

logs = getLogger(__name__)
logging_format = "%(levelname)s [%(asctime)s] [%(name)s] %(message)s"
logging_handler = StreamHandler()
logging_handler.setFormatter(ColoredFormatter(logging_format))
root_logger = getLogger()
root_logger.setLevel(CRITICAL)
root_logger.addHandler(logging_handler)
basicConfig(level=INFO)
logs.setLevel(INFO)

core = Core("", "")
sid = input("请输入 sid：")
core.login_use_sid(sid)
# 获取课程列表
courses = core.get_course()
if courses.get("code", 0) != 200:
    logs.error("获取课程列表失败")
    exit(1)
course_list = get_course_list(courses.get("data", []))
print_course_list(course_list)
if not course_list:
    logs.warning("无课程")
    exit(0)
# 输入需要输出的课程
while 1:
    try:
        course_id = input("请输入课程ID：")
    except KeyboardInterrupt:
        break
    course = None
    for i in course_list:
        if course_id == i.course_id:
            course = i
            break
    if not course:
        logs.error("课程 id 错误，请重新输入")
    else:
        # 获取章节列表
        chapters = core.get_chapters_info(course_id)
        all_exams = []
        # 获取测验列表
        exams = core.get_exam_info(course_id)
        [all_exams.append(i) for i in exams.get("data", [])]
        # 获取考试列表
        exams_main = core.get_exam_main_info(course_id)
        [all_exams.append(i) for i in exams_main.get("data", [])]
        exam_list = get_exam_list(core, course_id, all_exams, chapters.get("data", []))
        tasks = core.get_task_info(course_id)
        task_list = get_task_list(tasks.get("data", []))
        # 导出
        export_exam_list(course, exam_list, task_list)
        logs.info(f"{course.title} | 导出成功")
