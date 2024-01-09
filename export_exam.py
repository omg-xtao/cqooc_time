# 导出已公布答案的测试题

from sys import exit

from defs.core import Core
from defs.export_answer import export
from logs import logs
from model.course import get_course_list, print_course_list
from model.exam_answer import get_all_exam

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
    exit(1)
course_id = input("请输入课程ID：")
course = None
for i in course_list:
    if course_id == i.course_id:
        course = i
        break
if not course:
    logs.error(f"课程 id 错误 ID：{course_id}")
    exit(1)
exams_main = core.get_exam_papers_info(course_id)
data = get_all_exam(core, course, exams_main.get("data", []))
export(data)
logs.info(f"{course.title} | 导出成功")
