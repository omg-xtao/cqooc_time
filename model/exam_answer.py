import traceback
from time import sleep
from typing import List, TYPE_CHECKING, Optional

from pydantic import BaseModel
from tqdm import tqdm

from logs import logs
from model.exam import Exam

if TYPE_CHECKING:
    from model.course import Course
    from defs.core import Core


class DanXuanQuestionBody(BaseModel):
    choices: List[str]
    """选项"""
    answer: List[int]
    """答案"""


class TianKongQuestionBody(BaseModel):
    answer: List[str]
    """答案"""


class PanDuanQuestionBody(BaseModel):
    answer: int
    """答案"""


class BaseQuestion(BaseModel):
    id: int
    question: str
    """题目"""
    resolution: Optional[str] = ""
    """解析"""


class DanXuanQuestion(BaseQuestion):
    body: DanXuanQuestionBody
    """题目内容"""


class TianKongQuestion(BaseQuestion):
    body: TianKongQuestionBody
    """题目内容"""


class PanDuanQuestion(BaseQuestion):
    body: PanDuanQuestionBody
    """题目内容"""


class ExamQuestion(BaseModel):
    danxuan: List[DanXuanQuestion] = []
    """单选题"""
    tiankong: List[TianKongQuestion] = []
    """填空题"""
    panduan: List[PanDuanQuestion] = []
    """判断题"""


def parse_exam(data: ExamQuestion, info: dict):
    for body in info["body"]:
        if not body["questions"]:
            continue
        if body["type"] == "0":
            data.danxuan.extend(DanXuanQuestion(**i) for i in body["questions"])
        elif body["type"] == "1":
            logs.warning(f"暂不支持多选题 {info['title']}")
        elif body["type"] == "2":
            data.tiankong.extend(TianKongQuestion(**i) for i in body["questions"])
        elif body["type"] == "3":
            logs.warning(f"暂不支持简答题 {info['title']}")
        elif body["type"] == "4":
            data.panduan.extend(PanDuanQuestion(**i) for i in body["questions"])


def get_all_exam(core: "Core", course: "Course", exams: List[dict]) -> ExamQuestion:
    data = ExamQuestion()
    for exam in tqdm(exams):
        try:
            exam_ = Exam(exam, course.title)
            info = core.get_paper_info(course.course_id, exam_.id)
            if info.get("body", 0) != 0:
                parse_exam(data, info)
                sleep(.5)
        except Exception as e:  # noqa
            print(f"解析失败：{exam.get('title', '')}")
            print(traceback.format_exc())
            continue
    return data
