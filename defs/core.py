# -*- coding: utf-8 -*-
from hackcqooc import Core as BaseCore
from hackcqooc.msg import Msg
from defs.api_url import ApiUrl


class Core(BaseCore):
    def __init__(
            self, username: str = "", pwd: str = "", cookie: str = None
    ) -> None:
        super().__init__(username, pwd, cookie)
        self.__api_url = ApiUrl()

    def login_use_sid(self, sid: str):
        self.__user.set_xsid(sid)
        self.__request.set_headers("Cookie", f'xsid={sid}')
        self.__process_user_info()
        return Msg().processing("设置成功", 200)

    def get_paper_answer(self, course_id: str, paper_id: str) -> dict:
        paper_res = self.__request.do_get(
            self.__api_url.paper_answer_api(paper_id),
            headers={
                "Referer": f'https://www.cqooc.com/learn/mooc/testing/do?tid='
                           f'{paper_id}&id={course_id}',
                "Host": "www.cqooc.com",
            },
        )
        return Msg().processing(
            "获取答案成功", 200, paper_res.json()
        )

    def get_paper_info(self, course_id: str, paper_id: str) -> dict:
        paper_res = self.__request.do_get(
            self.__api_url.paper_info_api(paper_id),
            headers={
                "Referer": f'https://www.cqooc.com/learn/mooc/testing/do?tid='
                           f'{paper_id}&id={course_id}',
                "Host": "www.cqooc.com",
            },
        )
        try:
            paper_res.json()
        except Exception as e:
            print(paper_res)
        return Msg().processing(
            "获取成功", 200, paper_res.json()
        )
