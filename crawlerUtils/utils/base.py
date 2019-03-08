import json
from bs4 import BeautifulSoup


__all__ = ["BaseCrawler"]


class BaseCrawler():

    @classmethod
    def beautifulJson(self, text):
        ''' 处理异常格式Json '''
        start_temp = text.find("{")
        end_temp = text.rfind("}") + 1
        start = text.find("[")
        end = text.rfind("]") + 1
        if start < start_temp and start != -1:
            text_json = text[start:end]
        elif start > start_temp and start_temp != -1:
            text_json = text[start_temp:end_temp]
        elif start < start_temp and start_temp != -1:
            text_json = text[start_temp:end_temp]
        elif start > start_temp and start != -1:
            text_json = text[start:end]
        if text_json:
            return json.loads(text_json)
        else:
            return ""

    @classmethod
    def beautifulSoup(self, text, parser="html.parser"):
        """ 返回BeautifulSoup(text, "html.parser") """
        return BeautifulSoup(text, parser)