from typing import Tuple

from bs4 import BeautifulSoup
from pathlib import Path

from model.exam_answer import ExamQuestion, DanXuanQuestion, TianKongQuestion, PanDuanQuestion

no_answer_path = Path("exams.txt")
answer_path = Path("exams_answer.txt")
danxuan_answer_map = {0: "A", 1: "B", 2: "C", 3: "D"}


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    p_all = soup.find_all("p")
    text = ""
    for p in p_all:
        t = p.get_text()
        if not t:
            continue
        text += t + "\n"
    return text.strip()


def export_danxuan(question: DanXuanQuestion) -> Tuple[str, str]:
    title = html_to_text(question.question)
    answer = question.body.answer
    answer_text = danxuan_answer_map.get(answer[0])
    text = f"{title}\n"
    for idx, choice in enumerate(question.body.choices):
        text += f"{danxuan_answer_map.get(idx)}. {choice}\n"
    text_answer = f"{text}\n答案：{answer_text}\n"
    if question.resolution:
        text_answer += f"\n解析：{html_to_text(question.resolution)}\n"
    return text, text_answer


def export_tiankong(question: TianKongQuestion) -> Tuple[str, str]:
    title_raw = html_to_text(question.question)
    title = title_raw.replace("[]", "_____________")
    answer = ", ".join(question.body.answer)
    text = f"{title}\n"
    text_answer = f"{title}\n答案：{answer}\n"
    if question.resolution:
        text_answer += f"\n解析：{html_to_text(question.resolution)}\n"
    return text, text_answer


def export_panduan(question: PanDuanQuestion) -> Tuple[str, str]:
    title = html_to_text(question.question)
    answer = "正确" if question.body.answer == 1 else "错误"
    text = f"{title}\n"
    text_answer = f"{text}\n答案：{answer}\n"
    if question.resolution:
        text_answer += f"\n解析：{html_to_text(question.resolution)}\n"
    return text, text_answer


def export(data: ExamQuestion):
    text_no_answer = ""
    text_answer = ""
    type_map = {"单选": data.danxuan, "填空": data.tiankong, "判断": data.panduan}
    func_map = {"单选": export_danxuan, "填空": export_tiankong, "判断": export_panduan}
    for k, v in type_map.items():
        if v:
            text_no_answer += f"{k}题\n\n"
            text_answer += f"{k}题\n\n"
            for idx, exam in enumerate(v):
                text_, text_answer_ = func_map[k](exam)
                text_no_answer += f"{idx + 1}. {text_}\n"
                text_answer += f"{idx + 1}. {text_answer_}\n"
            text_no_answer += "\n\n"
            text_answer += "\n\n"
    with open(no_answer_path, "w", encoding="utf-8") as f:
        f.write(text_no_answer)
    with open(answer_path, "w", encoding="utf-8") as f:
        f.write(text_answer)
