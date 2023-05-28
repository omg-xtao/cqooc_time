# -*- coding: utf-8 -*-

from hackcqooc.api_url import ApiUrl as BaseApiUrl


class ApiUrl(BaseApiUrl):
    def paper_answer_api(self, paper_id: str) -> str:
        return f'https://www.cqooc.com/json/test/result/search?testID={paper_id}&ts={self.__get_ts()}'

    def paper_info_api(self, paper_id: str) -> str:
        return f"https://www.cqooc.com/test/api/paper/get?id={paper_id}&ts={self.__get_ts()}"
