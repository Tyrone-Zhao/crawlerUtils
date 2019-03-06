# crawlerUtils
Special gift for spiderman, Make crawler programming easier.

## Installation
```shell
pip install crawlerUtils
```

## Usages

### crawlerUtils.utils.gevent and crawlerUtils.utils.csv
```python
from crawlerUtils.utils import QUEUE, geventIt, writeCsv, getSeleniumSoupHeadLess
import time


url_list = [
    'http://www.mtime.com/top/tv/top100/',
]
url_list += [f"http://www.mtime.com/top/tv/top100/index-{str(x)}.html" for x in range(2, 11)]


def crawler():
    start = time.time()
    content = ["剧名", "导演", "主演", "简介"]
    while not QUEUE.empty():
        url = QUEUE.get_nowait()
        soup = getSeleniumSoupHeadLess(url)
        contents = soup.find("ul", id="asyncRatingRegion").find_all("li")
        for li in contents:
            content_dict = {}
            title = li.find("h2").text
            content_dict[content[0]] = title
            contents = li.find_all("p")
            for i in range(0, min([3, len(contents)])):
                if contents[i].text.strip():
                    if not contents[i].text.strip()[0].isdigit():
                        if contents[i].text[:2] in content:
                            content_dict[contents[i].text[:2]] = contents[i].text
                        else:
                            content_dict[content[3]] = contents[i].text
            writeCsv(dict_params=content_dict, filepath="shiguang.xls", fieldnames=["剧名", "导演", "主演", "简介"])
    end = time.time()
    print(end - start)


def getShiGuang(coroutines_number=5):
    writeCsv(fieldnames=["剧名", "导演", "主演", "简介"], filepath="shiguang.xls")
    geventIt(url_list, coroutines_number, crawler)

```

### crawlerUtils.utils.log
result had be writen into all.log and error.log
```python
from crawlerUtils.utils import setLog

logger = setLog()
logger.debug("这是一条debug信息")
logger.info("这是一条info信息")
logger.warning("这是一条warning信息")
logger.error("这是一条error信息")
logger.critical("这是一条critical信息")
logger.exception("这是一条exception信息")
```

**all.log**
```
2019-03-05 21:51:12,118 - DEBUG - 这是一条debug信息
2019-03-05 21:51:12,119 - INFO - 这是一条info信息
2019-03-05 21:51:12,121 - WARNING - 这是一条warning信息
2019-03-05 21:51:12,122 - ERROR - 这是一条error信息
2019-03-05 21:51:12,123 - CRITICAL - 这是一条critical信息
2019-03-05 21:51:12,124 - ERROR - 这是一条exception信息
NoneType: None
```

**error.log**
```
2019-03-05 21:51:12,122 - ERROR - noUse.py[:7] - 这是一条error信息
2019-03-05 21:51:12,123 - CRITICAL - noUse.py[:8] - 这是一条critical信息
2019-03-05 21:51:12,124 - ERROR - noUse.py[:9] - 这是一条exception信息
NoneType: None
```


### crawlerUtils.utils.selenium
```python
from crawlerUtils.utils import loginNoCaptcha, getMCFunc, Crawler


def loginAndPrintZens():
    ''' 实现登录动作并打印中英文版python之禅 '''
    url = "https://localprod.pandateacher.com/python-manuscript/hello-spiderman/"
    method_params = [
        ("id", "teacher"),
        ("id", "assistant"),
        ("cl", "sub"),
    ]
    username = "酱酱"
    password = "酱酱"

    driver = loginNoCaptcha(url, method_params, username, password)
    zens = getMCFunc(driver, "ids")("p")
    english_zen = Crawler.getBSText(zens[0].text)
    chinese_zen = Crawler.getBSText(zens[1].text)
    print(f"英文版Python之禅：\n{english_zen.text}\n")
    print(f"\n中文版Python之禅：\n{chinese_zen.text}\n")
```

### crawlerUtils.utils.requestAndBeautifulSoup and crawlerUtils.utils.excel
```python
import time
from crawlerUtils.utils import writeExcel, Get


def _getAuthorNames(name):
    """ 获取作者名字 """
    author_headers = {
        "referer": "https://www.zhihu.com/search?type=content&q=python"
    }

    author_params = {
        "type": "content",
        "q": name,
    }

    author_url = "https://www.zhihu.com/search"

    author_soup = Get(author_url, headers=author_headers, params=author_params).soup()
    author_name_json = Get.beautifulJson(
        author_soup.find("script", id="js-initialData").text
    )
    author_names = list(author_name_json['initialState']['entities']['users'])
    return author_names


def _getOneAuthorsArticles(author, wb):
    """ 爬取一个作者的所有文章 """
    ws = writeExcel(workbook=wb, sheetname=f"{author}Articles")
    writeExcel(0, 0, label="文章名", worksheet=ws)
    writeExcel(0, 1, label="文章链接", worksheet=ws)
    writeExcel(0, 2, label="文章摘要", worksheet=ws)

    headers = {
        "referer": f"https://www.zhihu.com/people/{author}/posts"
    }

    # 文章计数
    article_nums = 0
    offset = 0
    page_num = 1

    while True:
        articles_params = {
            "include": "data[*].comment_count,suggest_edit,is_normal,thumbnail_extra_info,thumbnail,can_comment,comment_permission,admin_closed_comment,content,voteup_count,created,updated,upvoted_followees,voting,review_info,is_labeled,label_info;data[*].author.badge[?(type=best_answerer)].topics",
            "offset": str(offset),
            "limit": "20",
            "sort_by": "created",
        }

        articles_url = f"https://www.zhihu.com/api/v4/members/{author}/articles"

        articles_res_json = Get(articles_url, headers=headers, params=articles_params).json()

        articles = articles_res_json["data"]
        for article in articles:
            article_nums += 1
            article_title = article["title"]
            article_url = article["url"]
            article_excerpt = article["excerpt"]
            print(article_title)
            writeExcel(article_nums, 0, label=article_title, worksheet=ws)
            writeExcel(article_nums, 1, label=article_url, worksheet=ws)
            writeExcel(article_nums, 2, label=article_excerpt, worksheet=ws)

        offset += 20
        headers["referer"] = f"https://www.zhihu.com/people/{author}/posts?page={page_num}"
        page_num += 1

        articles_is_end = articles_res_json["paging"]["is_end"]
        if articles_is_end:
            break

        # # 爬两页就结束
        # if page_num > 2:
        #     break


def getZhiHuArticle():
    """ 获取一个知乎作者的所有文章名称、链接、及摘要，并存到Excel表里 """
    # Excel
    wb = writeExcel(encoding='ascii')

    # 用户输入知乎作者名
    name = input("请输入作者的名字：")
    # 获取作者url_name
    authors = _getAuthorNames(name)
    if not authors:
        authors = _getAuthorNames(name)
    # 获取作者的所有文章
    for author in authors:
        time.sleep(1)
        _getOneAuthorsArticles(author, wb)

    wb.save(f"zhihu{name}.xls")

```

### crawlerUtils.utils.urllib and crawlerUtils.utils.mail and crawlerUtils.utils.schedule
```python
from crawlerUtils.utils import (
    urllibOpenJson,
    urlencode,
    urllibOpenSoup,
    sendMailInput,
    sendMail,
    regularFuncEveryDayTime,
)
import re


def queryChineseWeather(city_name="广州"):
    ''' 在中国天气网查询天气 '''
    while True:
        if not city_name:
            city_name = input("请问要查询哪里的天气：")
        city_url = f"http://toy1.weather.com.cn/search?cityname={urlencode(city_name)}"
        city_json = urllibOpenJson(city_url)

        if city_json:
            if city_json[0].get("ref"):
                city_string = city_json[0]["ref"]
                city_code = re.findall("\d+", city_string)[0]
        else:
            print("城市地址输入有误，请重新输入！")
            city_name = ""
            continue

        weather_url = f"http://www.weather.com.cn/weather1d/{city_code}.shtml"
        weather_soup = urllibOpenSoup(weather_url)
        weather = weather_soup.find(
            "input", id="hidden_title").get("value").split()

        return weather


def sendCityWeatherEveryDay(city="北京"):
    ''' 每天定时发送天气信息到指定邮箱 '''
    recipients, account, password, subj, text = sendMailInput()
    weather = queryChineseWeather(city)
    text = " ".join(weather)
    daytime = input("请问每天的几点发送邮件？格式'18:30'，不包含单引号 ：")

    regularFuncEveryDayTime(sendMail, daytime, recipients, account,
                            password, subj, text)

```

### More...

## Examples

所有例子的源代码都在crawlerUtils/examples里
```python
import crawlerUtils.examples

print(crawlerUtils.examples.__all__)
```

包括：
- 获取QQ音乐某个歌手的歌曲信息和评论
```python
from crawlerUtils.examples import *


getQQSinger()
```

- 获取知乎某个作者的所有文章
```python
from crawlerUtils.examples import *


getZhiHuArticle()
```

- 登陆饿了么并获取附近餐厅, 使用了向量空间进行验证码识别
```python
from crawlerUtils.examples import *


getElemeDishes()
```

- 获取豆瓣top250电影信息, 使用requests+正则表达式
```python
from crawlerUtils.examples import *


getDoubanTop250UseRegexExpression()
```

- 打印Python之禅, Selenium实现登录并用BeatifulSoup解析文本
```python
from crawlerUtils.examples import *


loginAndPrintZens()
```

- 每天定时发送天气信息邮件, 使用了urlopen等函数
```python
from crawlerUtils.examples import *


sendCityWeatherEveryDay()
```

- 爬取时光网top100电影信息，使用了协程gevent库和写csv函数
```python
from gevent import monkey
monkey.patch_all()
from crawlerUtils.examples import getShiGuang


getShiGuang()
```


## 更新记录
- Future
更新内容: utils全部文件改成基础类，由utils/utils.py里的Crawler继承; 集成Requests-html，增加多进程模块、分布式等; 欢迎提交Pull Request。

- V1.6.0
更新内容: 集成gevent，支持协程，增加examples里的shiguang.py；集成csv、math;重构requestsAndBeautifulSoup.py及对应example，采用面向对象方式编写。

- V1.5.2
更新内容: 增加utils.log模块，加入moviedownload.py 多线程Windows64位版

- V1.5.0 
更新内容: 集成schedule库函数, 重构utils代码

- V1.4.2 
更新内容: 增加每日定时发送天气的example及定时发送邮件等函数

- V1.4.1 
更新内容: 封装了一些BeautifulSoup和Selenium函数、增加打印python之禅的例子