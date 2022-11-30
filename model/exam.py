import traceback
from datetime import datetime
from time import sleep
from typing import List


class Exam:
    id: str = "0"
    chapter: str = ""
    title: str = ""
    parentId: str = "0"
    submitEnd: int = 0
    end_time: str = ""
    answer: str = ""

    def __init__(self, data: dict):
        self.id = data.get("id", "0")
        self.title = data.get("title", "")
        self.parentId = data.get("parentId", "0")
        self.submitEnd = data.get("submitEnd", 0) / 1000
        self.end_time = datetime.strftime(datetime.fromtimestamp(self.submitEnd), '%Y-%m-%d %H:%M:%S')
        self.answer = ""

    def parse_answer(self, body, data):
        # 题目顺序
        new_list = []
        new_list_pan = []
        new_list.extend(j["id"] for j in body[0]["questions"])
        new_list.extend(j["id"] for j in body[1]["questions"])
        new_list_pan.extend(j["id"] for j in body[4]["questions"])
        # 计算最高得分
        try:
            score_log = data[0]["scoreLog"]
        except IndexError:
            return
        max_score = 0.0
        max_score_index = 0
        for score in score_log:
            score_ = sum(float(values.get("get", 0.0)) for values in score.values())
            if score_ > max_score:
                max_score = score_
                max_score_index = score_log.index(score)
        # 获取最高得分的答案
        answer = data[0]["body"][max_score_index]
        answer_map = {}
        for key, value in answer.items():
            if isinstance(value, list):
                temp = "".join(chr(ord(i) + 17) for i in value)
                answer_map[key] = f" {temp} "
            elif isinstance(value, str):
                answer_map[key] = chr(ord(value) + 17)
        for i in new_list:
            self.answer += answer_map.get(f"q{i}", "_")
        for i in new_list_pan:
            self.answer += chr(ord(answer_map.get(f"q{i}", "`")) - 1)


def get_title(chapter_id: str, chapters: List[dict]) -> str:
    for chapter in chapters:
        if chapter.get("id", "0") == chapter_id and chapter.get("title", None) is not None:
            if chapter.get("parentId", None) is None:
                return chapter.get("title", "")
            else:
                return get_title(chapter.get("parentId"), chapters)
    return ""


def get_exam_list(core, course_id: str, exams: List[dict], chapters: List[dict]) -> List[Exam]:
    exam_list = []
    for exam in exams:
        try:
            exam_ = Exam(exam)
            info = core.get_paper_info(course_id, exam_.id)
            if info.get("body", 0) != 0:
                answer = core.get_paper_answer(course_id, exam_.id)
                if answer.get("code", 0) == 200:
                    exam_.parse_answer(info["body"], answer.get("data", {}))
                sleep(.5)
            print("ok")
            exam_.chapter = get_title(exam_.parentId, chapters)
            exam_list.append(exam_)
        except Exception as e:  # noqa
            print(traceback.format_exc())
            continue
    return exam_list
