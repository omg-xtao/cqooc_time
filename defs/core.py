# -*- coding: utf-8 -*-
from defs.request import Request
from defs.user import User
from defs.msg import Msg
from defs.test import test
from defs.processer import Processer
from defs.api_url import ApiUrl


class Core:
    def __init__(self, username: str, pwd: str) -> None:
        self.__processer = Processer()
        self.__request = Request()
        self.__api_url = ApiUrl()
        self.__user = User(username, pwd)

    def __process_user_info(self) -> None:
        id_res = self.__request.do_get(
            self.__api_url.id_api(self.__user.get_xsid())
        )
        id_data = id_res.json()
        self.__user.set_id(id_data["id"])

        info_res = self.__request.do_get(self.__api_url.info_api())
        info_data = info_res.json()
        self.__user.set_name(info_data["name"])
        self.__user.set_avatar(
            self.__request.get_host() + info_data["headimgurl"]
        )

    def login(self) -> dict:
        api = self.__api_url.get_nonce_api()
        nonce_res = self.__request.do_get(
            api,
            {
                "Referer": "http://www.cqooc.com/login",
            },
        )
        data = nonce_res.json()
        cn = test.cnonce()
        hash_str = test.getEncodePwd(
            data["nonce"] + test.getEncodePwd(self.__user.get_pwd()) + cn
        )
        login_res = self.__request.do_post(
            self.__api_url.login_api(
                self.__user.get_username(), hash_str, data["nonce"], cn
            ),
            headers={
                "Referer": "http://www.cqooc.com/login",
            },
        )
        data = login_res.json()
        login_success = data["code"] == 0
        if login_success:
            self.__user.set_xsid(data["xsid"])
            self.__request.set_headers("Cookie", f'xsid={data["xsid"]}')
            self.__process_user_info()
            return Msg().processing("登录成功", 200, data)
        else:
            return Msg().processing("登录失败，可能需要官网登录后重试", 400, data)

    def login_use_sid(self, sid: str):
        self.__user.set_xsid(sid)
        self.__request.set_headers("Cookie", f'xsid={sid}')
        self.__process_user_info()
        return Msg().processing("设置成功", 200)

    def get_user_info(self) -> dict:
        return Msg().processing("登录成功", 200, self.__user.get_info())

    def get_course(self, limit: int = 20) -> dict:
        course_res = self.__request.do_get(
            self.__api_url.course_api(str(self.__user.get_id()), limit),
            headers={
                "Referer": "http://www.cqooc.com/my/learn",
                "Host": "www.cqooc.com",
            },
        )
        course_data = self.__processer.process_course_data(course_res)
        self.__user.set_course_data(course_data.copy())
        return Msg().processing("获取课程成功", 200, self.__user.get_course_data())

    def get_course_lessons(self, course_id: str) -> dict:
        mcs_id_res = self.__request.do_get(
            self.__api_url.mcs_id_api(str(self.__user.get_id()), course_id),
            headers={
                "Referer": "http://www.cqooc.com/my/learn",
                "Host": "www.cqooc.com",
            },
        )
        mcs_id_data = mcs_id_res.json()
        self.__user.set_mcs_id(mcs_id_data["data"][0]["id"])
        lessons_res = self.__request.do_get(
            self.__api_url.lessons_api(course_id),
            headers={
                "Referer": "http://www.cqooc.com/learn"
                + f"/mooc/structure?id={course_id}",
                "host": "www.cqooc.com",
            },
        )
        lessons_status_res = self.__request.do_get(
            self.__api_url.lessons_status_api(
                course_id, self.__user.get_username()
            ),
            headers={
                "Referer": (
                    "http://www.cqooc.com/learn/mooc/progress"
                    + f"?id={course_id}"
                ),
                "host": "www.cqooc.com",
            },
        )
        lessons_data = self.__processer.process_lessons_data(
            self.__user.get_username(), lessons_res, lessons_status_res
        )
        self.__user.set_lessons_data(lessons_data.copy())
        return Msg().processing(
            "获取课程课时成功", 200, self.__user.get_lessons_data()
        )

    def skip_section(self, section_id: str) -> dict:
        section_data = list(
            filter(
                lambda d: d["id"] == section_id,
                self.__user.get_lessons_data()["data"],
            )
        )[0]
        post_data = self.__processer.process_section_data(
            section_data, self.__user.get_mcs_id()
        )
        skip_res = self.__request.do_post(
            self.__api_url.skip_section_api(),
            data=post_data,
            headers={
                "Referer": "http://www.cqooc.com/learn/mooc/structure?id="
                + section_data["courseId"],
                "Host": "www.cqooc.com",
            },
        )
        status_code = skip_res.json()["code"]
        if status_code == 2:
            return Msg().processing("已经跳过该课程", 200)
        elif status_code == 0:
            return Msg().processing("跳过课程成功", 200)
        elif status_code == 1:
            return Msg().processing("非法操作", 400)
        else:
            return Msg().processing("跳过课程失败", 400)

    def get_exam_info(self, course_id: str) -> dict:
        exam_list_res = self.__request.do_get(
            self.__api_url.exam_paper_api(course_id),
            headers={
                "Referer": "http://www.cqooc.com/my/learn",
                "Host": "www.cqooc.com",
            },
        )
        return Msg().processing(
            "获取测验列表成功", 200, exam_list_res.json()
        )

    def get_exam_main_info(self, course_id: str) -> dict:
        exam_list_res = self.__request.do_get(
            self.__api_url.exam_main_api(course_id),
            headers={
                "Referer": f"http://www.cqooc.com/learn/mooc/structure?id={course_id}",
                "Host": "www.cqooc.com",
            },
        )
        return Msg().processing(
            "获取考试列表成功", 200, exam_list_res.json()
        )

    def get_task_info(self, course_id: str) -> dict:
        task_list_res = self.__request.do_get(
            self.__api_url.task_list_api(course_id),
            headers={
                "Referer": "http://www.cqooc.com/my/learn",
                "Host": "www.cqooc.com",
            },
        )
        return Msg().processing(
            "获取作业列表成功", 200, task_list_res.json()
        )

    def get_chapters_info(self, course_id: str) -> dict:
        chapter_list_res = self.__request.do_get(
            self.__api_url.chapters_api(course_id),
            headers={
                "Referer": f"http://www.cqooc.com/learn/mooc/progress?id={course_id}",
                "Host": "www.cqooc.com",
            },
        )
        return Msg().processing(
            "获取章节列表成功", 200, chapter_list_res.json()
        )
