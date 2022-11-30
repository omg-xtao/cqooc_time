from typing import List, Optional

from openpyxl import Workbook, load_workbook
from os.path import isfile

from model.course import Course
from model.exam import Exam
from model.task import Task


def export_exam_list(course: Course, exam_list: List[Exam], task_list: List[Task]) -> None:
    if isfile("exams.xlsx"):
        wb = load_workbook('exams.xlsx')
    else:
        # 创建一个工作簿对象
        wb = Workbook()
    # 创建一个名为 课程名称 的 sheet 页
    ws = wb.create_sheet(course.title)
    if "Sheet" in wb.get_sheet_names():
        wb.remove_sheet(wb["Sheet"])
    # 标题
    ws["A1"] = "课程名称"
    ws["B1"] = "章节名称"
    ws["C1"] = "测验名称"
    ws["D1"] = "测验结束时间"
    ws["E1"] = "测验结束时间戳"
    ws["F1"] = "已回答答案"
    # 写入 exam_list
    for i, exam in enumerate(exam_list):
        ws.cell(row=i + 2, column=1, value=course.title)
        ws.cell(row=i + 2, column=2, value=exam.chapter)
        ws.cell(row=i + 2, column=3, value=exam.title)
        ws.cell(row=i + 2, column=4, value=exam.end_time)
        ws.cell(row=i + 2, column=5, value=exam.submitEnd)
        ws.cell(row=i + 2, column=6, value=exam.answer)
    # 写入 task_list
    for i, task in enumerate(task_list):
        ws.cell(row=i + 2 + len(exam_list), column=1, value=course.title)
        ws.cell(row=i + 2 + len(exam_list), column=2, value=task.chapter)
        ws.cell(row=i + 2 + len(exam_list), column=3, value=task.title)
        ws.cell(row=i + 2 + len(exam_list), column=4, value=task.end_time)
        ws.cell(row=i + 2 + len(exam_list), column=5, value=task.submitEnd)
        ws.cell(row=i + 2 + len(exam_list), column=6, value="")
    # 将创建的工作簿保存为 exams.xlsx
    wb.save("exams.xlsx")
    # 最后关闭文件
    wb.close()
