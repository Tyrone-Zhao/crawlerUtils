# crawlerUtils
Special gift for spiderman, make spinning a web easier.

## Installation
```shell
pip install --user --upgrade crawlerUtils
```

## Usages
**crawlerUtils.utils.crawler contains the follow methods:**

Crawler is the BaseClass, which is inherited by Get Class and Post Class in utils/crawler.py.
the other Classes in utils is inherited by Crawler.
Also some of the Classes maybe inherite BaseCrawler Class in utils/base.py

- Crawler.headersAdd(value) -- add the requests headers
- Crawler.headersSet(value) -- reset the requests headers
- Crawler.beautifulJson(text) -- deal the text to json
- Crawler.beautifulSoup(text, parser="html.parser") -- return BeautifulSoup object
- Crawler.cookiesStringToDict(cookie) -- get cookies to dict from type string cookies
- Crawler.cookiesSetFromDict(cookies_dict) -- set session cookies from dict
- Crawler.cookiesRead(filepath="", cookies="") -- set session cookies from txt
- Crawler.htmlParser(doc) -- read string object and return requests-html HTML object
- Crawler.asyncRun(func, number, *args, **kwargs) -- run async requests-html Aysnc func

- Get(url).text == requests.get(url).text
- Get(url).rtext ~= webdriver.Chrome().get(url).page_source
- Get(url).rhtext ~= webdriver.Chrome().headless.get(url).page_source
- Get(url).json ~= json.loads(requests.get(url).text)
- Get(url).rjson ~= json.loads(webdriver.Chrome().get(url).page_source)
- Get(url).rhjson ~= json.loads(webdriver.Chrome().headless.get(url).page_source)
- Get(url).soup ~= BeautifulSoup(requests.get(url).text, "html.parser")
- Get(url).rsoup ~= BeautifulSoup(webdriver.Chrome().get(url).page_source, "html.parser")
- Get(url).rhsoup ~= BeautifulSoup(webdriver.Chrome().headless.get(url).page_source, "html.parser")
- Get(url).html == request-html.get(url).html
- Get(url).rhtml ~= request-html.get(url).html.render().html
- Get(url).ahtml ~= await request-html.get(url).html
- Get(url).atext ~= await request-html.get(url).text
- Get(url).ajson ~= await json.loads(request-html.get(url).text)
- Get(url).asoup ~= await BeautifulSoup(request-html.get(url).text, "html.parser")
- Get(url).arhtml ~= await request-html.get(url).html.arender()
- Get(url).artext ~= await request-html.get(url).text.arender()
- Get(url).arjson ~= await json.loads(request-html.get(url).text.arender())
- Get(url).arsoup ~= await BeautifulSoup(request-html.get(url).text.arender(), "html.parser")
- Post(url).text == requests.post(url).text
- Post(url).rtext ~= webdriver.Chrome().get(url).page_source
- ...
- Post.cookiesToFile() == login in and save cookies locally

## What else can this Crawler do?
```python
from crawlerUtils import Crawler


print(dir(Crawler))
```

## Coding Examples

### Get(url).html
```python
from crawlerUtils import Get

url = "https://book.douban.com/top250?start=0"

soup = Get(url).html
trs = soup.find("tr.item")
for tr in trs:
    book_name = tr.find("td")[1].find("a", first=True).text
    author = tr.find("p.pl", first=True).text
    rating = tr.find("span.rating_nums", first=True).text
    introduction = tr.find("span.inq", first=True).text
    print("书名：{0}\n作者：{1}\n评分：{2}\n简介：{3}\n".format(
        book_name, author, rating, introduction))
```


### crawlerUtils.utils.requests and crawlerUtils.utils.csv
```python
from crawlerUtils import Get
import time


__all__ = ["getShiGuang"]


url_list = [
    'http://www.mtime.com/top/tv/top100/',
]
url_list += [f"http://www.mtime.com/top/tv/top100/index-{str(x)}.html" for x in range(2, 11)]


async def crawler():
    content = ["剧名", "导演", "主演", "简介"]
    while url_list:
        url = url_list.pop(0)
        rhtml = await Get(url).arhtml
        contents = rhtml.find("#asyncRatingRegion", first=True).find("li")
        for li in contents:
            content_dict = {}
            title = li.find("h2", first=True).text
            content_dict[content[0]] = title
            contents = li.find("p")
            for i in range(0, min([3, len(contents)])):
                if contents[i].text.strip():
                    if not contents[i].text.strip()[0].isdigit():
                        if contents[i].text[:2] in content:
                            content_dict[contents[i].text[:2]] = contents[i].text
                        else:
                            content_dict[content[3]] = contents[i].text
            Get.csvWrite(fieldnames=["剧名", "导演", "主演", "简介"], filepath="shiguang.csv", dict_params=content_dict)
    return url


def runShiGuang(coroutine_number=5):
    ''' 使用协程爬取时光电影网top100电影信息 '''
    start = time.time()
    Get.csvWrite(fieldnames=["剧名", "导演", "主演", "简介"], filepath="shiguang.csv")
    results = Get.asyncRun(crawler, coroutine_number)
    for result in results:
        print(result)
    end = time.time()
    print(end - start)
```

### crawlerUtils.utils.gevent and crawlerUtils.utils.csv
```python
from gevent import monkey
monkey.patch_all()
from crawlerUtils import Get


url_list = [Get.queue.put_nowait(
    f"http://www.boohee.com/food/group/{str(i)}?page={str(j)}") for i in range(1, 11) for j in range(1, 11)]
url_list2 = [Get.queue.put_nowait(
    f"http://www.boohee.com/food/view_menu?page={str(i)}") for i in range(1, 11)]
url_list += url_list2


def crawler():
    while not Get.queue.empty():
        url = Get.queue.get_nowait()
        res_soup = Get(url).soup
        foods = res_soup.find_all('li', class_='item clearfix')
        for i in range(0, len(foods)):
            food_name = foods[i].find_all('a')[1]['title']
            print(food_name)
            food_url = 'http://www.boohee.com' + foods[i].find_all('a')[1]['href']
            food_calorie = foods[i].find('p').text
            Get.csvWrite(filepath="薄荷.csv", row=[food_name, food_url, food_calorie])


def runBoheGevent():
    Get.csvWrite(filepath="薄荷.csv")
    Get.csvWrite(filepath="薄荷.csv", row=["食物名称", "食物链接", "食物热量"])
    Get.geventRun(crawler, 5)
```

### crawlerUtils.utils.log
result will be writen into all.log and error.log
```python
from crawlerUtils import Crawler

logger = Crawler.logSet()
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
from crawlerUtils import Get


def runLoginAndPrintZens():
    ''' 实现登录动作并打印中英文版python之禅 '''
    url = "https://localprod.pandateacher.com/python-manuscript/hello-spiderman/"
    method_params = [
        ("id", "teacher"),
        ("id", "assistant"),
        ("cl", "sub"),
    ]
    username = "酱酱"
    password = "酱酱"

    driver = Get.loginNoCaptcha(url, method_params, username, password)
    zens = Get.locateElement(driver, "ids")("p")
    english_zen = Get.beautifulSoup(zens[0].text)
    chinese_zen = Get.beautifulSoup(zens[1].text)
    print(f"英文版Python之禅：\n{english_zen.text}\n")
    print(f"\n中文版Python之禅：\n{chinese_zen.text}\n")
```

### crawlerUtils.utils.crawler and crawlerUtils.utils.excel
```python
import time
from crawlerUtils import Get

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

    author_soup = Get(author_url, headers=author_headers, params=author_params).soup
    author_name_json = Get.beautifulJson(
        author_soup.find("script", id="js-initialData").text
    )
    author_names = list(author_name_json['initialState']['entities']['users'])
    return author_names


def _getOneAuthorsArticles(author, wb):
    """ 爬取一个作者的所有文章 """
    ws = Get.excelWrite(workbook=wb, sheetname=f"{author}Articles")
    Get.excelWrite(0, 0, label="文章名", worksheet=ws)
    Get.excelWrite(0, 1, label="文章链接", worksheet=ws)
    Get.excelWrite(0, 2, label="文章摘要", worksheet=ws)

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

        articles_res_json = Get(articles_url, headers=headers, params=articles_params).json

        articles = articles_res_json["data"]
        for article in articles:
            article_nums += 1
            article_title = article["title"]
            article_url = article["url"]
            article_excerpt = article["excerpt"]
            print(article_title)
            Get.excelWrite(article_nums, 0, label=article_title, worksheet=ws)
            Get.excelWrite(article_nums, 1, label=article_url, worksheet=ws)
            Get.excelWrite(article_nums, 2, label=article_excerpt, worksheet=ws)

        offset += 20
        headers["referer"] = f"https://www.zhihu.com/people/{author}/posts?page={page_num}"
        page_num += 1

        articles_is_end = articles_res_json["paging"]["is_end"]
        if articles_is_end:
            break

        # # 爬两页就结束
        # if page_num > 2:
        #     break


def runZhiHuArticle():
    """ 获取一个知乎作者的所有文章名称、链接、及摘要，并存到Excel表里 """
    # Excel
    wb = Get.excelWrite(encoding='ascii')

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
from crawlerUtils import Get
import re


def queryChineseWeather(city_name="广州"):
    ''' 在中国天气网查询天气 '''
    while True:
        if not city_name:
            city_name = input("请问要查询哪里的天气：")
        city_url = f"http://toy1.weather.com.cn/search?cityname={Get.urlencode(city_name)}"
        city_json = Get.urllibOpenJson(city_url)

        if city_json:
            if city_json[0].get("ref"):
                city_string = city_json[0]["ref"]
                city_code = re.findall("\d+", city_string)[0]
        else:
            print("城市地址输入有误，请重新输入！")
            city_name = ""
            continue

        weather_url = f"http://www.weather.com.cn/weather1d/{city_code}.shtml"
        weather_soup = Get.urllibOpenSoup(weather_url)
        weather = weather_soup.find(
            "input", id="hidden_title").get("value").split()

        return weather


def runSendCityWeatherEveryDay(city="北京"):
    ''' 每天定时发送天气信息到指定邮箱 '''
    recipients, account, password, subj, text = Get.mailSendInput()
    weather = queryChineseWeather(city)
    text = " ".join(weather)
    daytime = input("请问每天的几点发送邮件？格式'18:30'，不包含单引号 ：")

    Get.scheduleFuncEveryDayTime(Get.mailSend, daytime, recipients, account,
                            password, subj, text)

```

### More...

## Examples Running

所有例子的源代码都在crawlerUtils/examples里

包括：
- 播放网易云音乐歌曲

```python
from crawlerUtils.examples import *


runPlayNeteaseSongs()
```

- 获取QQ音乐某个歌手的歌曲信息和评论

```python
from crawlerUtils.examples import *


runQQSinger()
```

- 获取知乎某个作者的所有文章

```python
from crawlerUtils.examples import *


runZhiHuArticle()
```

- 登陆饿了么并获取附近餐厅, 使用了向量空间进行验证码识别

```python
from crawlerUtils.examples import *


runElemeDishes()
```

- 获取豆瓣top250电影信息, 使用requests+正则表达式

```python
from crawlerUtils.examples import *


runDoubanTop250UseRegexExpression()
```

- 打印Python之禅, Selenium实现登录并用BeatifulSoup解析文本

```python
from crawlerUtils.examples import *


runLoginAndPrintZens()
```

- 每天定时发送天气信息邮件, 使用了urlopen及schedule等函数

```python
from crawlerUtils.examples import *


runSendCityWeatherEveryDay()
```

- 爬取薄荷网十一类食物的热量信息，使用了协程gevent库和写csv函数

```python
from gevent import monkey
monkey.patch_all()
from crawlerUtils.examples import runBoheGevent


runBoheGevent()
```

- 爬取时光网电影信息，使用了requests-html的并发模式及find等方法

```python
from crawlerUtils.examples import *


runShiGuang()
```

### Documentation：
requests: https://github.com/kennethreitz/requests

bs4: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

requests-html: https://github.com/kennethreitz/requests-html

selenium: https://www.seleniumhq.org/docs/

gevent: http://www.gevent.org/contents.html

excel: http://www.python-excel.org/

csv: https://docs.python.org/3/library/csv.html?highlight=csv#module-csv

log: https://docs.python.org/3/library/logging.html?highlight=log#module-logging

urllib: https://docs.python.org/3/library/urllib.html

email: https://docs.python.org/3/library/email.html?highlight=mail#module-email

schedule: https://schedule.readthedocs.io/en/stable/

regex: https://regexr.com/


## 更新记录
- Future
更新内容: 增加多进程模块、分布式等; 欢迎提交Pull Request。

- V1.7.0
更新内容: 集成了requests-html，支持并发和JavaScript解析(如r = Get(url).html; r.render();r.find();r.search();r.xpath())，重写examples里的shiguang.py；增加了utils.request里的async方法.

- V1.6.0
更新内容: 集成gevent，支持协程，增加examples里的shiguang.py；集成csv、math;重构utils.py及对应example，采用面向对象方式编写。

- V1.5.2
更新内容: 增加utils.log模块，加入moviedownload.py 多线程Windows64位版

- V1.5.0 
更新内容: 集成schedule库函数, 重构utils代码

- V1.4.2 
更新内容: 增加每日定时发送天气的example及定时发送邮件等函数

- V1.4.1 
更新内容: 封装了一些BeautifulSoup和Selenium函数、增加打印python之禅的例子


