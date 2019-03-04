import requests
import json
from bs4 import BeautifulSoup


__all__ = [
    "extract_cookies", "setSessionCookies", "beautifulJson", "getBSText",
    "readCookies", "getCookies", "getPostJson", "getGetJson", "getPostText",
    "getGetText", "getPostSoup", "getGetSoup", "SESSION", "HEADERS",

]


SESSION = requests.session()
HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
}


def extract_cookies(cookie):
    """从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies"""
    cookies = dict([l.split("=", 1) for l in cookie.split(";")])
    return cookies


def setSessionCookies(session, cookies_dict):
    ''' 从字典设置Session的cookies '''
    session.cookies = requests.utils.cookiejar_from_dict(cookies_dict)


def beautifulJson(text):
    ''' 处理异常格式Json '''
    start_temp = text.find("{")
    end_temp = text.rfind("}") + 1
    start = text.find("[")
    end = text.rfind("]") + 1
    if start < start_temp and start != -1:
        text_json = text[start:end]
    elif start > start_temp and start_temp != -1:
        text_json = text[start_temp:end_temp]
    else:
        text_json = ""
    if text_json:
        return json.loads(text_json)
    else:
        return ""


def getBSText(text, parser="html.parser"):
    """ 返回BeautifulSoup(text, "html.parser") """
    return BeautifulSoup(text, parser)


def readCookies(session, filepath="", cookies=""):
    """ 从txt文件读取cookies """
    # 如果能读取到cookies文件，执行以下代码，跳过except的代码，不用登录就能发表评论。
    cookies_dict = {}
    if cookies:
        cookies_dict = extract_cookies(cookies)
        cookies = requests.utils.cookiejar_from_dict(cookies_dict)
        session.cookies = cookies
    elif not filepath:
        filepath = 'crawlerUtilsCookies.txt'
    elif filepath:
        filepath = filepath
        try:
            cookies_txt = open(filepath, 'r')
            # 以reader读取模式，打开名为cookies.txt的文件。
            cookies_dict = cookies_txt.read()
            if cookies_dict:
                cookies_dict = json.loads(cookies_dict)
            # 调用json模块的loads函数，把字符串转成字典。
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            # 把转成字典的cookies再转成cookies本来的格式。
            session.cookies = cookies
            # 获取cookies：就是调用requests对象（session）的cookies属性。
            cookies_txt.close()
        except FileNotFoundError:
            pass


def getCookies(session, url, headers, data={}, params={}, jsons={}, filepath='crawlerUtilsCookies.txt'):
    """ 登陆获取cookies """
    session.post(url, headers=headers, data=data, params=params, json=jsons)
    # 在会话下，用post发起登录请求。
    cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
    # 把cookies转化成字典。
    cookies_str = json.dumps(cookies_dict)
    # 调用json模块的dump函数，把cookies从字典再转成字符串。
    f = open(filepath, 'w')
    # 创建名为cookies.txt的文件，以写入模式写入内容
    f.write(cookies_str)
    # 把已经转成字符串的cookies写入文件
    f.close()
    # 关闭文件


def getPostJson(session, url, headers={}, params={}, data={}, jsons={}, encoding="utf-8"):
    """ 获取Post请求的response.json() """
    if jsons:
        res = session.post(
            url, headers=headers, json=jsons
        )
    else:
        res = session.post(
            url, headers=headers, params=params, data=data
        )
    res.encoding = encoding
    res_json = beautifulJson(res.text)
    return res_json


def getGetJson(session, url, headers={}, params={}, data={}, jsons={}, encoding="utf-8"):
    """ 获取Get请求的response.json() """
    if jsons:
        res = session.get(
            url, headers=headers, json=jsons
        )
    else:
        res = session.get(
            url, headers=headers, params=params, data=data
        )
    res.encoding = encoding
    res_json = beautifulJson(res.text)

    return res_json


def getPostText(session, url, headers={}, params={}, data={}, jsons={}, encoding="utf-8"):
    """ 获取Post请求的response.text """
    if jsons:
        res = session.post(
            url, headers=headers, json=jsons
        )
    else:
        res = session.post(
            url, headers=headers, params=params, data=data
        )
    res.encoding = encoding
    return res.text


def getGetText(session, url, headers={}, params={}, data={}, jsons={}, encoding="utf-8"):
    """ 获取Get请求的response.text """
    if jsons:
        res = session.get(
            url, headers=headers, json=jsons
        )
    else:
        res = session.get(
            url, headers=headers, params=params, data=data
        )
    res.encoding = encoding
    return res.text


def getPostSoup(session, url, headers={}, params={}, data={}, jsons={}, parser="html.parser", encoding="utf-8"):
    """ 获取Post请求的BeautifulSoup实例 """
    if jsons:
        res = session.post(
            url, headers=headers, json=jsons
        )
    else:
        res = session.post(
            url, headers=headers, params=params, data=data
        )
    res.encoding = encoding
    soup = getBSText(res.text, parser)
    return soup


def getGetSoup(session, url, headers={}, params={}, data={}, jsons={}, parser="html.parser", encoding="utf-8"):
    """ 获取Get请求的BeautifulSoup实例 """
    if jsons:
        res = session.get(
            url, headers=headers, json=jsons
        )
    else:
        res = session.get(
            url, headers=headers, params=params, data=data
        )
    res.encoding = encoding
    soup = getBSText(res.text, parser)
    return soup
