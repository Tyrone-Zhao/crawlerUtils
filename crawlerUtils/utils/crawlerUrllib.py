from urllib.request import quote, unquote, urlopen
from urllib import parse
from .crawlerBase import BaseCrawler

__all__ = [
    "Urllib"
]


class Urllib(BaseCrawler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def urljoin(cls, url1, url2):
        """ 拼接url """
        return parse.urljoin(url1, url2)

    @classmethod
    def urlencode(self, string):
        ''' 返回中文的urlencode()结果 '''
        return quote(string)

    @classmethod
    def urldecode(self, string):
        ''' 返回urldecode()的中文结果 '''
        return unquote(string)

    @classmethod
    def urllibOpen(self, url, data=None):
        ''' 通过urllib.request.urlopen访问url，返回response对象
            selenium当前版本在访问某些响应头没有指定编码的url时，driver.page_source会返回乱码
        '''
        return urlopen(url, data)

    @classmethod
    def urllibOpenText(self, url, data=None, encoding="utf-8"):
        ''' 返回response.read().decode("utf-8") '''
        return self.urllibOpen(url, data).read().decode(encoding)

    @classmethod
    def urllibOpenJson(self, url, data=None, encoding="utf-8"):
        ''' 返回urllibOpenText及一些处理后的json '''
        text = self.urllibOpenText(url, data, encoding)
        text_json = self.beautifulJson(text)

        return text_json

    @classmethod
    def urllibOpenSoup(self, url, data=None, encoding="utf-8", parser="html.parser"):
        ''' 返回BeautifulSoup(
                urllibOpenText(url, data=None, encoding="utf-8"), "html.parser"
            ) 
        '''
        return self.beautifulSoup(
            self.urllibOpenText(url, data=None, encoding=encoding), parser)
