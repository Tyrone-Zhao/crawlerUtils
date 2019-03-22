from requests_html import HTML, HTMLSession, AsyncHTMLSession
import json
import requests
from bs4 import BeautifulSoup
from .selenium import Selenium
from .csv import Csv
from .gevent import Gevent
from .geohash import Geohash
from .time import Time
from .html import Html
from .excel import Excel
from .decorator import Decorator
from .mail import Mail
from .log import Log
from .schedule import Schedule
from .urllib import Urllib
from .captcha import Base64, Captcha

__all__ = [
    "Crawler", "Get", "Post"
]


class Crawler(Selenium, Csv, Gevent, Geohash, Time, Html, Excel, Decorator,
              Mail, Log, Schedule, Urllib, Base64, Captcha):
    session = requests.session()
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    }
    session.headers = headers
    html_session = HTMLSession()
    async_session = AsyncHTMLSession()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def headersAdd(self, value):
        ''' 添加headers条目 '''
        self.headers.update(value)
        self.session.headers = self.headers

    @classmethod
    def headersSet(self, value):
        ''' 设置session.headers '''
        self.headers = value
        self.session.headers = self.headers

    @classmethod
    def cookiesStringToDict(cls, cookie):
        """从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies"""
        cookies = dict([l.split("=", 1) for l in cookie.split(";")])
        return cookies

    @classmethod
    def cookiesSetFromDict(cls, cookies_dict):
        ''' 从字典设置Session的cookies '''
        cls.session.cookies = requests.utils.cookiejar_from_dict(
            cookies_dict)

    @classmethod
    def cookiesRead(cls, filepath="", cookies=""):
        """ 从txt文件读取cookies """
        # 如果能读取到cookies文件，执行以下代码，跳过except的代码，不用登录就能发表评论。
        cookies_dict = {}
        if cookies:
            cookies_dict = cls.cookiesStringToDict(cookies)
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
            cls.cookiesSetFromDict(cookies_dict)
            # 获取cookies：就是调用requests对象（session）的cookies属性。
            cookies_txt.close()
        except FileNotFoundError:
            pass

    @classmethod
    def htmlParser(self, doc):
        ''' 分析一段HTML文本, 返回requests-html对象 '''
        html = HTML(html=doc)
        return html

    @classmethod
    def asyncRun(self, func, number, *args, **kwargs):
        ''' 运行异步定义函数 '''
        func_list = [func for i in range(number)]
        result = self.async_session.run(*func_list)
        return result


class Get(Crawler):
    def __init__(self, url="", headers={}, params={}, data={}, jsons={},
                 parser="html.parser", encoding="utf-8", **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.add_headers = headers
        self.params = params
        self.data = data
        self.jsons = jsons
        self.parser = parser
        self.encoding = encoding
        self.kwargs = kwargs

    def __str__(self):
        if self.url:
            return f"<Response [{str(self.getGet(self.session).status_code)}]>"
        else:
            return self.__repr__()

    @property
    def driver(self):
        ''' 返回driver '''
        driver = self.getDriver()
        driver.get(self.url)
        return driver

    @property
    def hdriver(self):
        ''' 返回headlessDriver '''
        driver = self.getDriverHeadLess()
        driver.get(self.url)
        return driver

    @property
    def text(self):
        ''' 返回response.text '''
        response = self.getGet(self.session)
        return response.text

    @property
    def rtext(self):
        ''' 返回render()后的response.text '''
        rtext = self.getSeleniumText(self.url)
        return rtext

    @property
    def rhtext(self):
        ''' 无头模式返回render()后的response.text '''
        rhtext = getSeleniumTextHeadLess(self.url)
        return rhtext

    @property
    def json(self):
        ''' 返回json.loads()字典 '''
        return self.beautifulJson(self.text)

    @property
    def rjson(self):
        ''' 返回render()后的json.loads(response.text) '''
        rjson = self.getSeleniumJson(self.url)
        return rjson

    @property
    def rhjson(self):
        ''' 无头模式返回render()后的json.loads(response.text) '''
        rhjson = getSeleniumJsonHeadLess(self.url)
        return rhjson

    @property
    def soup(self):
        ''' 返回BeautifulSoup对象 '''
        return self.beautifulSoup(self.text, self.parser)

    @property
    def rsoup(self):
        ''' 返回render()后的BeautifulSoup对象 '''
        rsoup = getSeleniumSoup(self.url)
        return rsoup

    @property
    def rhsoup(self):
        ''' 无头模式返回render()后的BeautifulSoup对象 '''
        rhsoup = getSeleniumSoupHeadLess(self.url)
        return rhsoup

    def getGet(self, session):
        ''' 返回response对象 '''
        if self.jsons:
            res = session.get(
                self.url, headers=self.add_headers, json=self.jsons, **self.kwargs
            )
        else:
            res = session.get(
                self.url, headers=self.add_headers, params=self.params, data=self.data, **self.kwargs
            )
        res.encoding = self.encoding
        return res

    @property
    def html(self):
        ''' 返回requests-html的HTMLSession对象 '''
        return self.getGet(self.html_session).html

    @property
    def rhtml(self):
        ''' 返回render()后的requests-html的HTMLSession对象 '''
        r = self.getGet(self.html_session).html
        r.render()
        return r

    @property
    async def ahtml(self):
        ''' 返回async get(url).html '''
        r = await self.async_session.get(self.url)
        return r.html

    @property
    async def atext(self):
        ''' 返回async Get(url).text '''
        r = await self.async_session.get(self.url)
        text = r.content.decode(self.encoding)
        return text

    @property
    async def ajson(self):
        ''' 返回async Get(url).json '''
        r = await self.async_session.post(self.url)
        text = self.beautifulJson(r.content.decode(self.encoding))
        return text

    @property
    async def asoup(self):
        ''' 返回async Get(url).soup '''
        r = await self.async_session.get(self.url)
        text = r.content.decode(self.encoding)
        return BeautifulSoup(text, self.parser)

    @property
    async def arhtml(self):
        ''' 返回arender()后的async Get(url).html'''
        r = await self.async_session.get(self.url)
        await r.html.arender()
        return r.html

    @property
    async def artext(self):
        ''' 返回arender()后的async Get(url).text '''
        r = await self.async_session.get(self.url)
        await r.html.arender()
        text = r.content.decode(self.encoding)
        return text

    @property
    async def arjson(self):
        ''' 返回arender()后的async Get(url).json '''
        r = await self.async_session.post(self.url)
        await r.html.arender()
        text = self.beautifulJson(r.content.decode(self.encoding))
        return text

    @property
    async def arsoup(self):
        ''' 返回arender()后的async Get(url).soup '''
        r = await self.async_session.get(self.url)
        await r.html.arender()
        text = r.content.decode(self.encoding)
        return BeautifulSoup(text, self.parser)

    @property
    async def masoup(self, url):
        r = self.getGet(self.session)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup


class Post(Crawler):
    def __init__(self, url="", headers={}, params={}, data={}, jsons={},
                 parser="html.parser", encoding="utf-8", **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.add_headers = headers
        self.params = params
        self.data = data
        self.jsons = jsons
        self.parser = parser
        self.encoding = encoding
        self.kwargs = kwargs

    def __str__(self):
        if self.url:
            return f"<Response [{str(self.getPost(self.session).status_code)}]>"
        else:
            return self.__repr__()

    @property
    def driver(self):
        ''' 返回driver '''
        driver = self.getDriver()
        driver.get(self.url)
        return driver

    @property
    def hdriver(self):
        ''' 返回headlessDriver '''
        driver = self.getDriverHeadLess()
        driver.get(self.url)
        return driver

    @property
    def text(self):
        ''' 返回response.text '''
        response = self.getPost(self.session)
        return response.text

    @property
    def rtext(self):
        ''' 返回render()后的response.text '''
        rtext = self.getSeleniumText(self.url)
        return rtext

    @property
    def rhtext(self):
        ''' 无头模式返回render()后的response.text '''
        rhtext = getSeleniumTextHeadLess(self.url)
        return rhtext

    @property
    def json(self):
        ''' 返回json.loads()字典 '''
        return self.beautifulJson(self.text)

    @property
    def rjson(self):
        ''' 返回render()后的json.loads(response.text) '''
        rjson = self.getSeleniumJson(self.url)
        return rjson

    @property
    def rhjson(self):
        ''' 无头模式返回render()后的json.loads(response.text) '''
        rhjson = getSeleniumJsonHeadLess(self.url)
        return rhjson

    @property
    def soup(self):
        ''' 返回BeautifulSoup对象 '''
        return self.beautifulSoup(self.text, self.parser)

    @property
    def rsoup(self):
        ''' 返回render()后的BeautifulSoup对象 '''
        rsoup = getSeleniumSoup(self.url)
        return rsoup

    @property
    def rhsoup(self):
        ''' 无头模式返回render()后的BeautifulSoup对象 '''
        rhsoup = getSeleniumSoupHeadLess(self.url)
        return rhsoup

    def getPost(self, session):
        ''' 返回response对象 '''
        if self.jsons:
            res = session.post(
                self.url, headers=self.add_headers, json=self.jsons, **self.kwargs
            )
        else:
            res = session.post(
                self.url, headers=self.add_headers, params=self.params, data=self.data, **self.kwargs
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

    @property
    def html(self):
        ''' 返回requests-html的HTMLSession对象 '''
        return self.getPost(self.html_session).html

    @property
    def rhtml(self):
        ''' 返回render()后的requests-html的HTMLSession对象 '''
        r = self.getPost(self.html_session).html
        r.render()
        return r

    @property
    async def ahtml(self):
        ''' 返回async post(url).html '''
        r = await self.async_session.post(self.url)
        return r.html

    @property
    async def atext(self):
        ''' 返回async Post(url).text '''
        r = await self.async_session.post(self.url)
        text = r.content.decode(self.encoding)
        return text

    @property
    async def ajson(self):
        ''' 返回async Post(url).json '''
        r = await self.async_session.post(self.url)
        text = self.beautifulJson(r.content.decode(self.encoding))
        return text

    @property
    async def asoup(self):
        ''' 返回async Post(url).soup '''
        r = await self.async_session.post(self.url)
        text = r.content.decode(self.encoding)
        return BeautifulSoup(text, self.parser)

    @property
    async def arhtml(self):
        ''' 返回arender()后的async Post(url).html'''
        r = await self.async_session.post(self.url)
        await r.html.arender()
        return r.html

    @property
    async def artext(self):
        ''' 返回arender()后的async Post(url).text '''
        r = await self.async_session.post(self.url)
        await r.html.arender()
        text = r.content.decode(self.encoding)
        return text

    @property
    async def arjson(self):
        ''' 返回arender()后的async Post(url).json '''
        r = await self.async_session.post(self.url)
        await r.html.arender()
        text = self.beautifulJson(r.content.decode(self.encoding))
        return text

    @property
    async def arsoup(self):
        ''' 返回arender()后的async Post(url).soup '''
        r = await self.async_session.post(self.url)
        await r.html.arender()
        text = r.content.decode(self.encoding)
        return BeautifulSoup(text, self.parser)
