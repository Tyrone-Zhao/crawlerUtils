import requests
import json
from bs4 import BeautifulSoup


__all__ = [
    "Crawler", "Get", "Post"
]


class Crawler():
    session = requests.session()
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    }
    session.headers = headers

    @classmethod
    def addHeaders(self, value):
        ''' 添加headers条目 '''
        self.headers.update(value)
        self.session.headers = self.headers

    @classmethod
    def setHeaders(self, value):
        ''' 设置session.headers '''
        self.headers = value
        self.session.headers = self.headers

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
    def getBSText(self, text, parser="html.parser"):
        """ 返回BeautifulSoup(text, "html.parser") """
        return BeautifulSoup(text, parser)

    @classmethod
    def stringCookiesToDict(cls, cookie):
        """从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies"""
        cookies = dict([l.split("=", 1) for l in cookie.split(";")])
        return cookies

    @classmethod
    def setCookiesFromDict(cls, cookies_dict):
        ''' 从字典设置Session的cookies '''
        cls.session.cookies = requests.utils.cookiejar_from_dict(
            cookies_dict)

    @classmethod
    def readCookies(cls, filepath="", cookies=""):
        print(filepath)
        """ 从txt文件读取cookies """
        # 如果能读取到cookies文件，执行以下代码，跳过except的代码，不用登录就能发表评论。
        cookies_dict = {}
        if cookies:
            cookies_dict = cls.stringCookiesToDict(cookies)
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            cls.session.cookies = cookies
        if not filepath:
            filepath = 'crawlerUtilsCookies.txt'
        try:
            cookies_txt = open(filepath, 'r')
            # 以reader读取模式，打开名为cookies.txt的文件。
            cookies_dict = cookies_txt.read()
            if cookies_dict:
                cookies_dict = json.loads(cookies_dict)
            # 调用json模块的loads函数，把字符串转成字典。
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            # 把转成字典的cookies再转成cookies本来的格式。
            cls.session.cookies = cookies
            # 获取cookies：就是调用requests对象（session）的cookies属性。
            cookies_txt.close()
        except FileNotFoundError:
            pass


class Get(Crawler):
    def __init__(self, url, headers={}, params={}, data={}, jsons={}, parser="html.parser", encoding="utf-8", *args, **kwargs):
        super().__init__()
        self.url = url
        self.headers = headers
        self.params = params
        self.data = data
        self.jsons = jsons
        self.parser = parser
        self.encoding = encoding
        self.args = args
        self.kwargs = kwargs

        self.response = self.getGet()
        self.text = self.response.text

    def json(self):
        ''' 返回json.loads()字典 '''
        return self.beautifulJson(self.text)

    def soup(self):
        ''' 返回BeautifulSoup对象 '''
        return self.getBSText(self.text, self.parser)

    def getGet(self):
        ''' 返回response对象 '''
        if self.jsons:
            res = self.session.get(
                self.url, headers=self.headers, json=self.jsons, *self.args, **self.kwargs
            )
        else:
            res = self.session.get(
                self.url, headers=self.headers, params=self.params, data=self.data, *self.args, **self.kwargs
            )
        res.encoding = self.encoding
        return res


class Post(Crawler):
    def __init__(self, url, headers={}, params={}, data={}, jsons={}, parser="html.parser", encoding="utf-8", *args, **kwargs):
        super().__init__()
        self.url = url
        self.headers = headers
        self.params = params
        self.data = data
        self.jsons = jsons
        self.parser = parser
        self.encoding = encoding
        self.args = args
        self.kwargs = kwargs

        self.response = self.getPost()
        self.text = self.response.text

    def json(self):
        ''' 返回json.loads()字典 '''
        return self.beautifulJson(self.text)

    def soup(self):
        ''' 返回BeautifulSoup对象 '''
        return self.getBSText(self.text, self.parser)

    def getPost(self):
        ''' 返回response对象 '''
        if self.jsons:
            res = self.session.post(
                self.url, headers=self.headers, json=self.jsons, *self.args, **self.kwargs
            )
        else:
            res = self.session.post(
                self.url, headers=self.headers, params=self.params, data=self.data, *self.args, **self.kwargs
            )
        res.encoding = self.encoding
        return res

    def cookiesToFile(self, filepath='crawlerUtilsCookies.txt'):
        """ 登陆获取cookies """
        cookies_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
        # 把cookies转化成字典。
        cookies_str = json.dumps(cookies_dict)
        # 调用json模块的dump函数，把cookies从字典再转成字符串。
        f = open(filepath, 'w')
        # 创建名为cookies.txt的文件，以写入模式写入内容
        f.write(cookies_str)
        # 把已经转成字符串的cookies写入文件
        f.close()
        # 关闭文件
